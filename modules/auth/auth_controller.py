from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask import jsonify
import bcrypt
from modules.helpers.utils import validate_user_data
from modules.user.user_model import User
from modules.organisation.organisation_model import Organisation, OrganisationUser
import bcrypt
from db.db import db

# from modules.auth.auth_service import register as registerMain

def register(data):
    validation_errors = validate_user_data(data)

    if validation_errors:
        return jsonify({"errors": validation_errors}), 422

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"status": "Bad request","message": "Registration unsuccessful - account with this email already exists", "statusCode": 400}), 400
 
    salt = bcrypt.gensalt()     
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    # hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        firstName=data['firstName'],
        lastName=data['lastName'],
        email=data['email'],
        password=hashed_password,
        phone=data.get('phone')
    )
    
    db.session.add(new_user)
    db.session.commit()

    org_name = f"{data['firstName']}'s Organisation"
    new_org = Organisation(name=org_name, creator_id=new_user.userId)
    db.session.add(new_org)
    db.session.commit()

    org_user = OrganisationUser(orgId=new_org.orgId, userId=new_user.userId)
    db.session.add(org_user)
    db.session.commit()
    access_token = create_access_token(identity=new_user.userId)
    response = {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": new_user.userId,
                "firstName": new_user.firstName,
                "lastName": new_user.lastName,
                "email": new_user.email,
                "phone": new_user.phone
            }
        }
    }
    return jsonify(response), 201


def login(data):
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), bytes.fromhex(user.password[2:])):
        access_token = create_access_token(identity=user.userId)
        response = {
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone
                }
            }
        }
        return jsonify(response), 200

    return jsonify({"status": "Bad request", "message": "Authentication failed", "statusCode": 401}), 401
