from flask import Blueprint, request, jsonify,abort
from app.event_creator import create_and_send_ics_file

events_bp = Blueprint('events', __name__)

@events_bp.route('/create-and-send-event', methods=['POST'])
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


@events_bp.route('/cases/user', methods=['POST'])
def list_events_by_user():
    data = request.get_json()
    user = data.get('user')

    #try:
    abort(501)
        #data = list_assistants_favorite(user)
        #return jsonify([f.serialize() for f in data]), 200
    #except AssistantNotFoundException as e:
    #    return jsonify({"error": str(e)}), 404
    #except Exception as e:
    #    return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/cases/filter/', methods=['GET'])
def get(id):
    abort(501)
