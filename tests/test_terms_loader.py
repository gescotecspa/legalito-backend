import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.terms_and_conditions import TermsAndConditions
from app.utils.termsLoader import (
    DEFAULT_TERMS_CONTENT,
    DEFAULT_TERMS_VERSION,
    LEGACY_DEFAULT_CONTENT,
    initialize_terms_and_conditions,
)


class TermsLoaderTests(unittest.TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_initialize_terms_and_conditions_creates_richer_default_seed(self):
        terms = initialize_terms_and_conditions()

        self.assertEqual(terms.version, DEFAULT_TERMS_VERSION)
        self.assertEqual(terms.content, DEFAULT_TERMS_CONTENT)
        self.assertIn("Legalito - Terminos y Condiciones", terms.content)

    def test_initialize_terms_and_conditions_upgrades_legacy_placeholder_content(self):
        legacy_terms = TermsAndConditions(
            version=DEFAULT_TERMS_VERSION,
            content=LEGACY_DEFAULT_CONTENT,
        )
        db.session.add(legacy_terms)
        db.session.commit()

        terms = initialize_terms_and_conditions()

        self.assertEqual(terms.id, legacy_terms.id)
        self.assertEqual(terms.content, DEFAULT_TERMS_CONTENT)

    def test_initialize_terms_and_conditions_preserves_existing_custom_content(self):
        custom_terms = TermsAndConditions(
            version=DEFAULT_TERMS_VERSION,
            content="Contenido formal publicado por el equipo legal.",
        )
        db.session.add(custom_terms)
        db.session.commit()

        terms = initialize_terms_and_conditions()

        self.assertEqual(terms.id, custom_terms.id)
        self.assertEqual(
            terms.content,
            "Contenido formal publicado por el equipo legal.",
        )
