__author__ = 'cybran'

# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

from datetime import datetime

# Define a User model
class User(db.DynamicDocument, db.EmbeddedDocument):
    user_id = db.IntField(required=True, unique=True)
    # user-friendly identificator
    email = db.StringField(required=True, unique=True)
    #  user-friendly name
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    registered_at = db.DateTimeField(default=datetime.now, required=True)

    # store of subscribed channels and last viewed time
    unread_channels = db.DictField()

    # __init__ can't be function in inherited class from db.Document
    # def __init__(self, email, username, password):
    #     self.email = email
    #     self.username = username
    #     self.set_password(password)

    def __str__(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return self.__str__()