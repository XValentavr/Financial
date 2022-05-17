from flask import render_template, session, request
from flask_login import login_required

from financial.service.accounts import get_name_account_checker
from financial.service.currency import get_list_currency
from financial.service.moneysum import exchange_command
from financial.views import financial


@financial.route("/exchange", methods=["POST", "GET"])
@login_required
def exchange():
    ths = get_list_currency()
    selected = get_name_account_checker()
    if request.method == "POST":
        exchange_command(request.form)
    return render_template(
        "exchange.html", user=session["user"], superuser=session["superuser"], ths=ths,
        selected=selected
    )
