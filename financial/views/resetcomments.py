from flask import session, render_template, request
from flask_login import login_required

from financial.service.accounts import get_by_pair, get_by_account_status
from financial.service.accounts import get_name_account_checker
from financial.service.comments import (
    update_comment, update_moving_and_exchange_commands,
)
from financial.service.currency import get_list_currency
from financial.views import financial, WTForm


@financial.route("/comments/edit/<string:UUID>", methods=["GET", "POST"])
@login_required
def edit_comments(UUID):
    ths = get_list_currency()
    form = WTForm.Income()
    pairs = get_by_pair(UUID.strip())
    if len(pairs) < 2:
        for p in pairs:
            if p.addedsumma is not None and p.number is None:
                form = WTForm.Income()
                choices = p.addedsumma
                choices = choices.split(" ")
                wallet = list(get_by_account_status(p.money))
                form.set_choices()
                ths = get_list_currency()
                if form.validate_on_submit():
                    update_comment(
                        form,
                        p.pairidentificator,
                        "income",
                        float(choices[0]),
                        wallet,
                        choices[1],
                    )
                return render_template(
                    "income.html",
                    form=form,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
            elif p.deletedsumma is not None and p.number is None:
                form = WTForm.Outcome()
                choices = p.deletedsumma
                choices = choices.split(" ")
                wallet = list(get_by_account_status(p.money))
                form.set_choices()
                ths = get_list_currency()
                if form.validate_on_submit():
                    update_comment(
                        form,
                        p.pairidentificator,
                        "outcome",
                        float(choices[0]),
                        wallet,
                        choices[1],
                    )
                return render_template(
                    "outcome.html",
                    form=form,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
            elif p.number is not None:
                choices = p.deletedsumma
                choices = choices.split(" ")
                wallet = list(get_by_account_status(p.money))
                ths = get_list_currency()
                valuta = ths
                selected = get_name_account_checker()
                if request.method == "POST":
                    update_comment(
                        request.form,
                        p.pairidentificator,
                        "outcome",
                        float(choices[0]),
                        wallet,
                        choices[1],
                        "pay",
                    )
                return render_template(
                    "pay.html",
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                    valuta=valuta,
                    selected=selected,
                )
    else:
        for i in pairs:
            if i.ismoved == 1:
                added = pairs[0]
                deleted = pairs[1]

                choices_add = added.deletedsumma
                choices_add = choices_add.split(" ")
                wallet_add = list(get_by_account_status(added.money))

                choices_delete = deleted.addedsumma
                choices_delete = choices_delete.split(" ")
                wallet_delete = list(get_by_account_status(deleted.money))

                ths = get_list_currency()
                form = WTForm.Move()
                form.set_choices()
                if form.validate_on_submit():
                    update_moving_and_exchange_commands(
                        form,
                        choices_add[0],
                        choices_delete[0],
                        wallet_add,
                        wallet_delete,
                        choices_add[1],
                        choices_delete[1],'moving',
                        added.pairidentificator,
                    )
                return render_template(
                    "move.html",
                    form=form,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
            if i.isexchanged == 1:

                added = pairs[0]
                deleted = pairs[1]

                choices_add = added.deletedsumma
                choices_add = choices_add.split(" ")
                wallet_add = list(get_by_account_status(added.money))

                choices_delete = deleted.addedsumma
                choices_delete = choices_delete.split(" ")
                wallet_delete = list(get_by_account_status(deleted.money))

                form = request.form
                ths = get_list_currency()
                valuta_delete = valuta_add = ths
                selected_add = selected_delete = get_name_account_checker()
                if request.method == "POST":
                    update_moving_and_exchange_commands(
                        request.form,
                        choices_add[0],
                        choices_delete[0],
                        wallet_add,
                        wallet_delete,
                        choices_add[1],
                        choices_delete[1],'exchange',
                        added.pairidentificator
                    )
                return render_template(
                    "exchange.html",
                    form=form,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                    ths_from=valuta_delete,
                    selected_from=selected_delete,
                    ths_to=valuta_add,
                    selected_to=selected_add,
                )
    return render_template(
        "income.html",
        form=form,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
