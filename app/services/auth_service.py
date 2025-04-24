from datetime import datetime, timezone
from app import db
from app.models import User
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token

class InvalidCredentialsException(Exception):
    pass
class InactiveAccountException(Exception):
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
