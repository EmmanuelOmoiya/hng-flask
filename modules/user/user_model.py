from db.db import db
import uuid

class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), unique=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(350), nullable=False)
    phone = db.Column(db.String(20))