
from flask import render_template, session, request
from flask_login import login_required

from financial.service.accounts import insert_account
from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.views import financial, WTForm


@financial.route("/income", methods=["POST", "GET"])
@login_required
def income():
    wtform = WTForm.Income()
    wtform.set_choices()
    ths = get_list_currency()
    if request.method == "POST":
        form = request.form
        message = form.get("errormessage")
        if message is None:
            print(wtform.data)
            if wtform.validate_on_submit():
                insert_account(wtform)
                return render_template(
                    "income.html",
                    form=wtform,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
        else:
            add_error(message)
            return render_template(
                "income.html",
                form=wtform,
                user=session["user"],
                superuser=session["superuser"],
                ths=ths,
            )
    return render_template(
        "income.html",
        form=wtform,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
