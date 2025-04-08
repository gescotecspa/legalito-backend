from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.services.email_account_service import add_email_account, get_email_account_by_id, get_email_accounts_by_user,list_email_accounts,delete_email_accounts, toggle_email_account_status, update_email_account

email_accounts_bp = Blueprint('email_accounts', __name__)

@email_accounts_bp.route('/email-accounts', methods=['POST'])
@jwt_required()
def add():
    current_user = get_jwt_identity()
    data = request.json
    data['user'] = current_user
    try:
        account = add_email_account(data)
        return jsonify({"message": "Account successfully added", "account": account.serialize()}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error: " + str(e)}), 500

@email_accounts_bp.route('/email-accounts', methods=['GET'])
@jwt_required()
def list_email_acc():
    accounts = list_email_accounts()
    return jsonify([a.serialize() for a in accounts])

@email_accounts_bp.route('/email-accounts/byuser', methods=['GET'])
@jwt_required()
def get_email_by_user():
    current_user = get_jwt_identity()
    # print("usuario desde jwt",current_user)
    accounts = get_email_accounts_by_user(current_user)
    # Siempre devolvé una lista, aunque esté vacía
    return jsonify([a.serialize() for a in accounts]), 200

@email_accounts_bp.route('/email-accounts', methods=['DELETE'])
@jwt_required()
def delete():
    data = request.get_json()
    email = data.get('email')
    user = get_jwt_identity()

    try:
        success = delete_email_accounts(email, user)

        if not success:
            return jsonify({"error": "Account not found or could not be deleted"}), 404

        return jsonify({"message": "Account successfully deleted"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@email_accounts_bp.route('/email-accounts', methods=['PUT'])
@jwt_required()
def update():
    abort(501)
    
@email_accounts_bp.route('/email-accounts/toggle-status', methods=['PUT'])
@jwt_required()
def toggle_status():
    data = request.get_json()
    email = data.get('email')
    user = get_jwt_identity()

    try:
        result = toggle_email_account_status(email, user)

        if result is None:
            return jsonify({"error": "Account not found or could not toggle status"}), 404

        return jsonify({
            "message": f"Account status changed successfully. Now {'active' if result else 'inactive'}",
            "active": result
        }), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    

@email_accounts_bp.route('/email-accounts/<int:id>', methods=['GET'])
@jwt_required()
def get_account_by_id(id):
    account = get_email_account_by_id(id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.serialize()), 200


@email_accounts_bp.route('/email-accounts/<int:id>', methods=['PUT'])
@jwt_required()
def update_account(id):
    data = request.get_json()
    account = update_email_account(id, data)

    if account is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "message": "Account successfully updated",
        "account": account.serialize()
    }), 200  