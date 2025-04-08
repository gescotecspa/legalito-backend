from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.folio_service import create_folio, list_folios, delete_folio, FolioNotFoundException

folios_bp = Blueprint('folios', __name__)

@folios_bp.route('/folios', methods=['POST'])
@jwt_required()
def add_folio():
    data = request.get_json()
    try:
        new_folio = create_folio(data)
        return jsonify({"message": "Folio created successfully.", "folio": new_folio.serialize()}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@folios_bp.route('/folios', methods=['GET'])
@jwt_required()
def get_folios():
    try:
        folios = list_folios()
        return jsonify([f.serialize() for f in folios]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@folios_bp.route('/folios/<int:folio_id>', methods=['DELETE'])
@jwt_required()
def remove_folio(folio_id):
    try:
        delete_folio(folio_id)
        return jsonify({"message": "Folio deleted successfully."}), 200
    except FolioNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
