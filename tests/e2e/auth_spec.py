import json
import pytest
from db.db import db
from common.app import app

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


BASE_URL = 'http://localhost:5000'

def test_register_success(test_client):
    response = test_client.post(f'{BASE_URL}/auth/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['message'] == 'Registration successful'
    assert 'accessToken' in data['data']
    assert data['data']['user']['firstName'] == 'John'
    assert data['data']['user']['lastName'] == 'Doe'
    assert data['data']['user']['email'] == 'john.doe@example.com'

def test_missing_fields(test_client):
    response = test_client.post(f'{BASE_URL}/auth/register', json={})
    assert response.status_code == 422
    data = json.loads(response.data)
    assert 'errors' in data

def test_duplicate_email(test_client):
    response = test_client.post('/auth/register', json={
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    response = test_client.post(f'{BASE_URL}/auth/register', json={
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    assert response.status_code == 422
    data = json.loads(response.data)
    assert 'errors' in data

def test_login_success(test_client):
    test_client.post('/auth/register', json={
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "jane.doe@example.com",
        "password": "password123",
        "phone": "1234567890"
    })
    response = test_client.post('/auth/login', json={
        "email": "jane.doe@example.com",
        "password": "password123"
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Login successful'
    assert 'accessToken' in data['data']