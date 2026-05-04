import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app import db
from app.api.events import events_bp
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.event import Event
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.models.user import User
from app.services.event_service import EventOwnershipException


class EventsApiTests(unittest.TestCase):
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
        bcrypt.init_app(self.app)
        jwt.init_app(self.app)
        self.app.register_blueprint(events_bp, url_prefix="/api")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            active_status = Status(code="active", label="Activo")
            default_terms = TermsAndConditions(version="v1", content="Terminos")
            db.session.add_all([active_status, default_terms])
            db.session.commit()

            owner = User(
                user="events-user@example.com",
                email="events-user@example.com",
                first_name="Event",
                last_name="Owner",
                password_hash="hash",
                status_id=active_status.id,
                terms_and_conditions_id=default_terms.id,
            )
            other = User(
                user="other-user@example.com",
                email="other-user@example.com",
                first_name="Other",
                last_name="User",
                password_hash="hash",
                status_id=active_status.id,
                terms_and_conditions_id=default_terms.id,
            )
            db.session.add_all([owner, other])
            db.session.commit()

            event = Event(
                user=owner.user,
                title="Evento privado",
                description="Solo del owner",
                start_date=datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc),
            )
            db.session.add(event)
            db.session.commit()
            self.event_id = event.id
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='events-user@example.com')}"
            }
            self.other_auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='other-user@example.com')}"
            }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

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

    def test_get_event_by_id_when_event_belongs_to_authenticated_user_returns_event(self):
        response = self.client.get(
            f"/api/events/{self.event_id}",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], self.event_id)
        self.assertEqual(response.get_json()["user"], "events-user@example.com")

    def test_get_event_by_id_when_event_does_not_belong_to_authenticated_user_returns_not_found(self):
        response = self.client.get(
            f"/api/events/{self.event_id}",
            headers=self.other_auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            f"Evento con ID {self.event_id} no encontrado para el usuario autenticado.",
        )
