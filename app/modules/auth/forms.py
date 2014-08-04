from multiprocessing.managers import public_methods

__author__ = 'cybran'

# Import Form and RecaptchaField (optional)
from flask_wtf import Form, RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField # BooleanField

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
                                    DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [
                                    DataRequired(message='Must provide a password. ;-)')])
    password_repeat = PasswordField('Repeat password', [
                                    DataRequired(message='Passwords must match each other')])

    recaptcha = RecaptchaField()