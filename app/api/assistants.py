from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.assistant_service import (
    AssistantNotFoundException,
    add_favorite_assistant_service,
    delete_favorite_assistant_service,
    get_assistant_service,
    list_assistants_by_filter_service,
    list_assistants_favorite_service,
    list_assistants_service,
)

assistants_bp = Blueprint('assistants', __name__)

@assistants_bp.route('/assistants', methods=['GET'])
@jwt_required()
def list_all_assistants():
    try:
        result = list_assistants_service()
        return jsonify([f.serialize() for f in result]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/filter/<int:typeId>/<int:regionId>', methods=['GET'])
@jwt_required()
def list_by_filter(typeId,regionId):
    try:
        data = list_assistants_by_filter_service(typeId,regionId)
        
        return jsonify(data), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorites', methods=['POST'])
@jwt_required()
def get_favorite():
    user = get_jwt_identity()

    try:
        data = list_assistants_favorite_service(user)
        return jsonify(data), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/add', methods=['POST'])
@jwt_required()
def add_favorite ():
    
    data = request.get_json() or {}
    assistantId = data.get('assistantId')
    user = get_jwt_identity()

    try:
        add_favorite_assistant_service(assistantId,user)
       
        return jsonify(True), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/delete', methods=['DELETE'])
@jwt_required()
def delete_favorite ():
    
    data = request.get_json() or {}
    assistantId = data.get('assistantId')
    user = get_jwt_identity()

    try:
        delete_favorite_assistant_service(assistantId,user)
       
        return jsonify(True), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error deleting favorite assistant")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_assistant_by_id(id):
    assistant = get_assistant_service(id)
    
    if not assistant:
        return jsonify({"error": "Assistant not found"}), 404
    
    return jsonify(assistant.serialize()), 200
