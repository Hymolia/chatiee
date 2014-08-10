__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, redirect, url_for, Response, g
import json
from app.modules.chat.models import Message, Channel
from app.modules.chat.forms import New_channel, New_message
from app.modules.auth.models import User
from datetime import datetime

from flask.views import MethodView
from flask.ext.login import login_required, current_user

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

# Main page
@mod_chat.route('/')
@login_required
def main():
    form = New_channel(request.form)
    channels = Channel.objects()
    return render_template('chat/chat.html', form=form, channels=channels)
#
#
# # class Index(View):
# # def dispatch_request(self):
# # form = New_channel(request.form)
# #         channels = Channel.objects()
# #         return render_template('chat/channel.html', form=form, channels=channels)
# #
# #
# # mod_chat.add_url_rule('/', view_func=Index.as_view('index'))
#
#
# # Creating channels
#
# @mod_chat.route('/channels/create', methods=['GET', 'POST'])
# @login_required
# def create_channel():
#     form = New_channel(request.form)
#     if form.validate_on_submit():
#         channel = Channel()
#         channel.name = form.name.data
#         channel.save()
#         return redirect(url_for('.index'))
#
#
# # return rendered template with last 50 messages
# @login_required
# @mod_chat.route('/channels/<channel>')
# def get_message(channel):
#     # fixme monkey code, it needs for drawing createchannel form
#     channel_form = New_channel(request.form)
#
#     # fixme monkey code, for post_message test
#     message_form = New_message(request.form)
#
#     messages = Channel.objects.get(name=channel).messages[-5:]
#     return render_template('chat/conversation.html', messages=messages, form=channel_form,
#                            template_message_form=message_form)
#
#     # FIXME need to realize views as classes, not functions


# class UserAPI(MethodView):
#
#     def get(self, user_id):
#         if user_id is None:
#             # return a list of users
#             pass
#         else:
#             # expose a single user
#             pass
#
#     def post(self):
#         # create a new user
#         pass
#
#     def delete(self, user_id):
#         # delete a single user
#         pass
#
#     def put(self, user_id):
#         # update a single user
#         pass
#
# user_view = UserAPI.as_view('user_api')
# app.add_url_rule('/users/', defaults={'user_id': None},
#                  view_func=user_view, methods=['GET',])
# app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
# app.add_url_rule('/users/<int:user_id>', view_func=user_view,
#                  methods=['GET', 'PUT', 'DELETE'])


# RESTful API for managing channels

class ChatAPI(MethodView):
    decorators = [login_required]
    # returns JSON response
    def response_json(self, list):
        return Response(json.dumps(list), mimetype='application/json')


class ChannelAPI(ChatAPI):
    def get(self, channel_name):
        # /channels
        if channel_name is None:
            # if we haven't received search name string, return names of all channels
            if request.get_json() is None:
                channels = Channel.objects()
                names_of_channels = list()
                for channel in channels:
                    names_of_channels.append(dict(name=channel.name))
                return self.response_json(list=names_of_channels)

            # else return only channels with similar names to 'search-name'
            else:
                print("We've in!")
                similar_channels = Channel.objects(name__contains=request.get_json()['search-name'])

                names_of_channels = list()
                for channel in similar_channels:
                    names_of_channels.extend(channel.name)

                return self.response_json(list=names_of_channels)

        # /channels/<channel_name>
        # if we haven't received 'last-received-datetime', return all messages
        if request.args.get('unread') is None:
            messages = list()
            processed_channel = Channel.objects.get(name=channel_name)
            for single_message in processed_channel.messages:
                message_info = {
                    "author": single_message.author,
                    "content": single_message.content,
                    "date_created": single_message.date_created.strftime("%b %d %Y %H:%M:%S")
                }
                messages.append(message_info)
            return self.response_json(messages)
        # else we'll return only message after that datetime
        else:
            user = User.objects.get(email=current_user.email)
            subscribe_datetime = user.unread_channels[channel_name]

            unread_messages = Channel.objects.get(name=channel_name) \
                .messages(date_created__lt=subscribe_datetime)

            messages = list()
            for message in unread_messages:
                messages.extend(message)

            return self.response_json(messages)

    def post(self, channel_name):
        # /channels
        if channel_name is None:
            # insert new channel
            print(request.get_json())
            new_channel = Channel()
            new_channel.name = request.get_json()['name']
            new_channel.save()
            return Response(status=201)

        # /channels/<channel_name>
        else:
            # fixme avoided backbone.js bug with passing unexpected field (channel), but it's a duct tape
            json_model = request.get_json()
            message = Message()
            message.content = json_model['content']
            message.author = g.user.username
            current_channel = Channel.objects.get(name=channel_name)
            current_channel.messages.append(message)
            current_channel.save()
            return Response(status=201)


# set url rules for ChannelAPI
channel_view = ChannelAPI.as_view('channel_api')

mod_chat.add_url_rule('/channels',
                      defaults={'channel_name': None},
                      view_func=channel_view,
                      methods=['GET','POST'])

mod_chat.add_url_rule('/channels/<channel_name>',
                      view_func=channel_view,
                      methods=['GET', 'POST'])


class SubscribeAPI(ChatAPI):
    # return channel subscribes
    def get(self):
        user = User.objects.get(email=current_user.email)

        subscribes = dict()
        for key, value in user.unread_channels.items():
            subscribes[key] = value.strftime("%b %d %Y %H:%M:%S")

        return self.response_json(subscribes)

    # set (create or update) last read datetime for <channel_name>
    def post(self, channel_name):
        user = User.objects.get(email=current_user.email)
        user.unread_channels[channel_name] = datetime.now()
        user.save()
        return Response(status=200)

    # unsubscribe from channel <channel_name>
    def delete(self, channel_name):
        user = User.objects.get(email=current_user.email)
        del user.unread_channels[channel_name]
        user.save()
        return Response(status=200)



# set url rules for SubscribeAPI
subscribe_view = SubscribeAPI.as_view('subscribe_api')
mod_chat.add_url_rule('/user',
                      view_func=subscribe_view,
                      methods=['GET'])

mod_chat.add_url_rule('/user/<channel_name>',
                      view_func=subscribe_view,
                      methods=['POST', 'DELETE'])




