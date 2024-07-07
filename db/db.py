from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from common.app import app

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app)
