import os
import uuid

import sqlalchemy
from flask import request, session as s
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.moneysum import Moneysum
from financial.service.currency import (
    get_current_currency_by_name,
    get_current_currency,
)
from financial.service.userroot import get_user_root_id
from financial.service.users import get_user_by_UUID
from financial.service.wallet import get_current_wallet_by_name


def inser_into_money_sum(money: float, user: int, currency: int, wallet: int):
    """
    This module inserts data to moneysum
    :param money: money to enter
    :param user: user of transaction
    :param currency: currency of transaction
    :return:
    """
    general = get_user_root_id(wallet, user)
    money = Moneysum(
        wallet=wallet, moneysum=money, user=user, currency=currency, isgeneral=general
    )
    database.session.add(money)
    database.session.commit()


def get_to_sum(user: int, wallet: int, currency: int):
    """
    This module gets to sum
    :param user: user id
    :param wallet: wallet id
    :param currency: currency of value
    :return:
    """
    money = Moneysum.query.filter_by(user=user, wallet=wallet, currency=currency).all()
    if money:
        for m in money:
            if float(m.moneysum) != 0.0:
                return money
        return money
    return None


def update_summa(
        summas,
        summa,
        user,
        currency,
        wallet,
        date,
        info,
        s_add,
        s_delete,
        number,
        percent,
        exchanged,
        moved,
        modified,
        deleted,
        pair,
        useridentifier,
) -> None:
    """
    This module updates money in wallet
    :param summas: object of get summa
    :param summa: new summa
    :param user: current user
    :param currency: currenct id
    :param wallet: wallet id
    :param date: date to add
    :param info: info about adding
    :param s_add: summa to add
    :param s_delete" summa to delete
    :return: None
    """
    currency_name = get_current_currency(currency).name
    if int(summas.wallet) != int(wallet) and int(summas.currency) != int(currency):
        inser_into_money_sum(summa, user, currency, wallet)
        accounts = Accountstatus(
            money=summas.id,
            date=date,
            comments=info,
            addedsumma=str(s_add) + " " + currency_name if s_add else None,
            deletedsumma=str(s_delete) + " " + currency_name if s_delete else None,
            number=number,
            percent=percent,
            isexchanged=exchanged,
            ismoved=moved,
            ismodified=modified,
            isdeleted=deleted,
            pairidentificator=pair,
            useridentificator=useridentifier,
        )
        database.session.add(accounts)
        database.session.commit()
    else:
        summas.moneysum = summa
        database.session.add(summas)
        database.session.commit()
        accounts = Accountstatus(
            money=summas.id,
            date=date,
            comments=info,
            addedsumma=str(s_add) + " " + currency_name if s_add else None,
            deletedsumma=str(s_delete) + " " + currency_name if s_delete else None,
            number=number,
            percent=percent,
            isexchanged=exchanged,
            ismoved=moved,
            ismodified=modified,
            isdeleted=deleted,
            pairidentificator=pair,
            useridentificator=useridentifier,
        )
        database.session.add(accounts)
        database.session.commit()


def get_count_users(identifier: int):
    """
    This module gets users wallet group by wallets
    :return: list of number of wallets
    """
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    session = sessionmaker(bind=engine)
    session = session()
    with session as session:
        result = (
            session.query(Moneysum.wallet, func.count(Moneysum.wallet))
                .filter_by(wallet=identifier)
                .group_by(Moneysum.wallet)
                .all()
        )
    res_list = []
    if result:
        res_list.append(list(result[0]))
    return res_list


