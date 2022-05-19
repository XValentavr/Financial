from flask import render_template, session
from flask_login import login_required

from financial.service.accounts import delete_data
from financial.service.currency import get_list_currency
from financial.views import financial, WTForm


@financial.route("/outcome", methods=["POST", "GET"])
@login_required
def outcome():
    form = WTForm.Outcome()
    form.set_choices('outcome')
    if form.validate_on_submit():
        delete_data(form)
    ths = get_list_currency()
    return render_template(
        "outcome.html",
        user=session["user"],
        superuser=session["superuser"],
        form=form,
        ths=ths,
    )
