from app import db
from app.models import Assistant
from app.models import Favorite
from app.models import Parameter

class AssistantAlreadyExistsException(Exception):
    pass

class AssistantNotFoundException(Exception):
    pass

def list_assistants():
    result = Assistant.query.all()
    return result

def get_assistant(_id):
    assistant = Assistant.query.filter_by(id=_id).first()
    return assistant

def list_assistants_by_filter(typeId,regionId):
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
            (Assistant.type_id == typeId) | (typeId == 0),
            (Assistant.region_id == regionId) | (regionId == 0)
        )
        .order_by(Assistant.last_name.asc())
        .all()
    )

    # Convertir cada Row a diccionario
    return [dict(row._mapping) for row in results]  

def list_assistants_favorite(user):
    result = (
        db.session.query(Assistant)
        .join(Favorite, Assistant.id == Favorite.assistant_id)
        .filter(Favorite.user == user)
        .order_by(Assistant.last_name.asc())
        .all()
    )
    
    return result

def add_favorite_assitant(assistantId,user):

    new_favorite = Favorite(
        assistant_id = assistantId,
        user = user
    )

    db.session.add(new_favorite)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True

def delete_favorite_assistant(assistantId,user):

    Favorite.query.filter_by(assistant_id=assistantId, user=user).delete()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True