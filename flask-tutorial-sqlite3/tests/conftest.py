import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # create and open a temporary file, returning the file object and the file path to it
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,        # set flask in testing mode
        'DATABASE': db_path,    # points to temporary file
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # Tests will use the client to make requests
    # to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # creates a runner that can call the Click commands
    # registered with the application
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
