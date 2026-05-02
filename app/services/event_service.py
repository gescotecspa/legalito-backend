from datetime import datetime
from app.models import Event, User, Parameter
from app import db
from sqlalchemy import asc
from app.integrations.smtp_calendar import create_and_send_ics_file

class EventNotFoundException(Exception):
    pass


class EventInvitationDeliveryException(Exception):
    pass


class EventOwnershipException(Exception):
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
        raise EventOwnershipException("El evento no fue encontrado o no pertenece a este usuario.")

    # Solo actualiza los campos si fueron provistos
    if title is not None:
        event.title = title
    if start_date is not None:
        try:
            event.start_date = datetime.fromisoformat(start_date)
        except ValueError:
            raise ValueError("Formato de fecha inválido")
    if description is not None:
        event.description = description
    if type_id is not None:
        parameter = Parameter.query.get(type_id)
        if not parameter:
            raise ValueError("Tipo de evento no encontrado")
        event.type_id = type_id

    db.session.commit()

    return event

def list_events_by_user_service(user_id):
    if not user_id:
        raise ValueError("User parameter is required")
    events = Event.query.filter_by(user=user_id).order_by(asc(Event.start_date)).all()
    return events

def get_event_by_id_service(event_id):
    event = Event.query.get(event_id)
    
    if event is None:
        raise EventNotFoundException(f"Evento con ID {event_id} no encontrado.")
    
    return event


def send_calendar_invitation(title, date, time, location, recipient_email, description=""):
    required_fields = {
        "title": title,
        "date": date,
        "time": time,
        "recipient_email": recipient_email,
    }
    missing_fields = [field for field, value in required_fields.items() if not value]
    if missing_fields:
        raise ValueError(f"Faltan datos requeridos: {', '.join(missing_fields)}")

    result = create_and_send_ics_file(
        title=title,
        date_str=date,
        time_str=time,
        location=location,
        recipient_email=recipient_email,
        description=description,
    )

    if isinstance(result, str) and result.lower().startswith("error al enviar"):
        raise EventInvitationDeliveryException(result)

    return result
