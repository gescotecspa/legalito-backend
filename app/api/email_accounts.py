from flask import Blueprint, request, jsonify, abort
from app import db
from app.services.email_account_service import add_email_account,list_email_accounts,delete_email_accounts,get_email_account

email_accounts_bp = Blueprint('email_accounts', __name__)

@email_accounts_bp.route('/email-accounts', methods=['POST'])
def add():
    data = request.json
    account = add_email_account(data)
    return jsonify({"message": "Cuenta agregada", "account": account.serialize()}), 201

@email_accounts_bp.route('/email-accounts', methods=['GET'])
def list_email_acc():
    accounts = list_email_accounts()
    return jsonify([a.serialize() for a in accounts])

@email_accounts_bp.route('/email-accounts/byuser/<string:user>', methods=['GET'])
def get_email_by_user(user):
    account = get_email_account(user)
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify(account.serialize()), 200

@email_accounts_bp.route('/email-accounts', methods=['DELETE'])
def delete():
    data = request.get_json()
    email = data.get('email')
    user = data.get('user')

    try:
        delete_email_accounts(email,user)
       
        return jsonify(True), 200
    except Exception as e:
        print(e)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@email_accounts_bp.route('/email-accounts', methods=['PUT'])
def update():
    abort(501)