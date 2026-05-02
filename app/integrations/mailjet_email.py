import requests
from flask import current_app, render_template


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
    api_key = current_app.config.get("MAILJET_API_KEY")
    api_secret = current_app.config.get("MAILJET_API_SECRET")
    sender_email = current_app.config.get("MAILJET_SENDER_EMAIL")

    if not api_key or not api_secret or not sender_email:
        raise MailjetDeliveryException(
            "Missing required Mailjet configuration: MAILJET_API_KEY, MAILJET_API_SECRET or MAILJET_SENDER_EMAIL"
        )

    url = "https://api.mailjet.com/v3.1/send"
    headers = {"Content-Type": "application/json"}
    data = {
        "Messages": [{
            "From": {"Email": sender_email, "Name": "Legalito"},
            "To": [{"Email": user_email, "Name": user_first_name}],
            "Subject": "Código de recuperación de contraseña",
            "HTMLPart": email_html
        }]
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=(api_key, api_secret),
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
