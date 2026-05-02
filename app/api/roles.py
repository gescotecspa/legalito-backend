from flask import Blueprint, jsonify

from app.services.rol_service import list_roles_service

roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/roles', methods=['GET'])
def get_roles():
    try:
        data = list_roles_service()
        return jsonify([f.serialize() for f in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
