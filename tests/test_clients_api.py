import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.clients import clients_bp
from app.extensions import jwt
from app.models import Client
from app.services.client_service import ClientOwnershipException


class ClientsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(clients_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='owner@example.com')}"
            }

    def test_list_clients_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.get("/api/clients")

        self.assertEqual(response.status_code, 401)

    @patch("app.api.clients.list_clients_by_user", return_value=[])
    def test_list_clients_when_jwt_is_present_uses_authenticated_user(self, list_clients_mock):
        response = self.client.get("/api/clients", headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        list_clients_mock.assert_called_once_with("owner@example.com")

    @patch("app.api.clients.create_client")
    def test_create_client_when_payload_is_valid_returns_created(self, create_client_mock):
        created_client = Client(owner_user="owner@example.com", name="Cliente Nuevo")
        created_client.id = 7
        create_client_mock.return_value = created_client

        response = self.client.post(
            "/api/clients",
            json={"name": "Cliente Nuevo", "owner_user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "Cliente Nuevo")
        create_client_mock.assert_called_once_with(
            "owner@example.com",
            {"name": "Cliente Nuevo", "owner_user": "forged@example.com"},
        )

    @patch(
        "app.api.clients.get_client_for_user",
        side_effect=ClientOwnershipException("Client not found or does not belong to this user."),
    )
    def test_get_client_when_client_is_not_owned_returns_not_found(self, _get_client_mock):
        response = self.client.get("/api/clients/8", headers=self.auth_headers)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Client not found or does not belong to this user.",
        )
