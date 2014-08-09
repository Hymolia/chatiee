__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, render_template

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_intro = Blueprint('intro', __name__, url_prefix='/')

# Set the route and accepted methods
@mod_intro.route('/')
def index():
    return render_template('intro/intro.html')