from flask import render_template, session, request
from flask_login import login_required

from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.service.moneysum import moving_command
from financial.views import financial, WTForm


@financial.route("/move", methods=["POST", "GET"])
@login_required
def move():
    wtform = WTForm.Move()
    wtform.set_choices()
    ths = get_list_currency()
    if request.method == "POST":
        form = request.form
        message = form.get("errormessage")
        if message is None:
            if wtform.validate_on_submit():
                moving_command(wtform)
                return render_template(
                    "move.html",
                    form=wtform,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
        else:
            add_error(message)
            return render_template(
                "move.html",
                form=wtform,
                user=session["user"],
                superuser=session["superuser"],
                ths=ths,
            )
    return render_template(
        "move.html",
        form=wtform,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
