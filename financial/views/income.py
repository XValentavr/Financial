from flask import render_template, session
from flask_login import login_required

from financial.service.accounts import insert_account
from financial.service.users import get_user_by_UUID
from financial.views import financial, WTForm


@financial.route('/income', methods=["POST", "GET"])
@login_required
def income():
    form = WTForm.Income()
    if form.validate_on_submit():
        summa = form.sum.data
        currency = form.currency.choices
        wallet = form.wallet.data
        info = form.info.data
        date = form.date.data
        user = get_user_by_UUID(session['UUID'].strip())
        insert_account(form, summa, currency, wallet, info, date, user.id)
    return render_template('income.html', form=form, user=session['user'], superuser=session['superuser'])
