from flask import render_template, session, request
from flask_login import login_required

from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.service.moneysum import moving_command
from financial.views import financial, WTForm


@financial.route("/move", methods=["POST", "GET"])
@login_required
def move():
    form = WTForm.Move()
    form.set_choices()
    ths = get_list_currency()
    if request.method == "POST":
        add_error(request.form)
        return render_template(
            "move.html",
            form=form,
            user=session["user"],
            superuser=session["superuser"],
            ths=ths,
        )
    if form.validate_on_submit():
        moving_command(form)
    return render_template(
        "move.html",
        form=form,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
