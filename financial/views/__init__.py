"""
__init__.py file of views module with
imported info, employee_view and department_view submodules
Register the user blueprint and specify the logic on '/' and '/home' addresses
Also handle an error status
"""
# pylint: disable=cyclic-import
from flask import Blueprint

from ..service.currency import get_list_currency

financial = Blueprint("financial", __name__)

from flask import render_template, redirect, session, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .WTForm import LoginForm
from ..models.users import Users
from financial import login_manager
from financial.service.users import get_user_by_name, get_super_user_by_name
from . import income
from . import outcome
from . import moving
from . import exchange
from . import pay
from . import adduser
from . import changeuser
from . import moving
from . import createwallet


@login_manager.user_loader
def load_user(user_UUID):
    return Users.query.get(user_UUID)


# because the blueprint must be registered before importing the views


@financial.route("/", methods=["POST", "GET"])
@financial.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle requests to the /login route
    Cretates login page using WTForm using post-requests.
    Admin data contains in MySQL database

    :return: html page
    """
    ths = get_list_currency()
    session.permanent = True
    if current_user.is_authenticated:
        return redirect(url_for("financial.income"))
    form = LoginForm()
    if form.validate_on_submit():
        root_user = get_user_by_name(form.username.data, form.password.data)
        superuser = get_super_user_by_name(form.username.data, form.password.data)
        if not root_user and not superuser:
            return redirect(url_for("financial.login"))
        if root_user and not superuser:
            login_user(root_user)
            session["superuser"] = False
            session["user"] = True
            session["UUID"] = root_user.UUID
            return render_template(
                "base.html", superuser=False, user=True, session=session, ths=ths
            )

        elif root_user and superuser:
            login_user(superuser)
            session["UUID"] = superuser.UUID
            session["superuser"] = True
            session["user"] = False

            return render_template(
                "base.html", superuser=True, user=False, session=session, ths=ths
            )

    return render_template("login.html", form=form)


@financial.route("/logout")
@login_required
def logout():
    """
    Handle requests to the /logout route
    Allow employee to logout moving to home page.
    """
    logout_user()
    del session["superuser"]
    del session["user"]

    return redirect(url_for("financial.login"))


@financial.app_errorhandler(404)
def handle_404(err):
    """
    Handel 404 error and redirect to 404.html page
    """
    return render_template("404.html"), 404


@financial.app_errorhandler(401)
def handle_401(err):
    """
    Handel 401 error and redirect to 401.html page
    """
    return render_template("401.html"), 401
