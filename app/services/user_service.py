from app import db
from app.models import User
from app.extensions import bcrypt

class UserAlreadyExistsException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class EmailAlreadyExistsException(Exception):
    pass

def list_users():
    return User.query.all()

def register_user(email, password, first_name, last_name):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise EmailAlreadyExistsException("El email ya está registrado")

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        user= email,
        email=email,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name
    )

    db.session.add(user)
    db.session.commit()

    return {
        "user": user.user,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

def delete(user):
    pass
