# tests/test_db.py
import pytest
from db.db import get_mongoDB, close_db


def test_get_close_db(app):

    with app.app_context():
        mongo = get_mongoDB()
        assert mongo is get_mongoDB()
        assert str(type(mongo)) == "<class 'pymongo.database.Database'>"

    with pytest.raises(Exception) as e:
        close_db()
        a = mongo.users.find_one({"username": 'a'})
    assert 'RuntimeError' in str(e)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('db.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

