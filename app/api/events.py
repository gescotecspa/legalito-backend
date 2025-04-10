from flask import Blueprint, request, jsonify,abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.event_creator import create_and_send_ics_file
from app.services.event_service import create_event, delete_event_service, edit_event_service, EventNotFoundException, list_events_by_user_service

events_bp = Blueprint('events', __name__)

@events_bp.route('/events/create-and-send-event', methods=['POST'])
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


# @events_bp.route('/byuser', methods=['POST'])
# @jwt_required()
# def list_events_by_user():
#     current_user = get_jwt_identity()
#     data = request.get_json()
#     user = current_user

#     try:
    
#         data = list_events_by_user(user)
#         return jsonify([f.serialize() for f in data]), 200
#     except EventNotFoundException as e:
#         return jsonify({"error": str(e)}), 404
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/events/cases/filter/', methods=['GET'])
@jwt_required()
def get(id):
    abort(501)


@events_bp.route('/events/create', methods=['POST'])
@jwt_required()
def create_event_api():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data.get('title') or not data.get('start_date'):
        return jsonify({"error": "Faltan datos requeridos"}), 400

    try:
        event = create_event(
            user_id=current_user,
            title=data['title'],
            start_date=data['start_date'],
            description=data.get('description', ''),
            type_id=data.get('type_id')
        )
        return jsonify(event.serialize()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/events/byuser', methods=['GET'])
@jwt_required()
def list_events_by_user():
    current_user = get_jwt_identity()
    try:
        events = list_events_by_user_service(current_user)
        return jsonify([event.serialize() for event in events]), 200
    except EventNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/events/edit/<int:event_id>', methods=['PUT'])
@jwt_required()
def edit_event(event_id):
    current_user = get_jwt_identity()  # Obtener el usuario desde el JWT
    data = request.get_json()  # Obtener los datos de la solicitud

    try:
        # Llamamos al servicio para editar el evento
        event = edit_event_service(
            event_id=event_id,
            user_id=current_user,
            title=data.get('title'),
            start_date=data.get('start_date'),
            description=data.get('description'),
            type_id=data.get('type_id')
        )
        return jsonify(event.serialize()), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    
@events_bp.route('/events/delete/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    current_user = get_jwt_identity() 

    try:
        delete_event_service(event_id=event_id, user_id=current_user)
        return jsonify({"message": "Evento eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500