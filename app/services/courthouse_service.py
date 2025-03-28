from app import db
from app.models import Courthouse

class CourthouseAlreadyExistsException(Exception):
    pass

class CourthouseNotFoundException(Exception):
    pass

def list_courthouses():
    return Courthouse.query.all()