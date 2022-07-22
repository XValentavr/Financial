from flask import render_template, redirect, session, url_for
from flask_login import login_user, login_required, logout_user, current_user

from financial import login_manager
from financial.models.users import Users
from financial.service.users import get_user_by_name, get_super_user_by_name
from financial.views.WTForm import LoginForm
from . import financial


@login_manager.user_loader
def load_user(user_UUID):
    return Users.query.get(user_UUID)


@financial.route("/", methods=["POST", "GET"])
@financial.route("/login", methods=["POST", "GET"])
def login():
    """
    Handle requests to the /login route
    Cretates login page using WTForm using post-requests.
    Admin data contains in MySQL database

    :return: html page
    """
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
            return redirect(url_for("financial.income"))

        elif root_user and superuser:
            login_user(superuser)
            session["UUID"] = superuser.UUID
            session["superuser"] = True
            session["user"] = False

            return redirect(url_for("financial.income"))

        return redirect(url_for("financial.income"))
    return render_template("login.html", form=form)


@financial.route("/logout", methods=["POST", "GET"])
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
