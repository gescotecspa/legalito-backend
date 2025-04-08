from flask import Blueprint, request, jsonify, abort
from app import db
from app.services.email_account_service import add_email_account, get_email_account_by_id, get_email_accounts_by_user,list_email_accounts,delete_email_accounts, toggle_email_account_status, update_email_account

email_accounts_bp = Blueprint('email_accounts', __name__)

@email_accounts_bp.route('/email-accounts', methods=['POST'])
def add():
    data = request.json
    try:
        account = add_email_account(data)
        return jsonify({"message": "Account successfully added", "account": account.serialize()}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error: " + str(e)}), 500

@email_accounts_bp.route('/email-accounts', methods=['GET'])
def list_email_acc():
    accounts = list_email_accounts()
    return jsonify([a.serialize() for a in accounts])

@email_accounts_bp.route('/email-accounts/byuser/<string:user>', methods=['GET'])
def get_email_by_user(user):
    accounts = get_email_accounts_by_user(user)
    # Siempre devolvé una lista, aunque esté vacía
    return jsonify([a.serialize() for a in accounts]), 200

@email_accounts_bp.route('/email-accounts', methods=['DELETE'])
def delete():
    data = request.get_json()
    email = data.get('email')
    user = data.get('user')

    try:
        success = delete_email_accounts(email, user)

        if not success:
            return jsonify({"error": "Account not found or could not be deleted"}), 404

        return jsonify({"message": "Account successfully deleted"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@email_accounts_bp.route('/email-accounts', methods=['PUT'])
def update():
    abort(501)
    
@email_accounts_bp.route('/email-accounts/toggle-status', methods=['PUT'])
def toggle_status():
    data = request.get_json()
    email = data.get('email')
    user = data.get('user')

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
def get_account_by_id(id):
    account = get_email_account_by_id(id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(account.serialize()), 200


@email_accounts_bp.route('/email-accounts/<int:id>', methods=['PUT'])
def update_account(id):
    data = request.get_json()
    account = update_email_account(id, data)

    if account is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "message": "Account successfully updated",
        "account": account.serialize()
    }), 200  