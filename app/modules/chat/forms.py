__author__ = 'cybran'

from flask_wtf import Form

from wtforms import StringField

from wtforms.validators import DataRequired


class New_channel(Form):
    name = StringField('Name',[DataRequired(message='Enter the name')])


class New_message(Form):
    text = StringField('Text',[DataRequired(message='Enter the text')])