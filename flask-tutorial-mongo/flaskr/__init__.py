#!/usr/bin/env python
import os
from flask import Flask


"""
Note: setting up the application ...
$ export FLASK_APP=flaskr && export FLASK_ENV=development
$ export APP_SETTINGS=flaskr.config.DevelopmentConfig
$ export APP_SETTINGS=flaskr.config.TestingConfig
$ flask run
"""


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        database_configuration = os.getenv('APP_SETTINGS')
        app.config.from_object(database_configuration)
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    try:
        # ensure the instance folder exists
        os.makedirs(app.instance_path)
    except OSError:
        try:
            with open("instance/secret.txt", 'rb') as file:
                data = file.read()
            app.secret_key = data
        except:
            pass

    from db import db
    db.init_app(app)

    print('started ...')
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    print("secret key ... :", app.config["SECRET_KEY"])
    return app
