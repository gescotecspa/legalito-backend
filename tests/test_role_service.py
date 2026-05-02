import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.rol import Rol
from app.services.rol_service import list_roles_service


class RoleServiceTests(unittest.TestCase):
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

        db.session.add_all(
            [
                Rol(name="Admin", description="Administrador"),
                Rol(name="Viewer", description="Consulta"),
            ]
        )
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_list_roles_service_returns_registered_roles(self):
        result = list_roles_service()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Admin")
