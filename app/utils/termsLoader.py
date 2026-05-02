from app import db
from app.models.terms_and_conditions import TermsAndConditions


def initialize_terms_and_conditions():
    default_version = "v1"
    default_content = (
        "Terminos y condiciones iniciales para entornos locales o no productivos."
    )

    existing_terms = TermsAndConditions.query.filter_by(version=default_version).first()
    if existing_terms:
        return existing_terms

    terms = TermsAndConditions(
        version=default_version,
        content=default_content,
    )
    db.session.add(terms)
    db.session.commit()
    return terms
