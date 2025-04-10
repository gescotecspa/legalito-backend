from flask import Blueprint, Response, jsonify, current_app
import os

image_bp = Blueprint('image', __name__)

@image_bp.route('/static/uploads/users/<path:filename>')
def serve_image(filename):
    upload_folder = os.path.abspath(os.path.join(current_app.root_path, '..', 'static', 'uploads', 'users'))
    file_path = os.path.join(upload_folder, *filename.split('/'))

    if not os.path.exists(file_path):
        return jsonify({"error": "Archivo no encontrado"}), 404

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return Response(data, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500