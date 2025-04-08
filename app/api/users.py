from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.user_service import list_users, UserNotFoundException

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        data = list_users()
        return jsonify([f.serialize() for f in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500