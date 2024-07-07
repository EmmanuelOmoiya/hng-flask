from flask_jwt_extended import jwt_required
from flask import Blueprint, request
from modules.organisation.organisation_controller import get_organisation, get_organisations, create_organisation, add_user_to_organisation

organisation_bp = Blueprint('organisation', __name__)

@jwt_required()
@organisation_bp.route('/api/organisations', methods=['GET'])
def getOrganisations():
    return get_organisations()

@jwt_required()
@organisation_bp.route('/api/organisations/<org_id>', methods=['GET'])
def getOrganisation(org_id):
    return get_organisation(org_id)

@jwt_required()
@organisation_bp.route('/api/organisations', methods=['POST'])
def createOrganisation():
    data = request.get_json()
    return create_organisation(data)

@jwt_required()
@organisation_bp.route('/api/organisations/<org_id>/users', methods=['POST'])
def addUserToOrganisation(org_id):
    data = request.get_json()
    return add_user_to_organisation(org_id, data)