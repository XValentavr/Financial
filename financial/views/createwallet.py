from flask import render_template, session, flash
from flask_login import login_required

from financial.service.wallet import get_wallets, insert_wallet
from financial.views import financial, WTForm


@financial.route("/wallet", methods=["POST", "GET"])
@login_required
def wallet():
    form = WTForm.Wallet()
    if not session["superuser"]:
        return render_template("404.html"), 404
    else:
        if form.validate_on_submit():
            name = form.wallet.data
            wallets = get_wallets()
            identifier = wallets[-1].get('id') + 1
            for w in wallets:
                if str(w.get(name)).strip() == name.strip():
                    print('уже есть')
                    flash('Такой кошелек уже есть')
                    return render_template(
                        "wallet.html", form=form, user=session["user"], superuser=session["superuser"]
                    )
            else:
                insert_wallet(identifier, name)
        return render_template(
            "wallet.html", form=form, user=session["user"], superuser=session["superuser"]
        )


@financial.route("/changewallet", methods=["POST", "GET"])
@login_required
def changewallet():
    if not session["superuser"]:
        return render_template("404.html")
    return render_template(
        "changewallet.html", user=session["user"], superuser=session["superuser"]
    )
