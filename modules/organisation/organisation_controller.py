from flask_jwt_extended import get_jwt_identity
from modules.user.user_model import User
from flask import jsonify
from modules.organisation.organisation_service import create_organisation_main
from modules.organisation.organisation_model import Organisation
from db.db import db
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def get_organisations():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()
    organisations = user.organisations

    org_list = [{
        "orgId": org.orgId,
        "name": org.name,
        "description": org.description
    } for org in organisations]

    response = {
        "status": "success",
        "message": "Organisations found",
        "data": {
            "organisations": org_list
        }
    }
    return jsonify(response), 200

@jwt_required()
def get_organisation(org_id):
    current_user_id = get_jwt_identity()
    org = Organisation.query.filter_by(orgId=org_id).first()

    if not org or (current_user_id not in [user.userId for user in org.users]):
        return jsonify({"status": "Bad request", "message": "Access denied", "statusCode": 403}), 403

    response = {
        "status": "success",
        "message": "Organisation found",
        "data": {
            "orgId": org.orgId,
            "name": org.name,
            "description": org.description
        }
    }
    return jsonify(response), 200


def create_organisation(data):
    new_org = create_organisation_main(data)
    response = {
        "status": "success",
        "message": "Organisation created successfully",
        "data": {
            "orgId": new_org.orgId,
            "name": new_org.name,
            "description": new_org.description
        }
    }
    return jsonify(response), 201


@jwt_required()
def add_user_to_organisation(org_id, data):
    current_user_id = get_jwt_identity()

    org = Organisation.query.filter_by(orgId=org_id).first()

    if not org or current_user_id not in [user.userId for user in org.users]:
        return jsonify({"status": "Bad request", "message": "Access denied", "statusCode": 403}), 403

    user = User.query.filter_by(userId=data['userId']).first()

    if not user:
        return jsonify({"status": "Bad request", "message": "User not found", "statusCode": 404}), 404

    org.users.append(user)
    db.session.commit()

    response = {
        "status": "success",
        "message": "User added to organisation successfully"
    }
    return jsonify(response), 200
