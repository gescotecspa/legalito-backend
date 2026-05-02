import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.mails import mails_bp
from app.extensions import jwt


class MailsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(mails_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='mails-user@example.com')}"
            }

    def test_read_mails_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.post("/api/read-mails", json={"email": "account@example.com"})

        self.assertEqual(response.status_code, 401)

    @patch(
        "app.api.mails.read_mails_for_user",
        return_value={"email_address": "account@example.com", "extracted_events": []},
    )
    def test_read_mails_when_jwt_is_present_uses_authenticated_user(
        self,
        read_mails_mock,
    ):
        response = self.client.post(
            "/api/read-mails",
            json={"email": "account@example.com", "user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email_address"], "account@example.com")
        read_mails_mock.assert_called_once_with(
            "account@example.com",
            "mails-user@example.com",
        )
