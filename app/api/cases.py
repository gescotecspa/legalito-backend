from flask import Blueprint, request, jsonify, abort
from app.services.case_service import create_case, list_cases, delete_case, CaseAlreadyExistsException, CaseNotFoundException

case_bp = Blueprint('cases', __name__)

@case_bp.route('/cases', methods=['POST'])
def add_case():
    data = request.get_json()
    try:
        new_case = create_case(data)
        return jsonify({"message": "Case created successfully.", "case": new_case.serialize()}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except CaseAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@case_bp.route('/cases/list', methods=['GET'])
def list_cases():
    try:
        cases = list_cases()
        return jsonify([case.serialize() for case in cases]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@case_bp.route('/cases/<int:case_id>', methods=['DELETE'])
def delete_case(case_id):
    try:
        delete_case(case_id)
        return jsonify({"message": "Case deleted successfully."}), 200
    except CaseNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@case_bp.route('/cases', methods=['PUT'])
def update():
    abort(501)

@case_bp.route('/cases/<int:id>', methods=['GET'])
def get(id):
    abort(501)