import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.case import Case
from app.models.case_user import CaseUser
from app.models.client import Client
from app.services.case_service import (
    CaseNotFoundException,
    CaseOwnershipException,
    delete_case_service,
    get_case_by_user_service,
    list_cases_by_user_service,
)


class CaseServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

        db.init_app(self.app)
        jwt.init_app(self.app)

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.client_record = Client(owner_user="owner@example.com", name="Cliente Uno")
        db.session.add(self.client_record)
        db.session.commit()

        self.case = Case(
            rit="RIT-001",
            name="Caso principal",
            status="active",
            client_id=self.client_record.id,
        )
        self.other_case = Case(rit="RIT-002", name="Caso secundario", status="active")
        db.session.add_all([self.case, self.other_case])
        db.session.commit()

        db.session.add(CaseUser(case_id=self.case.id, user="owner@example.com"))
        db.session.add(CaseUser(case_id=self.other_case.id, user="other@example.com"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_cases_by_user_service_when_user_is_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            list_cases_by_user_service(None)

    def test_list_cases_by_user_service_returns_only_cases_for_user(self):
        result = list_cases_by_user_service("owner@example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].rit, "RIT-001")

    def test_delete_case_service_when_case_does_not_exist_raises_not_found(self):
        with self.assertRaises(CaseNotFoundException):
            delete_case_service(999)

    def test_get_case_by_user_service_returns_owned_case_with_client(self):
        result = get_case_by_user_service(self.case.id, "owner@example.com")

        self.assertEqual(result.rit, "RIT-001")
        self.assertEqual(result.client.name, "Cliente Uno")

    def test_get_case_by_user_service_when_case_is_not_owned_raises_ownership(self):
        with self.assertRaises(CaseOwnershipException):
            get_case_by_user_service(self.other_case.id, "owner@example.com")
