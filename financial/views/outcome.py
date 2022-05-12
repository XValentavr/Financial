from flask import render_template, session
from flask_login import login_required

from financial.views import financial


@financial.route('/outcome', methods=["POST", "GET"])
@login_required
def outcome():
    return render_template('outcome.html', user=session['user'], superuser=session['superuser'])
