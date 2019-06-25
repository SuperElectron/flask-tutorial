# db/models.py
from mongoengine.document import Document
from mongoengine.fields import StringField, IntField, DateTimeField, ObjectIdField
import datetime


class Users(Document):
    username = StringField()
    password = StringField()


class Posts(Document):
    post_id = IntField()
    username = StringField()
    author_id = ObjectIdField()
    created = DateTimeField(default=datetime.datetime.utcnow)
    title = StringField()
    body = StringField()
