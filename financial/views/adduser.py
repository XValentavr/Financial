from flask import render_template, session, flash, redirect, url_for
from flask_login import login_required

from financial.service.userroot import add_all_possible_pairs
from financial.service.users import add_user, get_user_by_enter_name
from financial.views import financial, WTForm


@financial.route("/add", methods=["POST", "GET"])
@login_required
def add():
    form = WTForm.Register()
    if form.validate_on_submit():
        root_user = get_user_by_enter_name(form.username.data)
        if root_user:
            flash("Такой пользователь уже есть", "error")
            return render_template(
                "add.html",
                form=form,
                user=session["user"],
                superuser=session["superuser"],
            )
        else:
            add_user(form.username.data, form.password.data)
            add_all_possible_pairs()
            return redirect(url_for("financial.income"))
    return render_template(
        "add.html", form=form, user=session["user"], superuser=session["superuser"]
    )
