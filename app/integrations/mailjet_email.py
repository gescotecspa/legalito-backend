import os
import requests
from flask import render_template

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")


class MailjetDeliveryException(Exception):
    pass


def load_email_template(first_name, reset_code):
    return render_template(
        "emails/reset_password.html",
        first_name=first_name,
        reset_code=reset_code,
    )


def send_reset_email(user_email, user_first_name, reset_code):
    email_html = load_email_template(user_first_name, reset_code)

    url = "https://api.mailjet.com/v3.1/send"
    headers = {"Content-Type": "application/json"}
    data = {
        "Messages": [{
            "From": {"Email": MAILJET_SENDER_EMAIL, "Name": "Legalito"},
            "To": [{"Email": user_email, "Name": user_first_name}],
            "Subject": "Código de recuperación de contraseña",
            "HTMLPart": email_html
        }]
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
    )

    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text

    if not response.ok:
        raise MailjetDeliveryException(
            f"Mailjet delivery failed with status {response.status_code}: {response_body}"
        )

    return {"status": response.status_code, "message": response_body}
