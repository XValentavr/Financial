import datetime
import os
import uuid

import sqlalchemy
from flask import session
from sqlalchemy.orm import sessionmaker

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.models.wallet import Accounts
from financial.service.currency import (
    get_list_currency,
    get_current_currency_by_name,
    get_current_currency,
)
from financial.service.moneysum import inser_into_money_sum, get_to_sum, update_summa
from financial.service.users import get_user_by_UUID
from financial.service.wallet import get_current_wallet_by_name


def get_account_money(UUID: str):
    """
    This module get account status of user
    :param UUID: user
    :return: list of values
    """
    ...

    dct_lst = []
    get_user = get_user_by_UUID(UUID)
    account_id = get_user.get("id")
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    checker = get_name_account_checker()
    for check in checker:
        if check.visibility == "Приватный":
            result = (
                session.query(
                    Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name
                )
                    .join(Moneysum.accountid)
                    .join(Moneysum.currencyid)
                    .filter(
                    Moneysum.user == account_id,
                    Accounts.visibility == check.visibility,
                    Accounts.name == check.name,
                    Moneysum.moneysum != 0.0
                )
                    .all()
            )
            if result:
                for details in sorted(result):
                    transpone = list(details)
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(transpone[2]) + " " + transpone[3],
                        }
                    )
        elif check.visibility == "Общий":
            result = (
                session.query(
                    Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name
                )
                    .join(Moneysum.accountid)
                    .join(Moneysum.currencyid)
                    .filter(
                    Accounts.visibility == check.visibility, Accounts.name == check.name, Moneysum.moneysum != 0.0
                )
                    .all()
            )
            summa_usd = summa_eur = summa_uah = summa_zlt = 0
            for details in sorted(result):
                transpone = list(details)
                if transpone[3] == "USD":
                    summa_usd += transpone[2]
                if transpone[3] == "EUR":
                    summa_eur += transpone[2]
                if transpone[3] == "UAH":
                    summa_uah += transpone[2]
                if transpone[3] == "PLN":
                    summa_zlt += transpone[2]
            count_usd = count_uah = count_eur = count_pln = 0
            for details in sorted(result):
                transpone = list(details)
                if transpone[3] == "USD" and count_usd == 0:
                    count_usd += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_usd) + " " + transpone[3],
                        }
                    )
                if transpone[3] == "EUR" and count_eur == 0:
                    count_eur += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_eur) + " " + transpone[3],
                        }
                    )
                if transpone[3] == "UAH" and count_uah == 0:
                    count_uah += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_uah) + " " + transpone[3],
                        }
                    )
                if transpone[3] == "PLN" and count_pln == 0:
                    count_pln += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_zlt) + " " + transpone[3],
                        }
                    )
    return merge_dict(dct_lst)


