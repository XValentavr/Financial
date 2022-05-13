from flask import render_template, session
from flask_login import login_required

from financial.views import financial


@financial.route("/pay", methods=["POST", "GET"])
@login_required
def pay():
    if not session["superuser"]:
        return render_template("404.html"), 404
    else:
        return render_template(
            "pay.html", user=session["user"], superuser=session["superuser"]
        )
