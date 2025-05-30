from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.assistant_service import list_assistants,list_assistants_by_filter,add_favorite_assitant,list_assistants_favorite,delete_favorite_assistant,get_assistant, AssistantNotFoundException

assistants_bp = Blueprint('assistants', __name__)

@assistants_bp.route('/assistants', methods=['GET'])
@jwt_required()
def list_all_assistants():
    try:
        result = list_assistants()
        return jsonify([f.serialize() for f in result]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/filter/<int:typeId>/<int:regionId>', methods=['GET'])
@jwt_required()
def list_by_filter(typeId,regionId):
    try:
        data = list_assistants_by_filter(typeId,regionId)
        
        return jsonify(data), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorites', methods=['POST'])
@jwt_required()
def get_favorite():
    data = request.get_json()
    user = get_jwt_identity()

    try:
        data = list_assistants_favorite(user)
        return jsonify(data), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/add', methods=['POST'])
@jwt_required()
def add_favorite ():
    
    data = request.get_json()
    assistantId = data.get('assistantId')
    user = get_jwt_identity()

    try:
        print(user)
        add_favorite_assitant(assistantId,user)
       
        return jsonify(True), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/delete', methods=['DELETE'])
@jwt_required()
def delete_favorite ():
    
    data = request.get_json()
    assistantId = data.get('assistantId')
    user = get_jwt_identity()

    try:
        delete_favorite_assistant(assistantId,user)
       
        return jsonify(True), 200
    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/profile/<int:id>', methods=['GET'])
@jwt_required()
def get_assistant_by_id(id):
    assistant = get_assistant(id)
    
    if not assistant:
        return jsonify({"error": "Assistant not found"}), 404
    
    return jsonify(assistant.serialize()), 200