from flask import Blueprint, request, jsonify
from app.services.parameter_service import list_parameters,list_parameters_by_parent, ParameterNotFoundException

parameters_bp = Blueprint('parameters', __name__)

@parameters_bp.route('/parameters', methods=['GET'])
def get_paramters():
    try:
        parametes = list_parameters()
        return jsonify([f.serialize() for f in parametes]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@parameters_bp.route('/parameters/byparent/<int:parent_id>', methods=['GET'])
def get_by_parent(parent_id):
    try:
        parametes = list_parameters_by_parent(parent_id)
        return jsonify([f.serialize() for f in parametes]), 200
    except ParameterNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500