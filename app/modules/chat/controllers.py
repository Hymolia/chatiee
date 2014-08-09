__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, redirect, url_for
from app.modules.chat.models import Message, Channel

from app.modules.chat.forms import New_channel, New_message

from flask.views import MethodView
from flask.ext.login import login_required

from flask import g

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Home page
@mod_chat.route('/')
@login_required
def index():
    form = New_channel(request.form)
    channels = Channel.objects()
    return render_template('chat/channel.html', form=form, channels=channels)


# class Index(View):
# def dispatch_request(self):
#         form = New_channel(request.form)
#         channels = Channel.objects()
#         return render_template('chat/channel.html', form=form, channels=channels)
#
#
# mod_chat.add_url_rule('/', view_func=Index.as_view('index'))


# Creating channels

@mod_chat.route('/channels/create', methods=['GET', 'POST'])
@login_required
def create_channel():
    form = New_channel(request.form)
    if form.validate_on_submit():
        channel = Channel()
        channel.name = form.name.data
        channel.save()
        return redirect(url_for('.index'))


# return rendered template with last 50 messages
@login_required
@mod_chat.route('/channels/<channel>')
def get_message(channel):
    # fixme monkey code, it needs for drawing createchannel form
    channel_form = New_channel(request.form)

    # fixme monkey code, for post_message test
    message_form = New_message(request.form)

    messages = Channel.objects.get(name=channel).messages[-5:]
    return render_template('chat/conversation.html', messages=messages, form=channel_form,
                           template_message_form=message_form)

    # FIXME need to realize views as classes, not functions


# class Get_message(View):
#     def dispatch_request(self, channel):
#         #form = New_channel(request.form)
#         current_channel = Channel.objects.get(name=channel)
#         messages = current_channel.messages[:50]
#         return render_template('chat/conversation.html', messages=messages)
#
#mod_chat.add_url_rule('/channels/<channel>', view_func=Get_message.as_view('Get_message'))

# @mod_chat.route('/channels/<channel>/postmessage', methods=['POST'])
# def post_message(channel):
#     form = New_message(request.form)
#     message = Message()
#     print(form.text.data)
#     message.text = form.text.data
#     print(request.args.get('channel'))
#     current_channel = Channel.objects.get(name=request.args.get('channel'))
#     current_channel.messages.append(message)
#     current_channel.save()
    # return redirect('chat.index')

class MessageAPI(MethodView):
    def post(self, channel):
        message = Message(**request.get_json())
        message.author = g.user.username
        current_channel = Channel.objects.get(name=channel)
        current_channel.messages.append(message)
        current_channel.save()
        return redirect(url_for('chat.index'))

mod_chat.add_url_rule('/channels/<channel>/postmessage', view_func=MessageAPI.as_view('message'))