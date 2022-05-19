from flask import session, render_template, request
from flask_login import login_required

from financial.service.accounts import get_name_account_checker
from financial.service.comments import update_comment
from financial.service.currency import get_list_currency
from financial.service.moneysum import get_by_pair, get_by_account_status
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
                form.set_choices("edit", [[choices[1]], wallet])
                ths = get_list_currency()
                if form.validate_on_submit():
                    update_comment(
                        form, p.pairidentificator, "income", float(choices[0])
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
                form.set_choices("edit", [[choices[1]], wallet])
                ths = get_list_currency()
                if form.validate_on_submit():
                    update_comment(
                        form, p.pairidentificator, "outcome", float(choices[0])
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
                for v in valuta:
                    if v.name in choices[1]:
                        valuta = [v]
                        break
                for s in selected:
                    if s.name in wallet:
                        selected = [s]
                        break
                if request.method == "POST":
                    update_comment(
                        request.form,
                        p.pairidentificator,
                        "outcome",
                        float(choices[0]),
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
        for p in pairs:
            if p.ismoved == 1:
                form = WTForm.Move()
                return render_template(
                    "move.html",
                    form=form,
                    user=session["user"],
                    superuser=session["superuser"],
                    ths=ths,
                )
            elif p.exchanged == 1:
                if request.method == "POST":
                    form = request.form
                    return render_template(
                        "exchange.html",
                        form=form,
                        user=session["user"],
                        superuser=session["superuser"],
                        ths=ths,
                    )
    return render_template(
        "income.html",
        form=form,
        user=session["user"],
        superuser=session["superuser"],
        ths=ths,
    )
