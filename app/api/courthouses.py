from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.courthouse_service import list_courthouses_service

courthouses_bp = Blueprint('courthouses', __name__)

@courthouses_bp.route('/courthouses', methods=['GET'])
@jwt_required()
def get_courthouses():
    try:
        data = list_courthouses_service()
        return jsonify([f.serialize() for f in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
