from datetime import datetime
from app.models import Event, User, Parameter
from app import db

class EventNotFoundException:
    pass

def create_event(user_id, title, start_date, description=None, type_id=None):
    # Validar la fecha de inicio
    try:
        start_date = datetime.fromisoformat(start_date)
    except ValueError:
        raise ValueError("Formato de fecha inválido")

    user = User.query.filter_by(user=user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")

    # Si se ha proporcionado un type_id, buscar el parámetro correspondiente
    if type_id:
        parameter = Parameter.query.get(type_id)
        if not parameter:
            raise ValueError("Tipo de evento no encontrado")
    else:
        parameter = None

    event = Event(
        user=user_id,
        title=title,
        description=description,
        start_date=start_date,
        type_id=type_id,
    )

    db.session.add(event)
    db.session.commit()

    return event

def delete_event_service(event_id, user_id):
    event = Event.query.filter_by(id=event_id, user=user_id).first()
    if not event:
        raise ValueError("El evento no fue encontrado o no pertenece a este usuario.")
    db.session.delete(event)
    db.session.commit()

def edit_event_service(event_id, user_id, title=None, start_date=None, description=None, type_id=None):
    event = Event.query.filter_by(id=event_id, user=user_id).first()
    if not event:
        raise ValueError("El evento no fue encontrado o no pertenece a este usuario.")

    # Solo actualiza los campos si fueron provistos
    if title is not None:
        event.title = title
    if start_date is not None:
        event.start_date = start_date
    if description is not None:
        event.description = description
    if type_id is not None:
        event.type_id = type_id

    db.session.commit()

    return event

def list_events_by_user_service(user_id):
    events = Event.query.filter_by(user=user_id).all()
    if not events:
        raise ValueError("No se encontraron eventos para este usuario.")
    return events

def get_event(id):
    pass