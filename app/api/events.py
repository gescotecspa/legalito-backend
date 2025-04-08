from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.event_creator import create_and_send_ics_file
from app.services.event_service import list_events_by_user,EventNotFoundException

events_bp = Blueprint('events', __name__)

@events_bp.route('/create-and-send-event', methods=['POST'])
@jwt_required()
def create_and_send_event():
    data = request.json
    title = data.get('title')
    date = data.get('date')
    time = data.get('time')
    location = data.get('location')
    recipient_email = data.get('recipient_email')
    description = data.get('description', '')

    result = create_and_send_ics_file(
        title=title,
        date_str=date,
        time_str=time,
        location=location,
        recipient_email=recipient_email,
        description=description
    )

    return jsonify({"result": result})


@events_bp.route('/byuser', methods=['POST'])
@jwt_required()
def list_events_by_user():
    current_user = get_jwt_identity()
    data = request.get_json()
    user = current_user

    try:
    
        data = list_events_by_user(user)
        return jsonify([f.serialize() for f in data]), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/cases/filter/', methods=['GET'])
@jwt_required()
def get(id):
    abort(501)
