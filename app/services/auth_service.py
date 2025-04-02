from app import db
from app.models import User
from app.extensions import bcrypt
from flask_jwt_extended import create_access_token

class InvalidCredentialsException(Exception):
    pass

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        raise InvalidCredentialsException("Email o contraseña incorrectos")

    token = create_access_token(identity=user.user)
    
    return {
        "access_token": token,
        "user": {
            "user": user.user,
            "email": user.email,
            "first_name": user.first_name,
            "last_name":user.last_name,  # Ajustá según tus campos
        }
    }
