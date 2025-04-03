import requests
import os
import random

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "email_reset_password.html")

def generate_reset_code():
    return str(random.randint(100000, 999999))  # Código de 6 dígitos

def load_email_template(first_name, reset_code):
    """Carga el HTML localmente y reemplaza las variables."""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        template = file.read()
    
    # Reemplazamos las variables en el HTML
    template = template.replace("{{ first_name }}", first_name)
    template = template.replace("{{ reset_code }}", reset_code)
    
    return template

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

    response = requests.post(url, json=data, headers=headers, auth=(MAILJET_API_KEY, MAILJET_API_SECRET))
    return {"status": response.status_code, "message": response.json()}