# tests/test_blog.py
import pytest
from db.db import get_mongoDB
import datetime
from bson.objectid import ObjectId


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_create(client, auth, app):
    with app.app_context():
        db = get_mongoDB()
        db.posts.drop()

    auth.login()
    assert client.get('/create').status_code == 200

    client.post('/create', data={'title': 'first post', 'body': 'a first posting'})
    client.post('/create', data={'title': 'second post', 'body': 'second go at it'})

    with app.app_context():
        db = get_mongoDB()
        cursor = db.posts.find().sort([("post_id", -1)]).limit(1)
        count = 0
        for item in cursor:
            count = item["post_id"]
        assert count == 2


def test_index(client, auth):
    # look at home view without being logged in
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    # log in and verify data functionality
    auth.login()
    response = client.get('/')
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    assert b'Log Out' in response.data
    assert b'New' in response.data
    assert b'first post' in response.data
    assert b'a first posting' in response.data
    assert today in str(response.data)
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', ('/4/update', '/4/delete'))
def test_exists_required(client, auth, path, app):
    auth.login()
    assert client.post(path).status_code == 404


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': 'changed the body'})

    with app.app_context():
        db = get_mongoDB()
        post = db.posts.find_one({"post_id": 1})
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', ('/create', '/1/update'))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_mongoDB()
        adminId = db.users.find_one({"username": 'admin'})["_id"]
        user2Id = db.users.find_one({"username": 'a'})["_id"]
        db.posts.update_one({"post_id": 1}, {"$set": {"author_id": str(user2Id)}})

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/2/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_mongoDB()
        post = db.posts.find_one({"post_id": 2})
        assert post is None
