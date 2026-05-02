import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.event import Event
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.models.user import User
from app.services.event_service import (
    EventInvitationDeliveryException,
    EventOwnershipException,
    edit_event_service,
    list_events_by_user_service,
    send_calendar_invitation,
)


class EventServiceTests(unittest.TestCase):
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

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        active_status = Status(code="active", label="Activo")
        default_terms = TermsAndConditions(version="v1", content="Terminos")
        db.session.add_all([active_status, default_terms])
        db.session.commit()

        user = User(
            user="event-user@example.com",
            email="event-user@example.com",
            first_name="Event",
            last_name="User",
            password_hash="hash",
            status_id=active_status.id,
            terms_and_conditions_id=default_terms.id,
        )
        db.session.add(user)
        db.session.commit()

        self.user_id = user.user
        self.event = Event(
            user=self.user_id,
            title="Evento original",
            description="Descripcion",
            start_date=datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc),
        )
        db.session.add(self.event)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    @patch("app.services.event_service.create_and_send_ics_file")
    def test_send_calendar_invitation_when_required_fields_are_missing_raises_value_error(
        self,
        _send_ics_mock,
    ):
        with self.assertRaises(ValueError):
            send_calendar_invitation(
                title="",
                date="01/05/2026",
                time="10:00",
                location="Sala 1",
                recipient_email="user@example.com",
            )

    @patch(
        "app.services.event_service.create_and_send_ics_file",
        return_value="Error al enviar la invitacion: smtp failure",
    )
    def test_send_calendar_invitation_when_delivery_fails_raises_delivery_exception(
        self,
        _send_ics_mock,
    ):
        with self.assertRaises(EventInvitationDeliveryException):
            send_calendar_invitation(
                title="Reunion",
                date="01/05/2026",
                time="10:00",
                location="Sala 1",
                recipient_email="user@example.com",
            )

    def test_list_events_by_user_service_when_user_is_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            list_events_by_user_service(None)

    def test_edit_event_service_when_event_does_not_belong_to_user_raises_ownership_exception(self):
        with self.assertRaises(EventOwnershipException):
            edit_event_service(
                event_id=self.event.id,
                user_id="other-user@example.com",
                title="Editado",
            )

    def test_edit_event_service_when_start_date_is_invalid_raises_value_error(self):
        with self.assertRaises(ValueError):
            edit_event_service(
                event_id=self.event.id,
                user_id=self.user_id,
                start_date="invalid-date",
            )
