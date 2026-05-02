from app.models import Courthouse

class CourthouseAlreadyExistsException(Exception):
    pass

class CourthouseNotFoundException(Exception):
    pass


def list_courthouses_service():
    return Courthouse.query.all()


def list_courthouses():
    return list_courthouses_service()
