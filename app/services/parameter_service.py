from app.models import Parameter

class ParameterAlreadyExistsException(Exception):
    pass

class ParameterNotFoundException(Exception):
    pass


def list_parameters_service():
    return Parameter.query.all()


def list_parameters_by_parent_service(parent_id):
    return Parameter.query.filter_by(parent_id=parent_id).order_by(Parameter.name.asc()).all()


def list_parameters():
    return list_parameters_service()


def list_parameters_by_parent(parent_id):
    return list_parameters_by_parent_service(parent_id)
