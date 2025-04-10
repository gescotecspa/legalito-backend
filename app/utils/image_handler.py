import os
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime, timezone
import re

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

BASE_UPLOAD_FOLDER = 'static/uploads/users'

def save_base64_image(base64_string, username, old_image_url=None):
    safe_username = sanitize_filename(username)
    user_folder = os.path.join(BASE_UPLOAD_FOLDER, safe_username)
    os.makedirs(user_folder, exist_ok=True)

    # Eliminar imagen anterior si existe
    if old_image_url:
        old_path = old_image_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    # Decodificar imagen base64
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))

    # Comprimir imagen
    image = image.convert("RGB")
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}.jpg"
    full_path = os.path.join(user_folder, filename)
    image.save(full_path, format='JPEG', quality=70)

    # Devolver URL relativa
    return f"/{user_folder}/{filename}"
