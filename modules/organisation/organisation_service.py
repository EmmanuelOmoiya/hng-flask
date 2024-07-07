from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from modules.organisation.organisation_model import Organisation, OrganisationUser
from db.db import db

def create_organisation_main(data):
    current_user_id = get_jwt_identity()

    if 'name' not in data or not data['name']:
        return jsonify({"status": "Bad Request", "message": "Client error", "statusCode": 400}), 400

    new_org = Organisation(name=data['name'], description=data.get('description'), creator_id=current_user_id)
    db.session.add(new_org)
    db.session.commit()

    org_user = OrganisationUser(orgId=new_org.orgId, userId=current_user_id)
    db.session.add(org_user)
    db.session.commit()

    return new_org