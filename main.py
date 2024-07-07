from flask import Flask, jsonify
import logging
import config.config as cfg
from flask_cors import CORS
from flask_compress import Compress
from db.db import db
from common.app import app
from flask_bcrypt import Bcrypt
from routes.auth_route import auth_bp
from routes.user_route import user_bp
from routes.organisation_route import organisation_bp
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from flask_migrate import Migrate

# app = Flask(__name__)
CORS(app, origins=["*"])
Compress(app)

logging.basicConfig(filename='error.log', level=logging.ERROR)

jwt = JWTManager(app)

# db.init_app(app)
# migrate = Migrate(app, db)

app.config["SECRET_KEY"] = cfg.app["secret"]
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{cfg.db["username"]}:{cfg.db["password"]}@{cfg.db["server"]}:{cfg.db["port"]}/{cfg.db["db"]}'
app.config["JWT_SECRET_KEY"] = cfg.jwt["secret"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_TOKEN_LOCATION"] = cfg.jwt["location"]

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": 'Hello from Flask!'})

# Auth routes
app.register_blueprint(auth_bp)

# User routes
app.register_blueprint(user_bp)

# Organisation routes
app.register_blueprint(organisation_bp)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "status": "Badd Request",
        "message": "Page not found"
    }), 404 

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "status": "Bad Request",
        "message": "Internal Server error"
    }), 500 

portMain = cfg.app["port"]

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=portMain)