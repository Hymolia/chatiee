__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from app.modules.chat.models import Message, Channel

from app.modules.chat.forms import New_channel

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Set the route and accepted methods
@mod_chat.route('/')
def index():
    return render_template('chat/channel.html')

@mod_chat.route('channels/create', methods='POST')
def create_channel():
    form = New_channel(request.form)

# return rendered template with last 50 messages
@mod_chat.route('channels/<channel>')
def get_message(channel):
    current_channel = Channel.objects.get(name=channel)
    messages = current_channel.messages[:50]
    return render_template('chat/conversation.html', messages=messages)

@mod_chat.route('channels/<channel>/postmessage')
def post_message():
    pass