def exchange_command(form):
    """
    This module exchange currencies
    :param form: form
    :return: None
    """
    pair = uuid.uuid4()
    summa = request.form.get("summa")

    from_ = request.form.get("wallet_from")
    to_ = from_
    from_ = get_current_wallet_by_name(from_)
    to_ = get_current_wallet_by_name(to_)

    currency_from_name = request.form.get("valuta_sold")
    currency_to = request.form.get("valuta_buy")
    currency_from = get_current_currency_by_name(currency_from_name).id
    currency_to = get_current_currency_by_name(currency_to).id

    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")

    summa_to_delete = get_to_sum(user, int(from_), currency_from)
    info = request.form.get("comments")
    date = str(request.form.get("date"))
    final_sum = 0
    new_entered_summa = float(summa) * float(request.form.get("rate_exchange"))
    if summa_to_delete:
        for summa_to_delete in summa_to_delete:
            final_sum = summa_to_delete.moneysum
            final_sum -= float(summa)
    else:
        if not summa_to_delete:
            inser_into_money_sum(0, user, currency_from, from_)
            final_sum = 0 - float(summa)
            summa_to_delete = get_to_sum(user, int(from_), currency_from)
            for _sum in summa_to_delete:
                summa_to_delete = _sum
    update_summa(
        summa_to_delete,
        final_sum,
        user,
        currency_from,
        from_,
        date,
        info,
        None,
        summa,
        None,
        None,
        True,
        False,
        False,
        False,
        pair,
        s["UUID"],
    )
    summa_to_add = get_to_sum(user, int(to_), currency_to)
    if summa_to_add:
        for summa_to_add in summa_to_add:
            summa_to_add.moneysum += float(new_entered_summa)
            update_summa(
                summa_to_add,
                summa_to_add.moneysum,
                user,
                currency_to,
                to_,
                date,
                info,
                new_entered_summa,
                None,
                None,
                None,
                True,
                False,
                False,
                False,
                pair,
                s["UUID"],
            )
    else:
        inser_into_money_sum(new_entered_summa, user, currency_to, int(to_))
        summa_to_update = get_to_sum(user, int(to_), currency_to)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=info,
                    addedsumma=str(new_entered_summa)
                               + " "
                               + request.form.get("valuta_buy"),
                    deletedsumma=None,
                    isexchanged=True,
                    ismoved=False,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=pair,
                    useridentificator=s["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def moving_command(form):
    pair = uuid.uuid4()
    sum_ = float(form.sum_.data)
    from_ = form.from_.data
    currency_from = int(form.currency_from.data)
    currency_to = int(form.currency_to.data)
    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")
    summa_to_delete = Moneysum.query.filter_by(
        user=user, wallet=int(from_), currency=currency_from
    ).all()
    info = form.info.data
    date = str(form.date.data)
    to_ = form.to_.data
    final_sum = 0
    code_from = get_current_currency(currency_from)
    currency_from = code_from.id
    code_to = get_current_currency(currency_to)
    currency_to = code_to.id
    new_entered_summa = sum_ * float(form.rate.data)
    if summa_to_delete:
        for summa_to_delete in summa_to_delete:
            final_sum = summa_to_delete.moneysum
            final_sum -= float(sum_)
    else:
        if not summa_to_delete:
            inser_into_money_sum(0, user, currency_from, from_)
            final_sum = 0 - float(sum_)
            summa_to_delete = get_to_sum(user, int(from_), currency_from)
            for _sum in summa_to_delete:
                summa_to_delete = _sum
    update_summa(
        summa_to_delete,
        final_sum,
        user,
        currency_from,
        from_,
        date,
        info,
        None,
        sum_,
        None,
        None,
        False,
        True,
        False,
        False,
        pair,
        s["UUID"],
    )
    summa_to_add = Moneysum.query.filter_by(
        user=user, wallet=int(to_), currency=currency_to
    ).all()
    if summa_to_add:
        for summa_to_add in summa_to_add:
            summa_to_add.moneysum += float(new_entered_summa)
            update_summa(
                summa_to_add,
                summa_to_add.moneysum,
                user,
                currency_to,
                to_,
                date,
                info,
                new_entered_summa,
                None,
                None,
                None,
                False,
                True,
                False,
                False,
                pair,
                s["UUID"],
            )
    else:
        inser_into_money_sum(new_entered_summa, user, currency_to, int(to_))
        summa_to_update = get_to_sum(user, int(to_), currency_to)
        currency_name = get_current_currency(currency_to).name
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=info,
                    addedsumma=str(new_entered_summa) + " " + currency_name,
                    deletedsumma=None,
                    isexchanged=False,
                    ismoved=True,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=pair,
                    useridentificator=s["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def reset_moneysum(status_id: int, identifier: int, summa: float):
    """
    This module updates summa when reset button is clicked
    :param status_id: id of status account
    :param identifier: id of summa
    :param summa: summa to update
    :return: new inserted data
    """

    from financial.service.accounts import delete_accountstatus

    changed = Moneysum.query.filter_by(id=identifier).first()
    changed.id = changed.id
    changed.user = changed.user
    changed.currency = changed.currency
    changed.wallet = changed.wallet
    changed.moneysum = changed.moneysum + summa
    database.session.add(changed)
    database.session.commit()
    delete_accountstatus(status_id)
