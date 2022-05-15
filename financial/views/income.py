from flask import render_template, session
from flask_login import login_required
from financial.service.accounts import insert_account
from financial.service.currency import get_list_currency
from financial.views import financial, WTForm


@financial.route("/income", methods=["POST", "GET"])
@login_required
def income():
    form = WTForm.Income()
    form.set_choices()
    ths = get_list_currency()
    if form.validate_on_submit():
        insert_account(form)
    return render_template(
        "income.html",
        form=form,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
