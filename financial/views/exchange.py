from flask import render_template, session
from flask_login import login_required

from financial.views import financial


@financial.route("/exchange", methods=["POST", "GET"])
@login_required
def exchange():
    return render_template(
        "exchange.html", user=session["user"], superuser=session["superuser"]
    )
