import re
from datetime import datetime

def extract_event_info(email_subject, email_body):
    """
    Función básica para extraer fecha, hora y lugar desde un correo.
    Se puede mejorar usando NLP más adelante.
    """
    # Buscar fechas en formato dd/mm/yyyy o dd-mm-yyyy
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})', email_subject + ' ' + email_body)
    event_date = date_match.group(1) if date_match else None

    # Buscar hora (ejemplo: 14:30)
    time_match = re.search(r'(\d{1,2}:\d{2})', email_subject + ' ' + email_body)
    event_time = time_match.group(1) if time_match else None

    # Buscar posible lugar (simplificado, busca palabras clave)
    location_match = re.search(r'Lugar: (.*?)(\n|$)', email_body, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else "Sin especificar"

    # Título del evento será el asunto si no hay otra indicación
    title = email_subject.strip()

    return {
        "title": title,
        "date": event_date,
        "time": event_time,
        "location": location
    }