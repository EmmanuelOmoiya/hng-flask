from db.db import db
import uuid

class Organisation(db.Model):
    __tablename__ = 'organisation'
    orgId = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    creator_id = db.Column(db.String(36), db.ForeignKey('user.userId'), nullable=False)
    users = db.relationship('User', secondary='organisation_user', backref=db.backref('organisations', lazy=True))


class OrganisationUser(db.Model):
    __tablename__ = 'organisation_user'
    orgId = db.Column(db.String(36), db.ForeignKey('organisation.orgId'), primary_key=True)
    userId = db.Column(db.String(36), db.ForeignKey('user.userId'), primary_key=True)