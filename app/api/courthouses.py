from flask import Blueprint, request, jsonify
from app.services.courthouse_service import list_courthouses, CourthouseNotFoundException

courthouses_bp = Blueprint('courthouses', __name__)

@courthouses_bp.route('/courthouses', methods=['GET'])
def get_courthouses():
    try:
        data = list_courthouses()
        return jsonify([f.serialize() for f in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500