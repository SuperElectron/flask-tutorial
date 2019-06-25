# tests/test_auth.py
import pytest
from flask import g, session
from db.db import get_mongoDB


def test_register(client, app):
    with app.app_context():
        db = get_mongoDB()
        assert db.users.find_one({"username": 'pickle_monster'}) is None

        if(db.users.find_one({"username": 'a'}) is not None):
            db.users.delete_one({"username": 'a'})

        assert client.get('/auth/register').status_code == 200
        response = client.post(
            '/auth/register', data={'username': 'a', 'password': 'a'}
        )
        print(vars(response.headers))
        assert 'http://localhost/auth/login' == response.headers['Location']

        assert db.users.find_one({"username": 'a'}) is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('admin', 'blackOps', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        db = get_mongoDB()
        userId = db.users.find_one({"username": 'admin'})["_id"]
        assert g.user == str(userId)


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('neverBeenCreated', 'test', b'Incorrect username.'),
    ('admin', 'appleCobler', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert g.user is None
