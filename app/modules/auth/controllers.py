__author__ = 'cybran'

# Import flask dependencies
from flask import Blueprint, request, render_template, flash, redirect, url_for, make_response
# Import security functions
from werkzeug.security import generate_password_hash, check_password_hash
# Import module forms
from app.modules.auth.forms import LoginForm, RegistrationForm
# Import module models (i.e. User)
from app.modules.auth.models import User

# Import login manager
from app import login_manager
from flask.ext.login import login_user, logout_user, current_user


@login_manager.user_loader
def load_user(id):
    return User.objects.get(user_id=id)


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Define unauthorized handler with user-friendly request.path
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth.signin') + '?next=' + request.path)


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template("auth/signin.html", form=form)
    # If sign in form is submitted
    # Verify the sign in form
    if form.validate_on_submit():
        registered_user = User.objects.get(email=form.email.data)
        if registered_user and check_password_hash(registered_user.password_hash, form.password.data):
            login_user(registered_user)
            redirect_to_chat = redirect(request.args.get("next") or url_for("chat.main"))
            response = make_response(redirect_to_chat)
            response.set_cookie('username', value=registered_user.username)
            return response

    flash('Wrong email or password', 'error-message')
    return redirect(url_for('chat.signin'))


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template("auth/signup.html", form=form)

    if form.validate_on_submit():
        if not User.objects(email=form.email.data):
            if not User.objects(username=form.username.data):
                new_user = User()
                new_user.user_id = User.objects().count() + 1
                new_user.email = form.email.data
                new_user.username = form.username.data
                new_user.password_hash = generate_password_hash(form.password.data)
                new_user.save()
                flash('You have been registered!')
                return redirect(url_for('.signin'))
            flash('User with this username is already exist', 'error-message')
        flash('User with this email is already exist', 'error-message')

    return render_template("auth/signup.html", form=form)


@mod_auth.route('/logout')
def logout():
    logout_user()
    response = make_response(redirect(url_for("intro.index")))
    response.set_cookie('username', expires=0)
    return response

