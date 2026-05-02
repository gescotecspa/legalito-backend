import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.folios import folios_bp
from app.extensions import jwt
from app.services.folio_service import FolioNotFoundException


class FoliosApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(folios_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='folios-user@example.com')}"
            }

    def test_create_folio_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.post("/api/folios", json={"case_id": 1, "folio_number": "F-001"})

        self.assertEqual(response.status_code, 401)

    @patch(
        "app.api.folios.create_folio_service",
        return_value=SimpleNamespace(
            serialize=lambda: {
                "id": 1,
                "case_id": 1,
                "folio_number": "F-001",
                "description": "Descripcion",
                "created_at": "2026-05-01T10:00:00",
            }
        ),
    )
    def test_create_folio_when_data_is_valid_returns_created(self, create_folio_mock):
        response = self.client.post(
            "/api/folios",
            json={"case_id": 1, "folio_number": "F-001"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["folio"]["folio_number"], "F-001")
        create_folio_mock.assert_called_once_with({"case_id": 1, "folio_number": "F-001"})

    @patch(
        "app.api.folios.list_folios_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 1, "folio_number": "F-001"})],
    )
    def test_list_folios_returns_serialized_folios(self, list_folios_mock):
        response = self.client.get(
            "/api/folios",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], 1)
        list_folios_mock.assert_called_once_with()

    @patch(
        "app.api.folios.delete_folio_service",
        side_effect=FolioNotFoundException("Folio with id 7 not found."),
    )
    def test_delete_folio_when_folio_does_not_exist_returns_not_found(self, _delete_folio_mock):
        response = self.client.delete(
            "/api/folios/7",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Folio with id 7 not found.")
