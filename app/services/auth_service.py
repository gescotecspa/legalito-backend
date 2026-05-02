from datetime import datetime, timezone
import secrets
from app import db
from app.models import User
from app.extensions import bcrypt
from app.integrations.mailjet_email import (
    MailjetDeliveryException,
    send_reset_email,
)
from flask_jwt_extended import create_access_token

class InvalidCredentialsException(Exception):
    pass


class InactiveAccountException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class InvalidResetCodeException(Exception):
    pass


class ExpiredResetCodeException(Exception):
    pass


class PasswordResetDeliveryException(Exception):
    pass


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        raise InvalidCredentialsException("Email o contraseña incorrectos")
    if not user.status or user.status.code.lower() != "active":
        raise InactiveAccountException("La cuenta no está activa")
    
    user.last_login = datetime.now(timezone.utc)
    db.session.commit()
    token = create_access_token(identity=user.user)
    
    return {
        "access_token": token,
        "user": user.serialize()
    }


def request_password_reset(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        raise UserNotFoundException("User not found")

    reset_code = str(secrets.randbelow(900000) + 100000)
    user.set_reset_code(reset_code)

    try:
        send_reset_email(user.email, user.first_name, reset_code)
    except MailjetDeliveryException as exc:
        db.session.rollback()
        raise PasswordResetDeliveryException("No se pudo enviar el correo de recuperacion") from exc

    db.session.commit()
    return {"message": "A recovery code has been sent to your email"}


def reset_password_with_code(email, reset_code, new_password):
    user = User.query.filter_by(email=email).first()
    if not user:
        raise UserNotFoundException("User not found")

    if user.reset_code != reset_code:
        raise InvalidResetCodeException("Incorrect code")
    if not user.reset_code_expiration or datetime.utcnow() > user.reset_code_expiration:
        raise ExpiredResetCodeException("Code expired")

    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.reset_code = None
    user.reset_code_expiration = None
    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {"message": "Password successfully updated"}
