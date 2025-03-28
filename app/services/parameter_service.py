from app import db
from app.models import Parameter
from datetime import datetime

class ParameterAlreadyExistsException(Exception):
    pass

class ParameterNotFoundException(Exception):
    pass

def list_parameters():
    return Parameter.query.all()

def list_parameters_by_parent(id):
    return Parameter.query.filter_by(parent_id = id).order_by(Parameter.name.asc()).all()