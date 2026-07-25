import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.models import Client
from app.services.client_service import (
    ClientOwnershipException,
    create_client,
    get_client_for_user,
    list_clients_by_user,
    update_client,
)


class ClientServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

        db.init_app(self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.client_record = Client(owner_user="owner@example.com", name="Cliente Uno")
        self.other_client = Client(owner_user="other@example.com", name="Cliente Dos")
        db.session.add_all([self.client_record, self.other_client])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_client_when_name_is_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_client("owner@example.com", {"name": "  "})

    def test_create_client_persists_owner_from_authenticated_user(self):
        result = create_client(
            "owner@example.com",
            {
                "name": "Nuevo Cliente",
                "email": "cliente@example.com",
                "phone_number": "+56912345678",
            },
        )

        self.assertEqual(result.owner_user, "owner@example.com")
        self.assertEqual(result.name, "Nuevo Cliente")
        self.assertEqual(result.status, "active")

    def test_list_clients_by_user_returns_only_owned_clients(self):
        result = list_clients_by_user("owner@example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Cliente Uno")

    def test_get_client_for_user_when_client_belongs_to_other_user_raises_ownership(self):
        with self.assertRaises(ClientOwnershipException):
            get_client_for_user(self.other_client.id, "owner@example.com")

    def test_update_client_updates_owned_client(self):
        result = update_client(
            self.client_record.id,
            "owner@example.com",
            {"name": "Cliente Actualizado", "notes": "Nota interna"},
        )

        self.assertEqual(result.name, "Cliente Actualizado")
        self.assertEqual(result.notes, "Nota interna")

