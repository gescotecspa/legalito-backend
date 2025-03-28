from flask import Blueprint, request, jsonify
from app.services.auth_service import login_user, InvalidCredentialsException

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

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
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    #try:
        user = register_user(email, password, first_name, last_name)
        return jsonify({"message": "Usuario registrado con éxito", "user": user}), 201
    #except EmailAlreadyExistsException as e:
    #    return jsonify({"error": str(e)}), 409
    #except Exception as e:
    #    return jsonify({"error": f"Error inesperado: {str(e)}"}), 500