import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.cases import case_bp
from app.extensions import jwt
from app.services.case_service import CaseNotFoundException
from app.models import Case


class CasesApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(case_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='cases-user@example.com')}"
            }

    def test_list_cases_by_user_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.post("/api/cases/byUser", json={})

        self.assertEqual(response.status_code, 401)

    @patch("app.api.cases.list_cases_by_user_service", return_value=[])
    def test_list_cases_by_user_when_jwt_is_present_uses_authenticated_user(
        self,
        list_cases_mock,
    ):
        response = self.client.post(
            "/api/cases/byUser",
            json={"user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        list_cases_mock.assert_called_once_with("cases-user@example.com")

    @patch(
        "app.api.cases.delete_case_service",
        side_effect=CaseNotFoundException("Case with id 7 not found."),
    )
    def test_delete_case_when_case_does_not_exist_returns_not_found(self, _delete_case_mock):
        response = self.client.delete(
            "/api/cases/7",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Case with id 7 not found.")

    @patch("app.api.cases.get_case_by_user_service")
    def test_get_case_when_jwt_is_present_uses_authenticated_user(self, get_case_mock):
        case = Case(rit="RIT-001", name="Caso principal", status="active")
        case.id = 4
        get_case_mock.return_value = case

        response = self.client.get("/api/cases/4", headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["rit"], "RIT-001")
        get_case_mock.assert_called_once_with(4, "cases-user@example.com")
