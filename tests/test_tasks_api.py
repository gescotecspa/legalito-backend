import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.tasks import tasks_bp
from app.extensions import jwt
from app.models import Task
from app.services.task_service import TaskOwnershipException


class TasksApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(tasks_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='tasks-user@example.com')}"
            }

    def test_list_tasks_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.get("/api/tasks")

        self.assertEqual(response.status_code, 401)

    @patch("app.api.tasks.list_tasks_by_user", return_value=[])
    def test_list_tasks_when_jwt_is_present_uses_authenticated_user(self, list_tasks_mock):
        response = self.client.get("/api/tasks?case_id=7", headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        list_tasks_mock.assert_called_once_with("tasks-user@example.com", 7, None, True)

    @patch("app.api.tasks.create_task")
    def test_create_task_when_payload_is_valid_returns_created(self, create_task_mock):
        created_task = Task(owner_user="tasks-user@example.com", title="Nueva tarea")
        created_task.id = 5
        create_task_mock.return_value = created_task

        response = self.client.post(
            "/api/tasks",
            json={"title": "Nueva tarea", "owner_user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["title"], "Nueva tarea")
        create_task_mock.assert_called_once_with(
            "tasks-user@example.com",
            {"title": "Nueva tarea", "owner_user": "forged@example.com"},
        )

    @patch(
        "app.api.tasks.get_task_for_user",
        side_effect=TaskOwnershipException("Task not found or does not belong to this user."),
    )
    def test_get_task_when_task_is_not_owned_returns_not_found(self, _get_task_mock):
        response = self.client.get("/api/tasks/8", headers=self.auth_headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Task not found or does not belong to this user.",
        )

    @patch("app.api.tasks.complete_task")
    def test_complete_task_when_jwt_is_present_uses_authenticated_user(self, complete_task_mock):
        task = Task(owner_user="tasks-user@example.com", title="Tarea")
        task.id = 9
        task.status = "completed"
        complete_task_mock.return_value = task

        response = self.client.post("/api/tasks/9/complete", headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "completed")
        complete_task_mock.assert_called_once_with(9, "tasks-user@example.com")

