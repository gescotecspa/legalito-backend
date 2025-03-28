from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import bcrypt, jwt

# Inicializamos SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializamos la base de datos
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importar y registrar blueprints después de que la app esté configurada
    from .api import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
