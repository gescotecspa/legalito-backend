from app import db
from app.models import User

class UserAlreadyExistsException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

def list_users():
    return User.query.all()