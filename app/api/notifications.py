from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.notification_service import get_notification,create_notification, list_notifications, delete_notification, get_notifications_by_user,dismiss,NotificationNotFoundException

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['POST'])
@jwt_required()
def add_notification():
    data = request.get_json()
    try:
        new_notification = create_notification(data)
        return jsonify({"message": "Notification created successfully.", "notification": new_notification.serialize()}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@notifications_bp.route('/notifications/list', methods=['GET'])
@jwt_required()
def list_notifications():
    try:
        notifications = list_notifications()
        return jsonify([n.serialize() for n in notifications]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@notifications_bp.route('/notifications/<int:id>', methods=['GET'])
@jwt_required()
def get_notification_by_id(id):
    try:
    
        notification = get_notification(id)

        if not notification:
            return jsonify({"error": "Notification not found"}), 404
    
        return jsonify(notification.serialize()), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@notifications_bp.route('/notifications/byUser', methods=['POST'])
#@jwt_required()
def list_notifications_by_user():
    #current_user = get_jwt_identity()
    data = request.get_json()
    #user = current_user
    user = data.get('user')
    try:
        data = get_notifications_by_user(user)
        return jsonify([n.serialize() for n in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@notifications_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def remove_notification(notification_id):
    try:
        delete_notification(notification_id)
        return jsonify({"message": "Notification deleted successfully."}), 200
    except NotificationNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@notifications_bp.route('/notifications/dismiss', methods=['POST'])
@jwt_required()
def dismiss_notifications():
    #current_user = get_jwt_identity()
    data = request.get_json()
    
    id = data.get('id')
    user = data.get('user')
    print(data)
    #user = current_user
    
    try:
        result = dismiss(id,user)
        return jsonify(True), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
