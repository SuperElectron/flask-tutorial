# flaskr/blog.py
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
from flaskr.auth import login_required
from werkzeug.exceptions import abort
from bson.objectid import ObjectId
from flask_mongoengine import MongoEngine

from db.models import Users, Posts
from db.db import get_mongoDB

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """ home page that shows posts with ability to create/edit if logged in """
    db = get_mongoDB()

    # get post data got this user
    query = db.posts.find()

    def f(item):
        item["_id"] = str(item["_id"])
        item["author_id"] = str(item["author_id"])
        return item
    posts = [f(item) for item in query]

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """ renders create a new blog post """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:

            db = get_mongoDB()
            result = db.posts.find().sort([("post_id", -1)]).limit(1)
            max_post = 0
            for item in result:
                max_post = item["post_id"]

            if(max_post == 0 | max_post is None):
                max_post == 1
            else:
                max_post += 1

            # # # create post data
            username = db.users.find_one({"_id": ObjectId(str(g.user))})["username"]
            post = Posts(post_id=max_post, username=username, author_id=ObjectId(g.user), title=title, body=body)
            post.save()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    """ get posts from the user and check for errors """

    db = get_mongoDB()
    post = db.posts.find_one({"post_id": id})

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and str(post['author_id']) != g.user:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """ gives logged in user option to update their post"""

    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_mongoDB()

            # write to existing post
            db.posts.update_one({"post_id": id}, {"$set": {"body": body, "title": title}})

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """ gives logged in user option to delete their post """
    get_post(id)
    db = get_mongoDB()

    # delete existing post
    db.posts.delete_one({"post_id": id})

    return redirect(url_for('blog.index'))


# a simple page that says hello
@bp.route('/hello')
def hello():
    """ shows some functionality for g.db """
    return 'Hello, World!'
    # db = get_mongoDB()
    # return jsonify('Hello, world!', dir(g), dir(db))
