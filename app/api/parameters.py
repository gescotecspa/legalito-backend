from flask import Blueprint, jsonify

from app.services.parameter_service import (
    ParameterNotFoundException,
    list_parameters_by_parent_service,
    list_parameters_service,
)

parameters_bp = Blueprint('parameters', __name__)

@parameters_bp.route('/parameters', methods=['GET'])
def get_paramters():
    try:
        parametes = list_parameters_service()
        return jsonify([f.serialize() for f in parametes]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@parameters_bp.route('/parameters/byparent/<int:parent_id>', methods=['GET'])
def get_by_parent(parent_id):
    try:
        parametes = list_parameters_by_parent_service(parent_id)
        return jsonify([f.serialize() for f in parametes]), 200
    except ParameterNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
