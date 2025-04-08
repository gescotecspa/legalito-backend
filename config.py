import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")  # URI de conexión a la base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Clave secreta para la app Flask

    # Directorio donde se guardarán los archivos .ics para generar eventos sin depender de un proveedor
    ICS_FILES_PATH = os.getenv("ICS_FILES_PATH", "ics_files/")

    # Configuración SMTP para envío de correos
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_DEFAULT_SENDER = os.getenv("SMTP_DEFAULT_SENDER")

    # Mail remitente válido para filtrar correos a procesar
    ALLOWED_SENDER = os.getenv("ALLOWED_SENDER")

 # Configuración de Mailjet
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
    MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
    MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 10800)))