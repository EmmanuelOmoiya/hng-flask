from flask import Blueprint, request
from modules.auth.auth_controller import login, register

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def loginMain():
    data = request.get_json()
    return login(data)

@auth_bp.route('/auth/register', methods=['POST'])
def registerMain():
    data = request.get_json()
    return register(data)
