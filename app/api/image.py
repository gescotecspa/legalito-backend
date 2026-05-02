import mimetypes
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify

image_bp = Blueprint('image', __name__)


def get_user_upload_folder():
    return (Path(current_app.root_path).resolve().parent / 'static' / 'uploads' / 'users').resolve()


def resolve_user_upload_path(filename):
    upload_folder = get_user_upload_folder().resolve()
    requested_path = (upload_folder / filename).resolve()

    try:
        requested_path.relative_to(upload_folder)
    except ValueError:
        return None

    return requested_path


@image_bp.route('/static/uploads/users/<path:filename>')
def serve_image(filename):
    file_path = resolve_user_upload_path(filename)

    if file_path is None or not file_path.exists() or not file_path.is_file():
        return jsonify({"error": "Archivo no encontrado"}), 404

    try:
        with file_path.open('rb') as f:
            data = f.read()
        mimetype = mimetypes.guess_type(file_path.name)[0] or 'application/octet-stream'
        return Response(data, mimetype=mimetype)
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
