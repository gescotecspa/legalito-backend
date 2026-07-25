from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.case_service import (
    CaseAlreadyExistsException,
    CaseNotFoundException,
    CaseOwnershipException,
    create_case,
    delete_case_service,
    get_case_by_user_service,
    list_cases_by_user_service,
    list_cases_service,
)

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
def list_cases_route():
    try:
        cases = list_cases_service()
        return jsonify([case.serialize() for case in cases]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@case_bp.route('/cases/<int:case_id>', methods=['DELETE'])
@jwt_required()
def delete_case_route(case_id):
    try:
        delete_case_service(case_id)
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
    current_user = get_jwt_identity()

    try:
        case = get_case_by_user_service(id, current_user)
        return jsonify(case.serialize()), 200
    except CaseOwnershipException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@case_bp.route('/cases/byUser', methods=['POST'])
@jwt_required()
def list_by_user():
    user = get_jwt_identity()

    try:
        data = list_cases_by_user_service(user)
        return jsonify([n.serialize() for n in data]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500 
