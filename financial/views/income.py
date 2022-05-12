from flask import render_template, session
from flask_login import login_required

from financial.views import financial, WTForm


@financial.route('/income', methods=["POST", "GET"])
@login_required
def income():
    form = WTForm.Register()

    return render_template('income.html', form=form, user=session['user'], superuser=session['superuser'])
