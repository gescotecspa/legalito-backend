import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.parameter import Parameter
from app.services.parameter_service import (
    list_parameters_by_parent_service,
    list_parameters_service,
)


class ParameterServiceTests(unittest.TestCase):
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

        parent = Parameter(name="Parent")
        db.session.add(parent)
        db.session.commit()

        db.session.add_all(
            [
                Parameter(parent_id=parent.id, name="Bravo"),
                Parameter(parent_id=parent.id, name="Alpha"),
                Parameter(parent_id=999, name="Other"),
            ]
        )
        db.session.commit()
        self.parent_id = parent.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_parameters_service_returns_all_parameters(self):
        result = list_parameters_service()

        self.assertEqual(len(result), 4)

    def test_list_parameters_by_parent_service_returns_sorted_parameters(self):
        result = list_parameters_by_parent_service(self.parent_id)

        self.assertEqual([item.name for item in result], ["Alpha", "Bravo"])
