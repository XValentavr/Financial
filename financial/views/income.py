from flask import render_template, session
from flask_login import login_required

from financial.views import financial


@financial.route('/income', methods=["POST", "GET"])
@login_required
def income():
    return render_template('income.html', user=session['user'], superuser=session['superuser'])
