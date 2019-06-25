# db/db.py
import os

import click
from flask import current_app, g, session
from flask.cli import with_appcontext
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash
from db.models import Users, Posts

from bson.objectid import ObjectId

"""
Note:
app.teardown_appcontext(close_db) on line 42 can be commented out.
This gives you the ability to login to database ...
$ mongo --port 27107
> use devDB
> show collections
> db.users.find.pretty()
[lists the users in your database ...]
"""


def get_mongoDB():
    """ this function avoids circular referencing when dealing with MongoEngine, or any other database
        Import this to any module/file/function using mongo: from db.db import get_mongoDB
    """
    if 'db' not in g:

        # connect to mongoEngine and load configuration settings from config.py
        mongo = MongoEngine()
        dbVersion = current_app.config["MONGODB_SETTINGS"]["db"]
        mongo.connect(dbVersion, connect=False)

        # print(vars(g))
        # print(dir(mongo))

        # save database into flask's "g" variable
        g.db = mongo.get_db()

    return g.db


def close_db(e=None):
    """ closes connection to database on port 27017 """
    db = g.pop('mongo', None)
    if db is not None:
        print('possible error disconnecting from mongo ... ')


def init_app(app):
    """ teardown after database request is complete AND initialize cli function """
    app.teardown_appcontext(close_db)  # disconnect DB
    app.cli.add_command(init_db_command)


def init_db():
    """ populate database with admin user and two posts """
    try:
        version = current_app.config["MONGODB_SETTINGS"]["db"]
        print('using {} database'.format(version))
    except:
        print("ERROR: $export APP_SETTINGS=flaskr.config.DevelopmentConfig OR $export APP_SETTINGS=flaskr.config.TestingConfig' to configure database")

    if(version is None):
        print('raise error: dataBase == None')

    # if the database version is not 'testDB' and not 'devDB' don't proceed
    elif((version != 'testDB') & (version != 'devDB')):
        print('raise error: not testDB or devDB')

    else:
        print('\nrefresh database ...')
        with current_app.app_context():
            db = get_mongoDB()

            # find all collections in current database
            collections = db.list_collection_names()
            for item in collections:
                db.drop_collection(item)

            # adding administrative user to setup schema
            adminUser = Users(username="admin", password=generate_password_hash("blackOps"))
            adminUser.save()

            # get the admin user objectId
            admin = db.users.find_one({"username": 'admin'})

            # add two posts to the database
            post = Posts(post_id=1, username=admin["username"], author_id=ObjectId(str(admin["_id"])), title='first post', body='a first time posting')
            post2 = Posts(post_id=2, username=admin["username"], author_id=ObjectId(str(admin["_id"])), title='second post', body='second go at it')
            post.save()
            post2.save()
            print('Added admin user and two posts\n')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create one Admin user."""
    init_db()
    click.echo('Initialized the database.')
