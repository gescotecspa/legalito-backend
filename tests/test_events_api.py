import unittest
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.events import events_bp
from app.extensions import jwt
from app.services.event_service import EventOwnershipException


class EventsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(events_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='events-user@example.com')}"
            }

    @patch("app.api.events.list_events_by_user_service", return_value=[])
    def test_list_events_by_user_when_jwt_is_present_uses_authenticated_user(
        self,
        list_events_mock,
    ):
        response = self.client.post(
            "/api/events/byuser",
            json={},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        list_events_mock.assert_called_once_with("events-user@example.com")

    @patch(
        "app.api.events.edit_event_service",
        side_effect=EventOwnershipException("El evento no fue encontrado o no pertenece a este usuario."),
    )
    def test_edit_event_when_event_is_not_owned_by_user_returns_not_found(self, _edit_event_mock):
        response = self.client.put(
            "/api/events/edit/1",
            json={"title": "Nuevo titulo"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "El evento no fue encontrado o no pertenece a este usuario.",
        )
