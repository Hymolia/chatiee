__author__ = 'cybran'

# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

import datetime

# Define a User model
class User(db.Document, db.EmbeddedDocument):

    meta = {
        'indexes' : ['-created_at'],
        'ordering' : ['-created_at']
    }
    email = db.StringField(required=True, unique=True)
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    # __init__ can't be in inherited class from db.Document
    # def __init__(self, email, username, password):
    #     self.email = email
    #     self.username = username
    #     self.set_password(password)

    def __str__(self):
        return self.username