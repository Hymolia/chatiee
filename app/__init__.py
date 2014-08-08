__author__ = 'cybran'

# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.mongoengine import MongoEngine

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.config.update(testing = True)

# Define the database object which is imported
# by modules and controllers
app.config["MONGODB_DB"] = 'MONGODB_DB'

db = MongoEngine(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.modules.intro.controllers import mod_intro as intro_module
from app.modules.auth.controllers import mod_auth as auth_module
from app.modules.chat.controllers import mod_chat as chat_module

# Register blueprint(s)
app.register_blueprint(intro_module)
app.register_blueprint(auth_module)
app.register_blueprint(chat_module)
# app.register_blueprint(xyz_module)
# ..



# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()