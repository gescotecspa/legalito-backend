import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.terms_and_conditions_api import terms_and_conditions_api__bp
from app.extensions import jwt
from app.services.terms_and_conditions_service import (
    TermsAndConditionsNotFoundException,
    TermsUserNotFoundException,
)


class TermsAndConditionsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(terms_and_conditions_api__bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='terms-user@example.com')}"
            }

    @patch("app.api.terms_and_conditions_api.TermsAndConditionsService.accept_terms")
    def test_accept_terms_when_jwt_is_present_uses_authenticated_user(
        self,
        accept_terms_mock,
    ):
        accept_terms_mock.return_value = type(
            "UserStub",
            (),
            {"serialize": lambda self: {"user": "terms-user@example.com"}},
        )()

        response = self.client.put(
            "/api/users/ignored@example.com/accept-terms",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["user"], "terms-user@example.com")
        accept_terms_mock.assert_called_once_with("terms-user@example.com")

    def test_accept_terms_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.put("/api/users/missing@example.com/accept-terms")

        self.assertEqual(response.status_code, 401)

    @patch(
        "app.api.terms_and_conditions_api.TermsAndConditionsService.accept_terms",
        side_effect=TermsUserNotFoundException("User not found."),
    )
    def test_accept_terms_when_user_is_missing_returns_not_found(self, _accept_terms_mock):
        response = self.client.put(
            "/api/users/missing@example.com/accept-terms",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["message"], "User not found.")

    @patch(
        "app.api.terms_and_conditions_api.TermsAndConditionsService.accept_terms",
        side_effect=TermsAndConditionsNotFoundException("No terms available."),
    )
    def test_accept_terms_when_terms_are_missing_returns_conflict(self, _accept_terms_mock):
        response = self.client.put(
            "/api/users/terms-user@example.com/accept-terms",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()["message"], "No terms available.")
