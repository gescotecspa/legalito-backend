import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.assistant import Assistant
from app.models.favorite import Favorite
from app.models.parameter import Parameter
from app.services.assistant_service import (
    AssistantNotFoundException,
    add_favorite_assistant_service,
    delete_favorite_assistant_service,
    list_assistants_by_filter_service,
    list_assistants_favorite_service,
)


class AssistantServiceTests(unittest.TestCase):
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
        jwt.init_app(self.app)

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        assistant_type = Parameter(name="Abogado")
        db.session.add(assistant_type)
        db.session.commit()

        self.assistant = Assistant(
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.com",
            phone_number="123456",
            type_id=assistant_type.id,
            region_id=1,
        )
        db.session.add(self.assistant)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_assistants_favorite_service_when_user_is_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            list_assistants_favorite_service(None)

    def test_add_favorite_assistant_service_when_assistant_is_missing_raises_not_found(self):
        with self.assertRaises(AssistantNotFoundException):
            add_favorite_assistant_service(999, "user@example.com")

    def test_add_favorite_assistant_service_creates_favorite(self):
        result = add_favorite_assistant_service(self.assistant.id, "user@example.com")

        self.assertTrue(result)
        favorite = Favorite.query.filter_by(
            assistant_id=self.assistant.id,
            user="user@example.com",
        ).first()
        self.assertIsNotNone(favorite)

    def test_list_assistants_favorite_service_returns_favorite_assistants_for_user(self):
        db.session.add(Favorite(assistant_id=self.assistant.id, user="user@example.com"))
        db.session.commit()

        result = list_assistants_favorite_service("user@example.com")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.assistant.id)

    def test_list_assistants_by_filter_service_returns_matching_assistants(self):
        result = list_assistants_by_filter_service(self.assistant.type_id, self.assistant.region_id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], self.assistant.id)

    def test_delete_favorite_assistant_service_when_favorite_does_not_exist_raises_not_found(self):
        with self.assertRaises(AssistantNotFoundException):
            delete_favorite_assistant_service(self.assistant.id, "user@example.com")

    def test_delete_favorite_assistant_service_removes_existing_favorite(self):
        db.session.add(Favorite(assistant_id=self.assistant.id, user="user@example.com"))
        db.session.commit()

        result = delete_favorite_assistant_service(self.assistant.id, "user@example.com")

        self.assertTrue(result)
        favorite = Favorite.query.filter_by(
            assistant_id=self.assistant.id,
            user="user@example.com",
        ).first()
        self.assertIsNone(favorite)
