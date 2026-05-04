import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # URI de conexión a la base de datos
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # Clave secreta para la app Flask
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    # Directorio donde se guardarán los archivos .ics para generar eventos sin depender de un proveedor
    ICS_FILES_PATH = os.getenv("ICS_FILES_PATH", "ics_files/")

    # Configuración SMTP para envío de correos
    EMAIL_DELIVERY_METHOD = os.getenv("EMAIL_DELIVERY_METHOD", "local")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_DEFAULT_SENDER = os.getenv("SMTP_DEFAULT_SENDER")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").strip().lower() in {"1", "true", "yes", "on"}
    SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").strip().lower() in {"1", "true", "yes", "on"}

    # Mail remitente válido para filtrar correos a procesar
    ALLOWED_SENDER = os.getenv("ALLOWED_SENDER")

 # Configuración de Mailjet
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
    MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
    MAILJET_SENDER_EMAIL = os.getenv("MAILJET_SENDER_EMAIL")
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 10800)))
    AUTH_LOGIN_RATE_LIMIT_ATTEMPTS = int(os.getenv("AUTH_LOGIN_RATE_LIMIT_ATTEMPTS", 5))
    AUTH_LOGIN_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AUTH_LOGIN_RATE_LIMIT_WINDOW_SECONDS", 300))
    AUTH_FORGOT_PASSWORD_RATE_LIMIT_ATTEMPTS = int(os.getenv("AUTH_FORGOT_PASSWORD_RATE_LIMIT_ATTEMPTS", 3))
    AUTH_FORGOT_PASSWORD_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AUTH_FORGOT_PASSWORD_RATE_LIMIT_WINDOW_SECONDS", 900))
    AUTH_RESET_PASSWORD_RATE_LIMIT_ATTEMPTS = int(os.getenv("AUTH_RESET_PASSWORD_RATE_LIMIT_ATTEMPTS", 5))
    AUTH_RESET_PASSWORD_RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("AUTH_RESET_PASSWORD_RATE_LIMIT_WINDOW_SECONDS", 900))
