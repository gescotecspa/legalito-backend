from flask import Blueprint, request, jsonify
from app.services.auth_service import (
    ExpiredResetCodeException,
    InactiveAccountException,
    InvalidCredentialsException,
    InvalidResetCodeException,
    UserNotFoundException as AuthUserNotFoundException,
    login_user,
    request_password_reset,
    reset_password_with_code,
)
from app.services.user_service import (
    EmailAlreadyExistsException,
    UserNotFoundException as UserServiceUserNotFoundException,
    delete_user,
    register_user,
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        result = login_user(email, password)
        return jsonify(result), 200
    except InvalidCredentialsException as e:
        return jsonify({"error": str(e)}), 401
    except InactiveAccountException as e:
        return jsonify({"error": str(e)}), 403
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

    try:
        result = request_password_reset(email)
        return jsonify(result), 200
    except AuthUserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@auth_bp.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    reset_code = data.get('reset_code')
    new_password = data.get('password')

    if not email or not reset_code or not new_password:
        return jsonify({"error": "Email, reset code, and new password are required"}), 400

    try:
        result = reset_password_with_code(email, reset_code, new_password)
        return jsonify(result), 200
    except AuthUserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except (InvalidResetCodeException, ExpiredResetCodeException) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@auth_bp.route('/auth/delete-account', methods=['POST'])
def delete_account():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    try:
        delete_user(email, password)
        return jsonify({"message": "Cuenta eliminada exitosamente"}), 200
    except UserServiceUserNotFoundException:
        return jsonify({"error": "Usuario no encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
