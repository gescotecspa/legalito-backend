from app import db
from app.models import Rol

class RolAlreadyExistsException(Exception):
    pass

class RolNotFoundException(Exception):
    pass

def list_roles():
    return Rol.query.all()