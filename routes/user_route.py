from flask import Blueprint, request
from modules.user.user_controller import get_user
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)

@jwt_required()
@user_bp.route('/api/users/<id>', methods=['GET'])
def getUser(id):
    return get_user(id)