from flask import render_template, session, request
from flask_login import login_required

from financial.service.accounts import delete_data
from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.views import financial, WTForm


@financial.route("/outcome", methods=["POST", "GET"])
@login_required
def outcome():
    wtform = WTForm.Outcome()
    wtform.set_choices()
    ths = get_list_currency()
    if request.method == "POST":
        form = request.form
        message = form.get("errormessage")
        if message is None:
            if wtform.validate_on_submit():
                delete_data(wtform)
                return render_template(
                    "outcome.html",
                    form=wtform,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
        else:
            add_error(message)
            return render_template(
                "outcome.html",
                form=wtform,
                user=session["user"],
                superuser=session["superuser"],
                ths=ths,
            )
    return render_template(
        "outcome.html",
        form=wtform,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
