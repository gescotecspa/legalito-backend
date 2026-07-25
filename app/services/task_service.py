from datetime import datetime

from app import db
from app.models import Case, CaseUser, Client, Task


VALID_STATUSES = {"pending", "in_progress", "completed", "cancelled"}
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}


class TaskNotFoundException(Exception):
    pass


class TaskOwnershipException(Exception):
    pass


def _normalize_optional(value):
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def _parse_datetime(value):
    value = _normalize_optional(value)
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("'due_date' must be a valid ISO date.") from exc


def _validate_status(status):
    if status not in VALID_STATUSES:
        raise ValueError(f"'status' must be one of: {', '.join(sorted(VALID_STATUSES))}.")
    return status


def _validate_priority(priority):
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"'priority' must be one of: {', '.join(sorted(VALID_PRIORITIES))}.")
    return priority


def _ensure_case_visible(case_id, user):
    if case_id is None:
        return None

    case = (
        db.session.query(Case)
        .join(CaseUser, Case.id == CaseUser.case_id)
        .filter(Case.id == case_id, CaseUser.user == user)
        .first()
    )
    if not case:
        raise ValueError("Case not found or does not belong to this user.")
    return case


def _ensure_client_visible(client_id, user):
    if client_id is None:
        return None

    client = db.session.get(Client, client_id)
    if not client or client.owner_user != user:
        raise ValueError("Client not found or does not belong to this user.")
    return client


def _get_int_or_none(data, field):
    value = data.get(field)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"'{field}' must be an integer.") from exc


def create_task(user, data):
    if not user:
        raise ValueError("User parameter is required.")

    title = _normalize_optional(data.get('title'))
    if not title:
        raise ValueError("'title' is required.")

    case_id = _get_int_or_none(data, 'case_id')
    client_id = _get_int_or_none(data, 'client_id')
    _ensure_case_visible(case_id, user)
    _ensure_client_visible(client_id, user)

    status = _validate_status(_normalize_optional(data.get('status')) or 'pending')
    priority = _validate_priority(_normalize_optional(data.get('priority')) or 'normal')

    task = Task(
        owner_user=user,
        title=title,
        description=_normalize_optional(data.get('description')),
        status=status,
        priority=priority,
        due_date=_parse_datetime(data.get('due_date')),
        assignee_user=_normalize_optional(data.get('assignee_user')),
        case_id=case_id,
        client_id=client_id,
        completed_at=datetime.utcnow() if status == 'completed' else None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(task)
    db.session.commit()
    return task


def list_tasks_by_user(user, case_id=None, client_id=None, include_completed=True):
    if not user:
        raise ValueError("User parameter is required.")

    query = Task.query.filter_by(owner_user=user)
    if case_id is not None:
        query = query.filter(Task.case_id == case_id)
    if client_id is not None:
        query = query.filter(Task.client_id == client_id)
    if not include_completed:
        query = query.filter(Task.status != 'completed')

    return query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc()).all()


def get_task_for_user(task_id, user):
    if not user:
        raise ValueError("User parameter is required.")

    task = db.session.get(Task, task_id)
    if not task:
        raise TaskNotFoundException(f"Task with id {task_id} not found.")
    if task.owner_user != user:
        raise TaskOwnershipException("Task not found or does not belong to this user.")
    return task


def update_task(task_id, user, data):
    task = get_task_for_user(task_id, user)

    if 'title' in data:
        title = _normalize_optional(data.get('title'))
        if not title:
            raise ValueError("'title' is required.")
        task.title = title

    if 'description' in data:
        task.description = _normalize_optional(data.get('description'))
    if 'priority' in data:
        task.priority = _validate_priority(_normalize_optional(data.get('priority')) or 'normal')
    if 'status' in data:
        new_status = _validate_status(_normalize_optional(data.get('status')) or 'pending')
        task.status = new_status
        task.completed_at = datetime.utcnow() if new_status == 'completed' else None
    if 'due_date' in data:
        task.due_date = _parse_datetime(data.get('due_date'))
    if 'assignee_user' in data:
        task.assignee_user = _normalize_optional(data.get('assignee_user'))
    if 'case_id' in data:
        case_id = _get_int_or_none(data, 'case_id')
        _ensure_case_visible(case_id, user)
        task.case_id = case_id
    if 'client_id' in data:
        client_id = _get_int_or_none(data, 'client_id')
        _ensure_client_visible(client_id, user)
        task.client_id = client_id

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return task


def complete_task(task_id, user):
    return update_task(task_id, user, {'status': 'completed'})
