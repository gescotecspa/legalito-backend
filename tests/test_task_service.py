import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.models import Case, CaseUser, Client, Task
from app.services.task_service import (
    TaskOwnershipException,
    complete_task,
    create_task,
    get_task_for_user,
    list_tasks_by_user,
    update_task,
)


class TaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

        db.init_app(self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.client_record = Client(owner_user="owner@example.com", name="Cliente Uno")
        self.other_client = Client(owner_user="other@example.com", name="Cliente Dos")
        db.session.add_all([self.client_record, self.other_client])
        db.session.commit()

        self.case = Case(rit="RIT-001", name="Caso principal", status="active")
        self.other_case = Case(rit="RIT-002", name="Caso ajeno", status="active")
        db.session.add_all([self.case, self.other_case])
        db.session.commit()

        db.session.add(CaseUser(case_id=self.case.id, user="owner@example.com"))
        db.session.add(CaseUser(case_id=self.other_case.id, user="other@example.com"))
        db.session.commit()

        self.task = Task(owner_user="owner@example.com", title="Tarea base")
        self.other_task = Task(owner_user="other@example.com", title="Tarea ajena")
        db.session.add_all([self.task, self.other_task])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_task_when_title_is_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_task("owner@example.com", {"title": "  "})

    def test_create_task_with_owned_case_and_client_persists_links(self):
        result = create_task(
            "owner@example.com",
            {
                "title": "Preparar escrito",
                "case_id": self.case.id,
                "client_id": self.client_record.id,
                "priority": "high",
                "due_date": "2026-08-01T10:00:00",
            },
        )

        self.assertEqual(result.owner_user, "owner@example.com")
        self.assertEqual(result.case_id, self.case.id)
        self.assertEqual(result.client_id, self.client_record.id)
        self.assertEqual(result.priority, "high")

    def test_create_task_when_case_is_not_owned_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_task(
                "owner@example.com",
                {"title": "Tarea invalida", "case_id": self.other_case.id},
            )

    def test_create_task_when_client_is_not_owned_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_task(
                "owner@example.com",
                {"title": "Tarea invalida", "client_id": self.other_client.id},
            )

    def test_list_tasks_by_user_filters_by_owner(self):
        result = list_tasks_by_user("owner@example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Tarea base")

    def test_get_task_for_user_when_task_is_not_owned_raises_ownership(self):
        with self.assertRaises(TaskOwnershipException):
            get_task_for_user(self.other_task.id, "owner@example.com")

    def test_update_task_changes_status_and_priority(self):
        result = update_task(
            self.task.id,
            "owner@example.com",
            {"status": "in_progress", "priority": "urgent"},
        )

        self.assertEqual(result.status, "in_progress")
        self.assertEqual(result.priority, "urgent")

    def test_complete_task_marks_completed(self):
        result = complete_task(self.task.id, "owner@example.com")

        self.assertEqual(result.status, "completed")
        self.assertIsNotNone(result.completed_at)

