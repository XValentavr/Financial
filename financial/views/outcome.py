from flask import render_template, session, request
from flask_login import login_required

from financial.service.accounts import delete_data
from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.views import financial, WTForm


@financial.route("/outcome", methods=["POST", "GET"])
@login_required
def outcome():
    form = WTForm.Outcome()
    form.set_choices()
    ths = get_list_currency()
    if request.method == "POST":
        add_error(request.form)
        return render_template(
            "outcome.html",
            user=session["user"],
            superuser=session["superuser"],
            form=form,
            ths=ths,
        )
    if form.validate_on_submit():
        delete_data(form)
    return render_template(
        "outcome.html",
        user=session["user"],
        superuser=session["superuser"],
        form=form,
        ths=ths,
    )
