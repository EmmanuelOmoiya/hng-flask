from flask import Flask
import config.config as cfg

app = Flask(__name__)

app.config["SECRET_KEY"] = cfg.app["secret"]
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{cfg.db["username"]}:{cfg.db["password"]}@localhost:5432/orgenz'
app.config["JWT_SECRET_KEY"] = cfg.jwt["secret"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_TOKEN_LOCATION"] = cfg.jwt["location"]