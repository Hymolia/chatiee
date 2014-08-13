__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, redirect, url_for, Response, g
import json
from app.modules.chat.models import Message, Channel
from app.modules.chat.forms import New_channel
from app.modules.auth.models import User
from datetime import datetime, timedelta

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

# RESTful API for managing channels

class ChatAPI(MethodView):
    decorators = [login_required]
    # returns JSON response
    def response_json(self, list):
        return Response(json.dumps(list), mimetype='application/json')


class ChannelAPI(ChatAPI):
    def get(self, channel_name, unread="false"):
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
                similar_channels = Channel.objects(name__contains=request.get_json()['search-name'])

                names_of_channels = list()
                for channel in similar_channels:
                    names_of_channels.extend(channel.name)

                return self.response_json(list=names_of_channels)

        # /channels/<channel_name>
        # if we haven't received "unread" tag, return all messages
        if unread is "false":

            # checking for user subscribes, if user subscribed for channel_name, update date
            user = User.objects.get(email=current_user.email)
            if channel_name in user.unread_channels:
                user.unread_channels[channel_name] = datetime.now()
                user.save()

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

        # else we'll return only messages count after that datetime
        else:
            user = User.objects.get(email=current_user.email)
            subscribe_datetime = user.unread_channels[channel_name]

            messages = Channel.objects.get(name=channel_name)\
                .messages
            unread_count = 0
            for message in messages:
                if message.date_created > subscribe_datetime:
                    unread_count += 1

            return Response(response=str(unread_count))

    def post(self, channel_name):
        # /channels
        if channel_name is None:
            # insert new channel
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
# search channels

mod_chat.add_url_rule('/channels/<channel_name>',
                      view_func=channel_view,
                      methods=['GET', 'POST'])

mod_chat.add_url_rule('/channels/<channel_name>/unread=<unread>',
                      view_func=channel_view,
                      methods=['GET'])


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