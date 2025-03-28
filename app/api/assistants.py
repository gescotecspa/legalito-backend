from flask import Blueprint, request, jsonify,abort
from app.services.assistant_service import list_assistants,list_assistants_by_filter,add_favorite_assitant,list_assistants_favorite,delete_favorite_assistant,get_assistant, AssistantNotFoundException

assistants_bp = Blueprint('assistants', __name__)

@assistants_bp.route('/assistants', methods=['GET'])
def list_all_assistants():
    try:
        result = list_assistants()
        return jsonify([f.serialize() for f in result]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/filter/<int:typeId>/<int:regionId>', methods=['GET'])
def list_by_filter(typeId,regionId):
    try:
        data = list_assistants_by_filter(typeId,regionId)
        print(data)
        return jsonify(data), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorites', methods=['POST'])
def get_favorite():
    data = request.get_json()
    user = data.get('user')

    try:
        data = list_assistants_favorite(user)
        return jsonify([f.serialize() for f in data]), 200
    except AssistantNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/add', methods=['POST'])
def add_favorite ():
    
    data = request.get_json()
    assistantId = data.get('assistantId')
    user = data.get('user')

    try:
        print(user)
        add_favorite_assitant(assistantId,user)
       
        return jsonify(True), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/favorite/delete', methods=['DELETE'])
def delete_favorite ():
    
    data = request.get_json()
    assistantId = data.get('assistantId')
    user = data.get('user')

    try:
        delete_favorite_assistant(assistantId,user)
       
        return jsonify(True), 200
    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@assistants_bp.route('/assistants/profile/<int:id>', methods=['GET'])
def get_assistant_by_id(id):
    assistant = get_assistant(id)
    
    if not assistant:
        return jsonify({"error": "Assistant not found"}), 404
    
    return jsonify(assistant.serialize()), 200