from flask import render_template, session, request
from flask_login import login_required
from financial.service.accounts import insert_pay_account, get_name_account_checker
from financial.service.currency import get_list_currency
from financial.views import financial


@financial.route("/paynment", methods=["POST", "GET"])
@login_required
def paynment():
    if not session["superuser"]:
        return render_template("404.html"), 404
    ths = get_list_currency()
    selected = get_name_account_checker()
    if request.method == "POST":
        insert_pay_account(request.form)

    return render_template(
        "pay.html",
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
        selected=selected,
    )
