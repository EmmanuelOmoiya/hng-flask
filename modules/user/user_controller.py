from modules.user.user_model import User
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required()
def get_user(id):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=id).first()

    if not user or (user.userId != current_user_id and user not in User.query.filter_by(userId=current_user_id).first().organisations):
        return jsonify({"status": "Bad request", "message": "Access denied", "statusCode": 403}), 403

    response = {
        "status": "success",
        "message": "User found",
        "data": {
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "phone": user.phone
        }
    }
    return jsonify(response), 200