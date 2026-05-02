from datetime import datetime

from flask import current_app

from app.integrations.imap_reader import read_unread_emails_for_account
from app.integrations.smtp_calendar import create_and_send_ics_file
from app.services.email_account_service import get_user_active_email
from app.services.notification_service import create_notification
from app.services.parameter_service import list_parameters_by_parent
from app.utils.info_extractor import extract_event_info


class SenderFilterNotFoundException(Exception):
    pass


class ActiveEmailAccountNotFoundException(Exception):
    pass


class MailReadIntegrationException(Exception):
    pass


def read_mails_for_user(email_to_check, user):
    if not email_to_check:
        raise ValueError("Email parameter is required.")
    if not user:
        raise ValueError("User parameter is required.")

    sender_filters = list_parameters_by_parent(32)
    if not sender_filters:
        raise SenderFilterNotFoundException("Email parameter not found.")

    sender_filter = sender_filters[0].name
    account = get_user_active_email(user, email_to_check)
    if not account:
        raise ActiveEmailAccountNotFoundException(
            "No active account found with the provided email."
        )

    emails = read_unread_emails_for_account(
        imap_server=account.imap_server,
        email_address=account.email_address,
        password=account.password,
        sender=sender_filter,
    )

    if emails and len(emails) == 1 and emails[0].get("error"):
        raise MailReadIntegrationException(emails[0]["error"])

    extracted_events = []

    for email_data in emails:
        subject = email_data.get("subject", "Sin asunto")
        body = email_data.get("body", "")
        sender = email_data.get("from", "Desconocido")
        received_date = email_data.get("date") or datetime.utcnow().isoformat()
        event_info = extract_event_info(subject, body)
        marked_as_invitation = "citacion" in subject.lower() or "citación" in subject.lower()

        notification_data = {
            "folio_id": None,
            "rit": event_info.get("rit"),
            "subject": subject,
            "sender": sender,
            "received_date": received_date,
            "body": body,
            "marked_as_invitation": marked_as_invitation,
            "status": "pending",
            "user": user,
        }

        notification = create_notification(notification_data)
        if not notification:
            current_app.logger.warning(
                "Notification creation failed for email subject '%s'",
                subject,
            )
            continue

        if sender_filter in (sender or "").lower() and marked_as_invitation:
            if all([event_info.get("date"), event_info.get("time"), event_info.get("title")]):
                result = create_and_send_ics_file(
                    title=event_info["title"],
                    date_str=event_info["date"],
                    time_str=event_info["time"],
                    location=event_info.get("location"),
                    recipient_email=user,
                    description=event_info["title"],
                )
                extracted_events.append(
                    {
                        "email_subject": subject,
                        "from": sender,
                        "extracted_info": event_info,
                        "event_result": result,
                    }
                )

    return {
        "email_address": account.email_address,
        "extracted_events": extracted_events,
    }
