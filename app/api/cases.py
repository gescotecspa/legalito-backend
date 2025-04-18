from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from app.services.case_service import create_case, list_cases, delete_case,list_cases_by_user, CaseAlreadyExistsException, CaseNotFoundException

case_bp = Blueprint('cases', __name__)

@case_bp.route('/cases', methods=['POST'])
@jwt_required()
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
@jwt_required()
def list_cases():
    try:
        cases = list_cases()
        return jsonify([case.serialize() for case in cases]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@case_bp.route('/cases/<int:case_id>', methods=['DELETE'])
@jwt_required()
def delete_case(case_id):
    try:
        delete_case(case_id)
        return jsonify({"message": "Case deleted successfully."}), 200
    except CaseNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@case_bp.route('/cases', methods=['PUT'])
@jwt_required()
def update():
    abort(501)

@case_bp.route('/cases/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    abort(501)

@case_bp.route('/cases/byUser', methods=['POST'])
@jwt_required()
def list_by_user():
    
    data = request.get_json()
    user = data.get('user')
    
    try:
        data = list_cases_by_user(user)
        return jsonify([n.serialize() for n in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500 