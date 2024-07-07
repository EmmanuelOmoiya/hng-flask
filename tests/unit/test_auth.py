import pytest
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, decode_token
from common.app import app
from db.db import db
from modules.user.user_model import User

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope='module')
def user():
    user = User(email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

def test_token_expiration(test_client, user):
    token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30))
    decoded = decode_token(token)
    expiration = datetime.utcfromtimestamp(decoded['exp'])
    expected_expiration = datetime.utcnow() + timedelta(minutes=30)
    assert abs((expiration - expected_expiration).total_seconds()) < 5

def test_token_contains_user_id(test_client, user):
    token = create_access_token(identity=user.id)
    decoded = decode_token(token)
    assert decoded['sub'] == user.id
