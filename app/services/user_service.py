import jwt
import datetime
from flask import current_app
from app import db
from app.models import User
from app.extensions import bcrypt
from app.utils.image_handler import save_base64_image
from datetime import datetime, timezone

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

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_reset_token(user_id):
    """Genera un token de recuperación de contraseña válido por 1 hora."""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expira en 1 hora
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def reset_password(token, new_password):
    """Valida el token y actualiza la contraseña del usuario."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(payload["user_id"])

        if not user:
            return False, "Usuario no encontrado"

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())  
        user.password_hash = hashed_password.decode('utf-8')
        db.session.commit()
        return True, "Contraseña actualizada con éxito"
    
    except jwt.ExpiredSignatureError:
        return False, "Token expirado"
    except jwt.InvalidTokenError:
        return False, "Token inválido"
    
    
def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        raise UserNotFoundException()

    allowed_fields = ['first_name', 'last_name', 'phone_number', 'birth_date']
    
    for key in allowed_fields:
        if key in data:
            if key == 'birth_date':
                user.birth_date = datetime.fromisoformat(data[key])
            else:
                setattr(user, key, data[key])

    if 'image_base64' in data and data['image_base64']:
        image_url = save_base64_image(data['image_base64'], user.user, user.image_url)
        user.image_url = image_url

    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return user