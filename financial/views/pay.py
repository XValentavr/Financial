from flask import render_template, session
from flask_login import login_required

from financial.service.currency import get_list_currency
from financial.views import financial


@financial.route("/pay", methods=["POST", "GET"])
@login_required
def pay():
    if not session["superuser"]:
        return render_template("404.html"), 404
    else:
        ths = get_list_currency()
        return render_template(
            "pay.html", user=session["user"], superuser=session["superuser"], ths=ths
        )
