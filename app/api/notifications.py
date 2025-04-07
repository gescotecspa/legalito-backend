from flask import Blueprint, request, jsonify
from app.services.notification_service import get_notification,create_notification, list_notifications, delete_notification, get_notifications_by_user,NotificationNotFoundException

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['POST'])
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
def list_notifications():
    try:
        notifications = list_notifications()
        return jsonify([n.serialize() for n in notifications]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@notifications_bp.route('/notifications/<int:id>', methods=['GET'])
def get_notification_by_id(id):
    try:
    
        notification = get_notification(id)

        if not notification:
            return jsonify({"error": "Notification not found"}), 404
    
        return jsonify(notification.serialize()), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@notifications_bp.route('/notifications/byUser', methods=['POST'])
def list_notifications_by_user():
    data = request.get_json()
    user = data.get('user')
    
    try:
        data = get_notifications_by_user(user)
        return jsonify([n.serialize() for n in data]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@notifications_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
def remove_notification(notification_id):
    try:
        delete_notification(notification_id)
        return jsonify({"message": "Notification deleted successfully."}), 200
    except NotificationNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
