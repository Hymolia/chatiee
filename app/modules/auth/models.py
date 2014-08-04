__author__ = 'cybran'

# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
import datetime

# Define a User model
class User(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    nickname = db.StringField(required=True, unique=True)
    name = db.StringField(max_length=255, required=True)

    def __str__(self):
        return self.name + self.nickname

    meta = {
        'indexes' : ['-created_at', 'facebook_id'],
        'ordering' : ['-created_at']
    }