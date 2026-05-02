from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.mail_service import (
    ActiveEmailAccountNotFoundException,
    MailReadIntegrationException,
    SenderFilterNotFoundException,
    read_mails_for_user,
)

mails_bp = Blueprint('mails', __name__)

@mails_bp.route('/read-mails', methods=['POST'])
@jwt_required()
def read_mails():
    data = request.get_json() or {}
    email_to_check = data.get('email')
    user = get_jwt_identity()

    try:
        result = read_mails_for_user(email_to_check, user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except SenderFilterNotFoundException as e:
        return jsonify({"error": str(e)}), 400
    except ActiveEmailAccountNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except MailReadIntegrationException as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
