import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.courthouse import Courthouse
from app.services.courthouse_service import list_courthouses_service


class CourthouseServiceTests(unittest.TestCase):
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

        db.session.add(
            Courthouse(
                name="Juzgado Civil",
                type_id=1,
                address="Calle 123",
                phone_number="1234567",
                email="court@example.com",
                website="https://court.example.com",
                status="active",
            )
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_courthouses_service_returns_registered_courthouses(self):
        result = list_courthouses_service()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Juzgado Civil")
