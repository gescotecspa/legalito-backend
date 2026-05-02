from app import db
from app.models import Assistant
from app.models import Favorite, Parameter

class AssistantAlreadyExistsException(Exception):
    pass


class AssistantNotFoundException(Exception):
    pass


def list_assistants_service():
    return Assistant.query.all()


def get_assistant_service(assistant_id):
    return Assistant.query.filter_by(id=assistant_id).first()


def list_assistants_by_filter_service(type_id, region_id):
    results = (
        db.session.query(
            Assistant.id,
            Assistant.first_name,
            Assistant.last_name,
            Assistant.email,
            Assistant.phone_number,
            Assistant.region_id,
            Assistant.type_id,
            Assistant.created_at,
            Assistant.updated_at,
            Assistant.image_url,
            Parameter.name.label('type_name'), # campo adicional
        )
        .join(Parameter, Assistant.type_id == Parameter.id)
        .filter(
            (Assistant.type_id == type_id) | (type_id == 0),
            (Assistant.region_id == region_id) | (region_id == 0)
        )
        .order_by(Assistant.last_name.asc())
        .all()
    )

    return [dict(row._mapping) for row in results]  


def list_assistants_favorite_service(user):
    if not user:
        raise ValueError("User parameter is required.")

    result = (
        db.session.query(
            Assistant.id,
            Assistant.first_name,
            Assistant.last_name,
            Assistant.email,
            Assistant.phone_number,
            Assistant.region_id,
            Assistant.type_id,
            Assistant.created_at,
            Assistant.updated_at,
            Assistant.image_url,
            Parameter.name.label('type_name')  # Campo adicional
        )
        .join(Parameter, Assistant.type_id == Parameter.id)
        .join(Favorite, Assistant.id == Favorite.assistant_id)
        .filter(Favorite.user == user)
        .order_by(Assistant.last_name.asc())
        .all()
    )
         
    return [dict(row._mapping) for row in result] 


def add_favorite_assistant_service(assistant_id, user):
    if not assistant_id:
        raise ValueError("Assistant parameter is required.")
    if not user:
        raise ValueError("User parameter is required.")

    assistant = db.session.get(Assistant, assistant_id)
    if not assistant:
        raise AssistantNotFoundException("Assistant not found")

    favorite = Favorite.query.filter_by(assistant_id=assistant_id, user=user).first()
    if favorite:
        return True

    new_favorite = Favorite(assistant_id=assistant_id, user=user)

    db.session.add(new_favorite)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True


def delete_favorite_assistant_service(assistant_id, user):
    if not assistant_id:
        raise ValueError("Assistant parameter is required.")
    if not user:
        raise ValueError("User parameter is required.")

    deleted = Favorite.query.filter_by(assistant_id=assistant_id, user=user).delete()
    if not deleted:
        raise AssistantNotFoundException("Favorite assistant not found")

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return False

    return True
