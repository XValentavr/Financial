from flask import render_template, session, flash, request
from flask_login import login_required

from financial.service.userroot import add_all_possible_pairs, update_roots, update_public_visibility
from financial.service.users import get_all_user, get_user_by_enter_name
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
                        variant=users,
                    )
            else:
                insert_wallet(identifier, name, visibility)
                add_all_possible_pairs()
        return render_template(
            "wallet.html",
            form=form,
            user=session["user"],
            superuser=session["superuser"],
            variant=users,
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
    # load employee.html template
    users = get_all_user()
    if not session["superuser"]:
        return render_template("404.html")
    else:

        form = WTForm.Wallet()
        if form.visibility.data == "Да":
            if request.method == "POST":
                if request.form.get("All") == "on":
                    update_roots(identifier, 1)
                else:
                    for u in users:
                        if request.form.get(u.name) == "on":
                            usr = get_user_by_enter_name(u.name)
                            update_roots(identifier, 1, usr.id)
        elif form.public.data == "Да":
            if request.method == "POST":
                if request.form.get("Allvisibility") == "on":
                    update_public_visibility(identifier, 1)
                else:
                    for u in users:
                        if request.form.get(u.name) == "on":
                            usr = get_user_by_enter_name(u.name)
                            update_public_visibility(identifier, 1, usr.id)
        else:
            update_roots(identifier, 0)
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
        "wallet.html",
        form=form,
        user=session["user"],
        superuser=session["superuser"],
        variant=users,
    )
