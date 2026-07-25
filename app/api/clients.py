from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.client_service import (
    ClientNotFoundException,
    ClientOwnershipException,
    create_client,
    get_client_for_user,
    list_clients_by_user,
    update_client,
)


clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients', methods=['GET'])
@jwt_required()
def list_clients():
    current_user = get_jwt_identity()

    try:
        clients = list_clients_by_user(current_user)
        return jsonify([client.serialize() for client in clients]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error listing clients")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@clients_bp.route('/clients', methods=['POST'])
@jwt_required()
def add_client():
    current_user = get_jwt_identity()
    data = request.get_json() or {}

    try:
        client = create_client(current_user, data)
        return jsonify(client.serialize()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error creating client")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    current_user = get_jwt_identity()

    try:
        client = get_client_for_user(client_id, current_user)
        return jsonify(client.serialize(include_cases=True)), 200
    except (ClientNotFoundException, ClientOwnershipException) as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error getting client")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
@jwt_required()
def edit_client(client_id):
    current_user = get_jwt_identity()
    data = request.get_json() or {}

    try:
        client = update_client(client_id, current_user, data)
        return jsonify(client.serialize()), 200
    except (ClientNotFoundException, ClientOwnershipException) as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.exception("Unexpected error updating client")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
