from flask import render_template, session
from flask_login import login_required

from financial.views import financial


@financial.route("/move", methods=["POST", "GET"])
@login_required
def move():
    return render_template(
        "move.html", user=session["user"], superuser=session["superuser"]
    )
