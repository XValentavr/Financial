import requests
from flask import render_template, session
from flask_login import login_required

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.service.moneysum import get_to_sum, update_summa, inser_into_money_sum, get_new_transfered_sum
from financial.service.users import get_user_by_UUID
from financial.views import financial, WTForm


@financial.route("/move", methods=["POST", "GET"])
@login_required
def move():
    form = WTForm.Move()
    if form.validate_on_submit():
        sum_ = float(form.sum_.data)
        from_ = form.from_.data
        currency_from = int(form.currency_from.data)
        currency_to = int(form.currency_to.data)
        user = get_user_by_UUID(session["UUID"].strip())
        user = user.get('id')
        summa_to_delete = get_to_sum(user, int(from_), currency_from)
        info = form.info.data
        date = form.date.data
        to_ = form.to_.data
        final_sum = 0
        new_entered_summa = get_new_transfered_sum(sum_, currency_from, currency_to)
        if summa_to_delete:
            for summa_to_delete in summa_to_delete:
                final_sum = summa_to_delete.moneysum
                final_sum -= float(sum_)
        else:
            if not summa_to_delete:
                inser_into_money_sum(0, user, currency_from, from_)
                final_sum = 0 - int(sum_)
                summa_to_delete = get_to_sum(user, int(from_), currency_from)
                for _sum in summa_to_delete:
                    summa_to_delete = _sum
        update_summa(
            summa_to_delete, final_sum, user, currency_from, from_, date, info, None, sum_
        )
        summa_to_add = get_to_sum(user, int(to_), currency_to)
        if summa_to_add:
            for summa_to_add in summa_to_add:
                summa_to_add.moneysum += float(new_entered_summa)
                update_summa(
                    summa_to_add, summa_to_add.moneysum, user, currency_to, to_, date, info, sum_, None
                )
        else:
            inser_into_money_sum(sum_, user, currency_to, int(to_))
            summa_to_update = get_to_sum(user, int(to_), currency_to)
            if summa_to_update:
                for summa_to_update in summa_to_update:
                    money = summa_to_update.id
                    accounts = Accountstatus(money=money, date=date, comments=info, addedsumma=sum_, deletedsumma=None)
                    database.session.add(accounts)
                    database.session.commit()

    return render_template(
        "move.html", form=form, user=session["user"], superuser=session["superuser"]
    )
