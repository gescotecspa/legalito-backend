import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.email_accounts import email_accounts_bp
from app.extensions import jwt
from app.services.email_account_service import EmailAccountOwnershipException


class EmailAccountsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(email_accounts_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='owner@example.com')}"
            }

    @patch(
        "app.api.email_accounts.update_email_account",
        side_effect=EmailAccountOwnershipException("Account not found or does not belong to this user"),
    )
    def test_update_account_when_account_does_not_belong_to_user_returns_not_found(
        self,
        _update_account_mock,
    ):
        response = self.client.put(
            "/api/email-accounts/1",
            json={"provider": "new-provider"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Account not found or does not belong to this user",
        )

    @patch(
        "app.api.email_accounts.update_email_account",
        side_effect=ValueError("Ya existe una cuenta utilizando el correo 'used@example.com'."),
    )
    def test_update_account_when_email_is_already_used_returns_bad_request(
        self,
        _update_account_mock,
    ):
        response = self.client.put(
            "/api/email-accounts/1",
            json={"email_address": "used@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Ya existe una cuenta utilizando el correo 'used@example.com'.",
        )

    @patch(
        "app.api.email_accounts.get_email_account_by_id_for_user",
        side_effect=EmailAccountOwnershipException("Account not found or does not belong to this user"),
    )
    def test_get_account_by_id_when_account_does_not_belong_to_user_returns_not_found(
        self,
        get_account_mock,
    ):
        response = self.client.get(
            "/api/email-accounts/1",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Account not found or does not belong to this user",
        )
        get_account_mock.assert_called_once_with(1, "owner@example.com")
