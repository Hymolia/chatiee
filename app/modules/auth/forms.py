__author__ = 'cybran'

# Import Form and RecaptchaField (optional)
from flask_wtf import Form, RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField

# Import Form validators
from wtforms.validators import DataRequired, Email, EqualTo



# Define the login form (WTForms)

class LoginForm(Form):
    email    = StringField('Email Address', [Email(),
                DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a password. ;-)')])

class RegistrationForm(Form):
    email    = StringField('Email Address', [Email(),
                                    DataRequired(message='Enter your email')])
    username = StringField('Username', [
                DataRequired(message='Enter new username')
                ])
    password = PasswordField('Password', [
                DataRequired(message='Must provide a password. ;-)'),
                EqualTo('confirm_password', message='Passwords must match')
                ])
    confirm_password = PasswordField('Repeat password')
    recaptcha = RecaptchaField()