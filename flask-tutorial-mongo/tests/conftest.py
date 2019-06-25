# test/conftest.py
import os
import tempfile

import pytest
from flaskr import create_app

"""
    pytest [name].py -s
    -s is used to show all the output

    pytest -v
    - get list of each function instead of dots
"""
# read in data from mongoDB
# with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
#     _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():

    database_configuration = os.getenv('APP_SETTINGS')
    app = create_app(test_config=database_configuration)

    with app.app_context():
        from db import db
        db.init_app(app)
        from db.db import get_mongoDB
        mongo = get_mongoDB()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='blackOps'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
