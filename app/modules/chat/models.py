__author__ = 'cybran'

# Import the database object (db) from the main application module
from app import db
import datetime
# Import module models (i.e. User) for using in subscribers field

class Message(db.EmbeddedDocument):

    meta = {
        'indexes' : ['-created_at'],
        'ordering' : ['-created_at']
    }

    author = db.StringField(required=True)
    date_created = db.DateTimeField(default=datetime.datetime.now)
    content = db.StringField(required=True)

    def __str__(self):
        return self.content

class Channel(db.Document):

    name = db.StringField(required=True, unique=True)
    messages = db.ListField(db.EmbeddedDocumentField(Message))

    def __str__(self):
        return self.name
