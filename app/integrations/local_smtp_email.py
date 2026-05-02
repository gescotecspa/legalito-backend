import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app, render_template


class LocalSmtpDeliveryException(Exception):
    pass


def load_reset_email_template(first_name, reset_code):
    return render_template(
        "emails/reset_password.html",
        first_name=first_name,
        reset_code=reset_code,
    )


def _required_config(key):
    value = current_app.config.get(key)
    if value:
        return value
    raise LocalSmtpDeliveryException(f"Missing required email configuration: {key}")


def send_reset_email(user_email, user_first_name, reset_code):
    smtp_server = _required_config("SMTP_SERVER")
    smtp_port = _required_config("SMTP_PORT")
    smtp_username = _required_config("SMTP_USERNAME")
    smtp_password = _required_config("SMTP_PASSWORD")
    sender_email = current_app.config.get("SMTP_DEFAULT_SENDER") or smtp_username

    email_html = load_reset_email_template(user_first_name, reset_code)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Codigo de recuperacion de contrasena"
    msg["From"] = sender_email
    msg["To"] = user_email
    msg.attach(MIMEText(email_html, "html", "utf-8"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, [user_email], msg.as_string())
    except Exception as exc:
        raise LocalSmtpDeliveryException(f"Local SMTP delivery failed: {exc}") from exc

    return {"status": 200, "message": "Email sent via local SMTP"}
