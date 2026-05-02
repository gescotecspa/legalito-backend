import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask

from app.api.image import image_bp


class ImageApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        self.app.register_blueprint(image_bp, url_prefix="/api")
        self.client = self.app.test_client()

    def test_serve_image_when_file_exists_returns_file_contents(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = Path(temp_dir)
            image_path = upload_dir / "avatar.jpg"
            image_path.write_bytes(b"fake-image-content")

            with patch("app.api.image.get_user_upload_folder", return_value=upload_dir):
                response = self.client.get("/api/static/uploads/users/avatar.jpg")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"fake-image-content")
        self.assertEqual(response.mimetype, "image/jpeg")

    def test_serve_image_when_file_does_not_exist_returns_not_found(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = Path(temp_dir)

            with patch("app.api.image.get_user_upload_folder", return_value=upload_dir):
                response = self.client.get("/api/static/uploads/users/missing.jpg")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Archivo no encontrado"})

    def test_serve_image_when_path_traversal_is_attempted_returns_not_found(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            upload_dir = Path(temp_dir)
            outside_file = upload_dir.parent / "secret.txt"
            outside_file.write_text("top-secret")

            with patch("app.api.image.get_user_upload_folder", return_value=upload_dir):
                response = self.client.get("/api/static/uploads/users/../secret.txt")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Archivo no encontrado"})

