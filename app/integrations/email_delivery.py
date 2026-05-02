from flask import current_app

from app.integrations.local_smtp_email import (
    LocalSmtpDeliveryException,
    send_reset_email as send_reset_email_via_local_smtp,
)
from app.integrations.mailjet_email import (
    MailjetDeliveryException,
    send_reset_email as send_reset_email_via_api,
)


class EmailDeliveryException(Exception):
    pass


def get_email_delivery_method():
    return (current_app.config.get("EMAIL_DELIVERY_METHOD") or "api").strip().lower()


def send_reset_email(user_email, user_first_name, reset_code):
    method = get_email_delivery_method()

    try:
        if method == "local":
            return send_reset_email_via_local_smtp(user_email, user_first_name, reset_code)
        if method == "api":
            return send_reset_email_via_api(user_email, user_first_name, reset_code)
    except (LocalSmtpDeliveryException, MailjetDeliveryException) as exc:
        raise EmailDeliveryException(str(exc)) from exc

    raise EmailDeliveryException(
        f"Unsupported EMAIL_DELIVERY_METHOD '{method}'. Expected one of: local, api."
    )
