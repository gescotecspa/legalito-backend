from app.models import Rol

class RolAlreadyExistsException(Exception):
    pass

class RolNotFoundException(Exception):
    pass


def list_roles_service():
    return Rol.query.all()


def list_roles():
    return list_roles_service()
