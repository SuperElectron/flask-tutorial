# tests/test_factory.py
from flaskr import create_app
import os


def test_config():
    assert os.getenv('APP_SETTINGS') == 'flaskr.config.TestingConfig'


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
