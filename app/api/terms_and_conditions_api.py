from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restful import Api, Resource
from app.services.terms_and_conditions_service import TermsAndConditionsService

terms_and_conditions_api__bp = Blueprint('terms_and_conditions_api', __name__)
api = Api(terms_and_conditions_api__bp)

class TermsAndConditionsResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data or 'content' not in data or 'version' not in data:
            return {'message': 'Missing required fields: content or version'}, 400
        terms = TermsAndConditionsService.create_terms(data['content'], data['version'])
        return terms.serialize(), 201

    @jwt_required()
    def put(self, terms_id):
        data = request.get_json()
        if not data or 'content' not in data or 'version' not in data:
            return {'message': 'Missing required fields: content or version'}, 400
        terms = TermsAndConditionsService.update_terms(terms_id, data['content'], data['version'])
        if terms:
            return terms.serialize(), 200
        return {'message': 'Terms and conditions not found or update failed'}, 404

    @jwt_required()
    def delete(self, terms_id):
        if TermsAndConditionsService.delete_terms(terms_id):
            return {'message': f'Terms and conditions with ID {terms_id} deleted'}, 200
        return {'message': 'Terms and conditions not found'}, 404

class TermsAndConditionsListResource(Resource):
    def get(self):
        terms_last_version = TermsAndConditionsService.get_latest_version()
        if terms_last_version:
            return terms_last_version.serialize(), 200
        return {'message': 'No terms and conditions found'}, 404
    

    def post(self):
        data = request.get_json()
        if not data or 'content' not in data or 'version' not in data:
            return {'message': 'Missing required fields: content or version'}, 400
        terms = TermsAndConditionsService.create_terms(data['content'], data['version'])
        return terms.serialize(), 201
class AcceptTermsResource(Resource):
    def put(self, user_id):
        try:
            user = TermsAndConditionsService.accept_terms(user_id)
            return user.serialize(), 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': f'Internal server error: {str(e)}'}, 500

api.add_resource(TermsAndConditionsResource, '/terms/<int:terms_id>')
api.add_resource(TermsAndConditionsListResource, '/terms')
api.add_resource(AcceptTermsResource, '/users/<int:user_id>/accept-terms')