def insert_account(form):
    """
    This module add new value to account
    :param form: get data from form
    :return: none
    """
    identificaator = uuid.uuid4()
    wallet = form.wallet.data
    info = form.info.data
    date = str(form.date.data) + " " + str(datetime.datetime.now().time())
    user = get_user_by_UUID(session["UUID"].strip())
    user = user.get("id")
    summa = form.sum.data
    currency = form.currency.data
    currency_name = get_current_currency(currency).name
    summa_to_update = get_to_sum(user, int(wallet), currency)
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum += float(summa)
            update_summa(
                summa_to_update,
                summa_to_update.moneysum,
                user,
                currency,
                wallet,
                date,
                info,
                summa,
                None,
                None,
                None,
                False,
                False,
                False,
                False,
                identificaator,
                session["UUID"],
            )
    else:
        inser_into_money_sum(summa, user, currency, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=info,
                    addedsumma=str(summa) + " " + currency_name,
                    deletedsumma=None,
                    number=None,
                    percent=None,
                    isexchanged=False,
                    ismoved=False,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=identificaator,
                    useridentificator=session["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def delete_data(form):
    """
    This module add new value to account
    :param form: get data from form
    :return: none
    """
    identificator = uuid.uuid4()
    wallet = form.wallet.data
    info = form.info.data
    date = str(form.date.data) + " " + str(datetime.datetime.now().time())
    user = get_user_by_UUID(session["UUID"].strip()).get("id")
    summa = form.sum.data
    currency = form.currency.data
    currency_name = get_current_currency(currency).name
    summa_to_update = get_to_sum(user, int(wallet), currency)
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum -= float(summa)
            added = None
            update_summa(
                summa_to_update,
                summa_to_update.moneysum,
                user,
                currency,
                wallet,
                date,
                info,
                added,
                summa,
                None,
                None,
                False,
                False,
                False,
                False,
                identificator,
                session["UUID"],
            )
    else:
        summa = 0 - int(summa)
        inser_into_money_sum(summa, user, currency, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=info,
                    addedsumma=None,
                    deletedsumma=str(abs(summa)) + " " + currency_name,
                    isexchanged=False,
                    ismoved=False,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=identificator,
                    useridentificator=session["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def get_name_account():
    """
    This module gets account name of value
    :return: list of account name
    """
    from financial import create_app

    with create_app().app_context():
        result = Accounts.query.all()
        return [(result.id, result.name) for result in result]


def get_name_account_checker():
    """
    This module gets account name of valuex
    :return: list of account name
    """
    result = Accounts.query.all()
    return [result for result in result]


def merge_dict(dct_list: list[dict]) -> list[dict]:
    """
    This module merges valuta on the sample wallet
    :param dct_list: dict to check and merge
    :return: new merged dict
    """
    res_dict = []
    for dct in dct_list:
        if not res_dict:
            res_dict.append(dct)
        else:
            for d in res_dict:
                if d["account"] == dct["account"]:
                    d["money"] = d["money"] + ", " + dct["money"]
                    break
            else:
                res_dict.append(dct)
    restrict_dict(res_dict)
    check_keys(res_dict)
    return res_dict


def restrict_dict(dct: list[dict]):
    """
    Thid module changes data in money key
    :param dct: dict to change
    :return: final transformed dict
    """
    final = []
    cur = get_list_currency()
    for c in cur:
        for d in dct:
            valuta = d.get("money").split(", ")
            for v in valuta:
                if c.name in v:
                    d[c.name] = v.replace(f" {c.name}", "")
                    final.append(d)


def check_keys(dct: list[dict]) -> None:
    """
    This module adds needed keys to yser dict
    :param dct: dict to add keys
    :return: None
    """
    cur = get_list_currency()
    for c in cur:
        for d in dct:
            if c.name not in d.keys():
                continue


def insert_pay_account(form):
    """
    This module add new value to account
    :param form: get data from form
    :return: none
    """
    pair = uuid.uuid4()
    number = form.get("number")
    percent = form.get("percent")
    wallet = form.get("wallet")
    summa = form.get("summa")
    comments = form.get("comments")
    currency = form.get("valuta")
    currency = get_current_currency_by_name(currency)
    date = str(form.get("date")) + " " + str(datetime.datetime.now().time())
    user = get_user_by_UUID(session["UUID"].strip())
    user = user.get("id")
    wallet = get_current_wallet_by_name(wallet)
    if int(percent) > 0:
        summa = int(summa) - (int(summa) * (int(percent) / 100))
    else:
        summa = int(summa)
    summa_to_update = get_to_sum(user, int(wallet), currency.id)
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum -= float(summa)
            update_summa(
                summa_to_update,
                summa_to_update.moneysum,
                user,
                currency.id,
                wallet,
                date,
                comments,
                None,
                summa,
                number,
                percent,
                False,
                False,
                False,
                False,
                pair,
                session["UUID"],
            )
    else:
        inser_into_money_sum(0 - summa, user, currency.id, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency.id)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=comments,
                    addedsumma=None,
                    deletedsumma=str(summa) + " " + currency.name,
                    number=number,
                    percent=percent,
                    isexchanged=False,
                    ismoved=False,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=pair,
                    useridentificator=session["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def get_account_status_by_identifier(identifier):
    status = Accountstatus.query.filter_by(id=identifier).first()
    return status


def delete_accountstatus(identifier: int):
    """
    This module deletes history by id
    :param identifier: id of history
    :return: new changed database
    """
    status = Accountstatus.query.get_or_404(identifier)
    status.isdeleted = True
    status.ismodified = session["UUID"]
    database.session.add(status)
    database.session.commit()


def get_by_account_status(identifier):
    """
    this module gets wallet to choice in form
    :param identifier: id to find
    :return:
    """
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    result = (
        session.query(Accounts.name)
            .join(Moneysum.accountid)
            .filter(Moneysum.id == identifier)
            .first()
    )
    return result


def get_pair(identifier: int):
    """
    This module gets pair identificator
    :param identifier:
    :return:
    """
    changed = Accountstatus.query.filter_by(id=identifier).first()
    return changed.pairidentificator


def get_by_pair(pairid: str):
    """
    To get accounts using pair
    :param pairid: pair identificator
    :return: list of accounts
    """
    accs = Accountstatus.query.filter_by(pairidentificator=pairid).all()
    return [p for p in accs]
