from flask import Blueprint, current_app, jsonify, request
from app.services.auth_service import (
    ExpiredResetCodeException,
    InactiveAccountException,
    InvalidCredentialsException,
    InvalidResetCodeException,
    PasswordResetDeliveryException,
    UserNotFoundException as AuthUserNotFoundException,
    login_user,
    request_password_reset,
    reset_password_with_code,
)
from app.services.user_service import (
    EmailAlreadyExistsException,
    register_user,
)
from app.utils.rate_limit import rate_limiter

auth_bp = Blueprint('auth', __name__)


def _client_identifier():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _rate_limit_key(scope, email=None):
    normalized_email = (email or "").strip().lower()
    return f"{scope}:{_client_identifier()}:{normalized_email}"


def _rate_limit_response(message, retry_after):
    response = jsonify({"error": message})
    response.status_code = 429
    response.headers["Retry-After"] = str(retry_after)
    return response


def _check_rate_limit(scope, email, limit_config_key, window_config_key, message):
    limit = current_app.config[limit_config_key]
    window_seconds = current_app.config[window_config_key]
    allowed, retry_after = rate_limiter.hit(
        _rate_limit_key(scope, email),
        limit,
        window_seconds,
    )

    if allowed:
        return None

    return _rate_limit_response(message, retry_after)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    rate_limit_response = _check_rate_limit(
        "auth-login",
        email,
        "AUTH_LOGIN_RATE_LIMIT_ATTEMPTS",
        "AUTH_LOGIN_RATE_LIMIT_WINDOW_SECONDS",
        "Too many login attempts. Please try again later.",
    )
    if rate_limit_response:
        return rate_limit_response

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

    rate_limit_response = _check_rate_limit(
        "auth-forgot-password",
        email,
        "AUTH_FORGOT_PASSWORD_RATE_LIMIT_ATTEMPTS",
        "AUTH_FORGOT_PASSWORD_RATE_LIMIT_WINDOW_SECONDS",
        "Too many password recovery attempts. Please try again later.",
    )
    if rate_limit_response:
        return rate_limit_response

    try:
        result = request_password_reset(email)
        return jsonify(result), 200
    except AuthUserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except PasswordResetDeliveryException as e:
        return jsonify({"error": str(e)}), 502
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

    rate_limit_response = _check_rate_limit(
        "auth-reset-password",
        email,
        "AUTH_RESET_PASSWORD_RATE_LIMIT_ATTEMPTS",
        "AUTH_RESET_PASSWORD_RATE_LIMIT_WINDOW_SECONDS",
        "Too many password reset attempts. Please try again later.",
    )
    if rate_limit_response:
        return rate_limit_response

    try:
        result = reset_password_with_code(email, reset_code, new_password)
        return jsonify(result), 200
    except AuthUserNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except (InvalidResetCodeException, ExpiredResetCodeException) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
