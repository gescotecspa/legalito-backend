from flask import Blueprint, jsonify, request
from app.models import EmailAccount
from app.imap_reader import read_unread_emails_for_account
from app.info_extractor import extract_event_info
from app.event_creator import create_and_send_ics_file
from app.services.notification_service import create_notification
from config import Config
from datetime import datetime

mails_bp = Blueprint('mails', __name__)

@mails_bp.route('/read-mails', methods=['POST'])
def read_mails():
    data = request.get_json()
    email_to_check = data.get('email')
    if not email_to_check:
        return jsonify({"error": "Email parameter is required."}), 400

    account = EmailAccount.query.filter_by(active=True, email_address=email_to_check).first()
    if not account:
        return jsonify({"error": "No active account found with the provided email."}), 404

    emails = read_unread_emails_for_account(
        imap_server=account.imap_server,
        email_address=account.email_address,
        password=account.password
    )

    extracted_events = []
    sender_filter = Config.ALLOWED_SENDER.lower()

    for email_data in emails:
        subject = email_data.get("subject", "Sin asunto")
        body = email_data.get("body", "")
        sender = email_data.get("from", "Desconocido")
        received_date = email_data.get("date") or datetime.utcnow().isoformat()

        notification_data = {
            "folio_id": None,
            "rit": extract_event_info(subject, body).get("rit"),
            "subject": subject,
            "sender": sender,
            "received_date": received_date,
            "body": body,
            "marked_as_invitation": "citación" in subject.lower(),
            "status": "processed"
        }

        try:
            create_notification(notification_data)
        except Exception as e:
            print(f"Error creating notification: {e}")
            continue

        if sender_filter in sender.lower() and notification_data["marked_as_invitation"]:
            event_info = extract_event_info(subject, body)
            if all([event_info.get("date"), event_info.get("time"), event_info.get("title")]):
                result = create_and_send_ics_file(
                    title=event_info["title"],
                    date_str=event_info["date"],
                    time_str=event_info["time"],
                    location=event_info.get("location"),
                    recipient_email="javieraoyarzun1991@gmail.com",
                    description=event_info["title"]
                )
                extracted_events.append({
                    "email_subject": subject,
                    "from": sender,
                    "extracted_info": event_info,
                    "event_result": result
                })

    return jsonify({
        'email_address': account.email_address,
        'extracted_events': extracted_events
    })
