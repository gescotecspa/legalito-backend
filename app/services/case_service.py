from app import db
from app.models import Case, CaseUser
from datetime import datetime

class CaseAlreadyExistsException(Exception):
    pass

class CaseNotFoundException(Exception):
    pass

def create_case(data):
    rit = data.get('rit')
    name = data.get('name')
    status = data.get('status', 'active')

    if not rit or not name:
        raise ValueError("'rit' and 'name' are required.")

    existing_case = Case.query.filter_by(rit=rit).first()
    if existing_case:
        raise CaseAlreadyExistsException(f"Case with RIT {rit} already exists.")

    new_case = Case(
        rit=rit,
        name=name,
        status=status,
        created_at=datetime.utcnow()
    )

    db.session.add(new_case)
    db.session.commit()

    return new_case

def list_cases():
    return Case.query.all()

def delete_case(case_id):
    case = Case.query.get(case_id)
    if not case:
        raise CaseNotFoundException(f"Case with id {case_id} not found.")

    db.session.delete(case)
    db.session.commit()

def list_cases_by_user(user):
    result = (
        db.session.query(Case)
        .join(CaseUser, Case.id == CaseUser.case_id)
        .filter(CaseUser.user == user)
        .order_by(Case.name.asc())
        .all()
    )
    return result