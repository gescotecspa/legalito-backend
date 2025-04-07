from datetime import datetime
import bcrypt
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.auth_service import login_user, InvalidCredentialsException
from app.services.email_service import send_reset_email
from app.services.user_service import create_reset_token, get_user_by_email, register_user, EmailAlreadyExistsException, reset_password
import random
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    print (email)
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        result = login_user(email, password)
        return jsonify(result), 200
    except InvalidCredentialsException as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "El request debe ser JSON"}), 415

    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = register_user(email, password, first_name, last_name)
        return jsonify({"message": "User successfully registered", "user": user}), 201
    except EmailAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    
@auth_bp.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    reset_code = str(random.randint(100000, 999999)) 
    user.set_reset_code(reset_code)
    db.session.commit()

    send_reset_email(user.email, user.first_name, reset_code)  
    return jsonify({"message": "A recovery code has been sent to your email"}), 200

@auth_bp.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    reset_code = data.get('reset_code')
    new_password = data.get('password')

    if not email or not reset_code or not new_password:
        return jsonify({"error": "Email, reset code, and new password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verificar que el código es correcto y no ha expirado
    if user.reset_code != reset_code:
        return jsonify({"error": "Incorrect code"}), 400
    if datetime.utcnow() > user.reset_code_expiration:
        return jsonify({"error": "Code expired"}), 400

    # Actualizar la contraseña
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())  
    user.password_hash = hashed_password.decode('utf-8')

    # Eliminar el código usado
    user.reset_code = None
    user.reset_code_expiration = None
    db.session.commit()

    return jsonify({"message": "Password successfully updated"}), 200