__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, session, redirect, url_for

# Import security functions
from werkzeug.security import generate_password_hash, check_password_hash

# Import module forms
from app.modules.auth.forms import LoginForm, RegistrationForm

# Import module models (i.e. User)
from app.modules.auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.objects.get(email=form.email.data)
        print(user.password_hash)
        if user and check_password_hash(user.password_hash, form.password.data):

            session['user_id'] = str(user.id)

            flash('Welcome %s' % user.username)

            return redirect(url_for('.signup'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)

@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)

    if form.validate_on_submit():
        if not User.objects(email=form.email.data):
            if not User.objects(username=form.username.data):
                new_user = User()
                new_user.email = form.email.data
                new_user.username = form.username.data
                new_user.password_hash = generate_password_hash(form.password.data)

                new_user.save()
                flash('You have been registered!')
                return redirect(url_for('.signin'))
            flash('User with this username is already exist', 'error-message')
        flash('User with this email is already exist', 'error-message')

    return render_template("auth/signup.html", form=form)