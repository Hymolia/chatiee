__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Set the route and accepted methods
@mod_chat.route('/')
def index():
    return render_template('chat/conversation.html')