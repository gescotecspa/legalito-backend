from app import db
from app.models.terms_and_conditions import TermsAndConditions

DEFAULT_TERMS_VERSION = "v1"
LEGACY_DEFAULT_CONTENT = (
    "Terminos y condiciones iniciales para entornos locales o no productivos."
)
DEFAULT_TERMS_CONTENT = """
Legalito - Terminos y Condiciones

Version: v1

1. Objeto
Estos terminos regulan el uso inicial de la plataforma Legalito en entornos
locales, de desarrollo y QA.

2. Uso de la plataforma
La persona usuaria declara que utilizara la aplicacion de forma licita y de
acuerdo con las funcionalidades habilitadas por el sistema.

3. Cuenta de usuario
Cada cuenta es personal. La persona usuaria es responsable de resguardar sus
credenciales y de mantener actualizada la informacion basica de su perfil.

4. Comunicaciones
La plataforma puede enviar comunicaciones operativas o transaccionales
relacionadas con autenticacion, recuperacion de acceso y funcionamiento del
servicio.

5. Datos y privacidad
La informacion registrada en la plataforma debe ser tratada conforme a las
politicas vigentes del proyecto y a la normativa aplicable que corresponda al
entorno de uso.

6. Vigencia
Esta version semilla existe para permitir el funcionamiento del sistema en
entornos controlados. Puede ser reemplazada por una version formal publicada
desde la administracion de terminos.
""".strip()


def initialize_terms_and_conditions():
    existing_terms = TermsAndConditions.query.filter_by(version=DEFAULT_TERMS_VERSION).first()
    if existing_terms:
        if not existing_terms.content or existing_terms.content == LEGACY_DEFAULT_CONTENT:
            existing_terms.content = DEFAULT_TERMS_CONTENT
            db.session.commit()
        return existing_terms

    terms = TermsAndConditions(
        version=DEFAULT_TERMS_VERSION,
        content=DEFAULT_TERMS_CONTENT,
    )
    db.session.add(terms)
    db.session.commit()
    return terms
