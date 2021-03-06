from flask import render_template, session, request
from flask_login import login_required

from financial.service.accounts import get_name_account_checker
from financial.service.currency import get_list_currency
from financial.service.error import add_error
from financial.service.moneysum import exchange_command
from financial.views import financial


@financial.route("/exchange", methods=["POST", "GET"])
@login_required
def exchange():
    ths = get_list_currency()
    selected = get_name_account_checker()
    if request.method == "POST":
        if "errormessage" in request.form:
            add_error(request.form.get('errormessage'))
            return render_template(
                "exchange.html",
                user=session["user"],
                superuser=session["superuser"],
                ths=ths,
                ths_from=ths,
                selected_from=selected,
                ths_to=ths,
                selected_to=selected,
            )
        else:
            exchange_command(request.form.getlist(""))
    return render_template(
        "exchange.html",
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
        ths_from=ths,
        selected_from=selected,
        ths_to=ths,
        selected_to=selected,
    )
