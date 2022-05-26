from flask import render_template, session, flash, request
from flask_login import login_required

from financial.service.userroot import add_all_possible_pairs
from financial.service.users import get_all_user
from financial.service.wallet import get_wallets, insert_wallet, update_wallet
from financial.views import financial, WTForm


@financial.route("/wallet", methods=["POST", "GET"])
@login_required
def wallet():
    form = WTForm.Wallet()
    users = get_all_user()
    if not session["superuser"]:
        return render_template("404.html"), 404
    else:
        if request.method == "POST":
            print(request.form)
            if request.form.get('All') == 'on':
                ...
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
                        variant=users
                    )
            else:
                insert_wallet(identifier, name, visibility)
                add_all_possible_pairs()
        return render_template(
            "wallet.html",
            form=form,
            user=session["user"],
            superuser=session["superuser"],
            variant=users
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
        if request.method == "POST":
            print(request.form)
        users = get_all_user()
        if form.validate_on_submit():
            update_wallet(
                identifier,
                form.wallet.data,
                form.visibility.data,
            )
            return render_template(
                "changewallet.html",
                user=session["user"],
                superuser=session["superuser"]
            )

    return render_template(
        "wallet.html", form=form, user=session["user"], superuser=session["superuser"],
        variant=users
    )
