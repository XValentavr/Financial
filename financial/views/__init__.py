"""
__init__.py file of views module with
imported info, employee_view and department_view submodules
Register the user blueprint and specify the logic on '/' and '/home' addresses
Also handle an error status
"""
# pylint: disable=cyclic-import
from flask import Blueprint

financial = Blueprint('financial', __name__)

from flask import render_template, redirect, session, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import WTForm
from ..models.users import Users
from werkzeug.security import check_password_hash
from financial import login_manager
from financial.service.users import get_user_by_name


@login_manager.user_loader
def load_user(user_UUID):
    return Users.query.get(user_UUID)


# because the blueprint must be registered before importing the views


@financial.route('/home')
@login_required
def home_page():
    """
    Render the home page template on the / route
    """
    return render_template('index.html', session=session)


@financial.route('/', methods=["POST", "GET"])
@financial.route('/login', methods=["POST", "GET"])
def login():
    """
    Handle requests to the /login route
    Cretates login page using WTForm using post-requests.
    Admin data contains in MySQL database

    :return: html page
    """
    session.permanent = True
    if current_user.is_authenticated:
        return redirect(url_for('financial.home_page'))
    form = WTForm.LoginForm()
    if form.validate_on_submit():
        root_user = get_user_by_name(form.username.data)
        if not root_user:
            return redirect(url_for('financial.login'))
        if not check_password_hash(root_user.password, form.password.data):
            return redirect(url_for('financial.login'))
        login_user(root_user)
        return redirect(url_for('financial.home_page'))
    return render_template('login.html', form=form)


@financial.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Allow employee to logout moving to home page.
    """
    logout_user()
    return redirect(url_for('financial.login'))


@financial.app_errorhandler(404)
def handle_404(err):
    """
    Handel 404 error and redirect to 404.html page
    """
    return render_template('404.html'), 404


@financial.app_errorhandler(401)
def handle_401(err):
    """
    Handel 401 error and redirect to 401.html page
    """
    return render_template('401.html'), 401
