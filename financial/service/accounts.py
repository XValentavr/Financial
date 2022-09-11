import datetime
import os
import uuid

import sqlalchemy
from flask import session as s
from sqlalchemy.orm import sessionmaker

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.service.currency import (
    get_list_currency,
    get_current_currency_by_name,
    get_current_currency,
)
from financial.service.moneysum import inser_into_money_sum, get_to_sum, update_summa
from financial.service.userroot import get_user_root
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
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
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
                .join(Moneysum.currencyid,
                      Moneysum.roots)
                .filter(
                    Moneysum.user == account_id,
                    Accounts.visibility == check.visibility,
                    Userroot.ispublic == 1
                    # Accounts.name == check.name,
                )
                .all()
            )
            if result:
                for details in sorted(result):
                    transpone = list(details)
                    dct_lst.append(
                        {
                            "account": transpone[1],
                            "money": str(transpone[2]) + " " + transpone[3],
                        }
                    )
        elif check.visibility == "Общий":
            user = get_user_by_UUID(s["UUID"].strip()).get("id")
            wallet = get_current_wallet_by_name(check.name)
            roots = get_user_root(user, wallet)
            if roots is not None:
                if roots.isgeneral:
                    result = (
                        session.query(
                            Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name
                        )
                        .join(Moneysum.accountid)
                        .join(Moneysum.currencyid)
                        .join(Moneysum.roots)
                        .filter(
                            Accounts.visibility == check.visibility,
                            Accounts.name == check.name,
                            # Moneysum.moneysum != 0.0,
                            Moneysum.user == Userroot.username,
                            Moneysum.wallet == Userroot.walletname,
                            Userroot.isgeneral == 1,
                            Userroot.ispublic == 1
                        )
                        .all()
                    )
                elif not roots.isgeneral:
                    usr = get_user_by_UUID(s["UUID"].strip()).get("id")
                    result = (
                        session.query(
                            Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name
                        )
                        .join(Moneysum.accountid)
                        .join(Moneysum.currencyid)
                        .join(Moneysum.roots)
                        .filter(
                            Accounts.visibility == check.visibility,
                            Accounts.name == check.name,
                            # Moneysum.moneysum != 0.0,
                            Moneysum.user == usr,
                            Moneysum.wallet == Userroot.walletname,
                            Userroot.isgeneral == 0,
                            Userroot.ispublic == 1
                        )
                        .all()
                    )
                for details in sorted(result):
                    transpone = list(details)
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(transpone[2]) + " " + transpone[3],
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
    date = str(form.date.data)
    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")
    summa = form.sum.data
    currency = form.currency.data
    currency_name = get_current_currency(currency).name
    summa_to_update = Moneysum.query.filter_by(
        user=user, wallet=int(wallet), currency=currency
    ).all()
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
                s["UUID"],
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
                    useridentificator=s["UUID"],
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
    date = str(form.date.data)
    user = get_user_by_UUID(s["UUID"].strip()).get("id")
    summa = form.sum.data
    currency = form.currency.data
    currency_name = get_current_currency(currency).name
    summa_to_update = Moneysum.query.filter_by(
        user=user, wallet=int(wallet), currency=currency
    ).all()
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
                s["UUID"],
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
                    useridentificator=s["UUID"],
                )
                database.session.add(accounts)
                database.session.commit()


def get_name_account():
    """
    This module gets account name of value
    :return: list of account name
    """

    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    session = sessionmaker(bind=engine)
    session = session()
    result = (
        session.query(
            Accounts.id, Accounts.name
        )
        .join(Userroot.walletid)
        .join(Userroot.userid)
        .filter(
            Users.UUID == s['UUID'],
            Userroot.ispublic == 1
        )
        .all()
    )

    return [(result.id, result.name) for result in result]


def get_name_account_checker():
    """
    This module gets account name of valuex
    :return: list of account name
    """
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    session = sessionmaker(bind=engine)
    session = session()
    result = (
        session.query(
            Accounts.id, Accounts.name, Accounts.visibility
        )
        .join(Userroot.walletid)
        .join(Userroot.userid)
        .filter(
            Users.UUID == s['UUID'],
            Userroot.ispublic == 1
        )
        .all()
    )
    return [result for result in result]


def merge_dict(dct_list: list) -> list:
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
    return res_dict


def restrict_dict(dct):
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
                    if c.name in d.keys():
                        d[c.name] += float(v.replace(f" {c.name}", ""))
                    else:
                        d[c.name] = float(v.replace(f" {c.name}", ""))
                    final.append(d)
    delete_if_zeros_more_than_2(dct, cur)
    delete_unused(dct)


def delete_unused(res_dict):
    for dct in res_dict:
        if 'id' in dct.keys():
            del dct['id']
        if 'money' in dct.keys():
            del dct['money']


def delete_if_zeros_more_than_2(money: dict, currency: list) -> None:
    """
    This nodule deletes if more then 2 zeros
    :param money: dict of money
    :param currency: currencies
    :return:
    """
    for m in money:
        zeros = 0
        for c in currency:
            mon = m.get(c.name)
            if mon is not None:
                if float('0.0') == float(mon):
                    zeros += 1
                    if zeros >= 2:
                        del m[c.name]


def check_keys(dct) -> None:
    """
    This module adds needed keys to user dict
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
    date = str(form.get("date"))
    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")
    wallet = get_current_wallet_by_name(wallet)
    print(summa)
    print(percent)
    if float(percent) > 0:
        summa = float(summa) - (float(summa) * (float(percent) / 100))
    else:
        summa = float(summa)
    summa_to_update = Moneysum.query.filter_by(
        user=user, wallet=int(wallet), currency=currency.id
    ).all()
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum += float(summa)
            update_summa(
                summa_to_update,
                summa_to_update.moneysum,
                user,
                currency.id,
                wallet,
                date,
                comments,
                summa,
                None,
                number,
                percent,
                False,
                False,
                False,
                False,
                pair,
                s["UUID"],
            )
    else:
        inser_into_money_sum(summa, user, currency.id, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency.id)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(
                    money=money,
                    date=date,
                    comments=comments,
                    addedsumma=str(summa) + " " + currency.name,
                    deletedsumma=None,
                    number=number,
                    percent=percent,
                    isexchanged=False,
                    ismoved=False,
                    ismodified=False,
                    isdeleted=False,
                    pairidentificator=pair,
                    useridentificator=s["UUID"],
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
    status.ismodified = s["UUID"]
    status.datedelete = datetime.datetime.now()
    database.session.add(status)
    database.session.commit()


def get_by_account_status(identifier):
    """
    this module gets wallet to choice in form
    :param identifier: id to find
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
