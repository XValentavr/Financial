from flask import render_template, session
from flask_login import login_required

from financial.service.currency import get_list_currency
from financial.views import financial


@financial.route("/walletinfo/<string:wallet>", methods=["POST", "GET"])
@login_required
def walletinfo(wallet):
    ths = get_list_currency()
    return render_template(
        "walletinfo.html", user=session["user"], superuser=session["superuser"], ths=ths
    )
