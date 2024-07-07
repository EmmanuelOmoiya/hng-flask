import pytest
from common.app import app
from db.db import db
from modules.user.user_model import User
from modules.organisation.organisation_model import Organisation
from flask_jwt_extended import create_access_token
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
def organisations():
    org1 = Organisation(name='Org1')
    org2 = Organisation(name='Org2')
    db.session.add_all([org1, org2])
    db.session.commit()
    yield org1, org2
    db.session.delete(org1)
    db.session.delete(org2)
    db.session.commit()

@pytest.fixture(scope='module')
def users(organisations):
    org1, org2 = organisations
    user1 = User(email='user1@example.com', password='password', organisation=org1)
    user2 = User(email='user2@example.com', password='password', organisation=org2)
    db.session.add_all([user1, user2])
    db.session.commit()
    yield user1, user2
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.commit()

def test_user_cannot_access_other_organisation_data(test_client, users):
    user1, user2 = users
    token = create_access_token(identity=user1.id)
    response = test_client.get(
        f'/organisations/{user2.organisation_id}', 
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 403
