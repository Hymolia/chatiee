__author__ = 'cybran'

# Import the database object (db) from the main application module
from app import db

# Import module models (i.e. User) for using in subscribers field
from app.modules.auth.models import User

class Message(db.EmbeddedDocument):
    author = db.StringField(required=True)
    content = db.StringField(required=True)

    def __str__(self):
        return self.content

class Channel(db.Document):

    name = db.StringField(required=True, unique=True)
    subscribers = db.ListField(db.EmbeddedDocumentField(User))
    messages = db.ListField(db.EmbeddedDocumentField(Message))

    def __str__(self):
        return self.name
