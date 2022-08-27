from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required

from financial.service.currency import get_current_currency_by_name, insert_new_currency, change_currency
from financial.views import financial, WTForm


@financial.route("/currency", methods=["POST", "GET"])
@login_required
def currency():
    if not session["superuser"]:
        return render_template("404.html")
    return render_template(
        "currency.html", user=session["user"], superuser=session["superuser"]
    )


@financial.route("/currency/edit/<string:name>", methods=["POST", "GET"])
@login_required
def currency_change(name):
    form = WTForm.CreateCurrency()
    if form.validate_on_submit():
        existed = get_current_currency_by_name(form.name.data)
        if existed:
            flash("Такая валюта уже есть", "error")
            return render_template(
                "currency_change.html",
                form=form,
                user=session["user"],
                superuser=session["superuser"],
            )
        else:
            change_currency(name, form.name.data)
            return redirect(url_for("financial.income"))
    return render_template(
        "currency_change.html", form=form, user=session["user"], superuser=session["superuser"]
    )


@financial.route("/currency/add", methods=["POST", "GET"])
@login_required
def currency_add():
    form = WTForm.CreateCurrency()
    if form.validate_on_submit():
        existed = get_current_currency_by_name(form.name.data)
        if existed:
            flash("Такая валюта уже есть", "error")
            return render_template(
                "currency_change.html",
                form=form,
                user=session["user"],
                superuser=session["superuser"],
            )
        else:
            insert_new_currency(form.name.data)
            return redirect(url_for("financial.currency"))
    return render_template(
        "currency_add.html", form=form, user=session["user"], superuser=session["superuser"]
    )
