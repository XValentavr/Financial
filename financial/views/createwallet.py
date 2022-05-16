from flask import render_template, session, flash
from flask_login import login_required

from financial.service.wallet import get_wallets, insert_wallet, update_wallet
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
            visibility = form.visibility.data
            wallets = get_wallets()
            identifier = wallets[-1].get("id") + 1
            for w in wallets:
                if str(w["name"]).strip() == name.strip():
                    flash("Такой кошелек уже есть")
                    return render_template(
                        "wallet.html",
                        form=form,
                        user=session["user"],
                        superuser=session["superuser"],
                    )
            else:
                insert_wallet(identifier, name, visibility)
        return render_template(
            "wallet.html",
            form=form,
            user=session["user"],
            superuser=session["superuser"],
        )


@financial.route("/changewallet", methods=["POST", "GET"])
@login_required
def changewallet():
    if not session["superuser"]:
        return render_template("404.html")
    return render_template(
        "changewallet.html", user=session["user"], superuser=session["superuser"]
    )


@financial.route("/wallet/edit/<string:identifier>", methods=["GET", "POST"])
@login_required
def edit_wallet(identifier):
    """
    This function represents the logic on /employees/edit address
    :return: the rendered employee.html template to edit an existing employee
    """

    # load employee.html template
    if not session["superuser"]:
        return render_template("404.html")
    else:
        form = WTForm.Wallet()
        if form.validate_on_submit():
            update_wallet(
                identifier,
                form.wallet.data,
                form.visibility.data,
            )
            return render_template(
                "changewallet.html",
                user=session["user"],
                superuser=session["superuser"],
            )

    return render_template(
        "wallet.html", form=form, user=session["user"], superuser=session["superuser"]
    )
