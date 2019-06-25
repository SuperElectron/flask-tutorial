# flaskr/auth.py
import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash

from db.models import Users
from bson import json_util
from bson.objectid import ObjectId
from db.db import get_mongoDB

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ basic registration page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # ensure the username is not taken
        else:
            db = get_mongoDB()
            result = db.users.find_one({"username": username})

            if result is not None:
                error = 'User {} is already registered.'.format(username)

        # if error checks pass, insert 'name' and hashed 'password' into database
        if error is None:
            addOne = Users(username=username, password=generate_password_hash(password))
            addOne.save()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ basic login page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_mongoDB()
        error = None

        # search database for the username provided
        user = db.users.find_one({"username": username})
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # careful with the conversion type!!!
            # user["_id"] must be converted to serializable JSON type to be stored as session
            # converting back is tricky unless kept like this!
            session['user_id'] = str(user["_id"])

            user_id = session.get('user_id')
            foundIt = db.users.find_one({"_id": ObjectId(user["_id"])})
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """ verifies from session if any user is logged in """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    elif user_id is not None:
        try:
            # try to connect to database
            db = get_mongoDB()
            userId = db.users.find_one({"_id": ObjectId(str(user_id))})["username"]
            g.user = user_id
            # may just have old user id in browser cache, so clear it!
            if(userId is None):
                session.clear()
        except:
            session.clear()


@bp.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('index'))
