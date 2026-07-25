from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.task_service import (
    TaskNotFoundException,
    TaskOwnershipException,
    complete_task,
    create_task,
    get_task_for_user,
    list_tasks_by_user,
    update_task,
)


tasks_bp = Blueprint('tasks', __name__)


def _optional_int_arg(name):
    value = request.args.get(name)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"'{name}' must be an integer.") from exc


@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    current_user = get_jwt_identity()

    try:
        case_id = _optional_int_arg('case_id')
        client_id = _optional_int_arg('client_id')
        include_completed = request.args.get('include_completed', 'true').lower() != 'false'
        tasks = list_tasks_by_user(current_user, case_id, client_id, include_completed)
        return jsonify([task.serialize() for task in tasks]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error listing tasks")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    data = request.get_json() or {}

    try:
        task = create_task(current_user, data)
        return jsonify(task.serialize()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error creating task")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user = get_jwt_identity()

    try:
        task = get_task_for_user(task_id, current_user)
        return jsonify(task.serialize()), 200
    except (TaskNotFoundException, TaskOwnershipException) as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error getting task")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def edit_task(task_id):
    current_user = get_jwt_identity()
    data = request.get_json() or {}

    try:
        task = update_task(task_id, current_user, data)
        return jsonify(task.serialize()), 200
    except (TaskNotFoundException, TaskOwnershipException) as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error updating task")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@tasks_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def mark_task_completed(task_id):
    current_user = get_jwt_identity()

    try:
        task = complete_task(task_id, current_user)
        return jsonify(task.serialize()), 200
    except (TaskNotFoundException, TaskOwnershipException) as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error completing task")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
