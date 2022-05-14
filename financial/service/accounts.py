import os

import sqlalchemy
from flask import session
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from financial.models.accounts import Accounts
from financial.models.accountstatus import Accountstatus
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.service.moneysum import inser_into_money_sum, get_to_sum, update_summa
from financial import database
from financial.service.users import get_user_by_UUID


def get_account_money(UUID: str):
    """
    This module get account status of user
    :param UUID: user
    :return: list of values
    """
    ...

    dct_lst = []
    get_user = get_user_by_UUID(UUID)
    account_id = get_user.id
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    session = sessionmaker(bind=engine)
    session = session()
    result = (session.query(
        Moneysum.wallet,
        Accounts.name,
        Moneysum.moneysum,
        Currency.name
    ).join(Moneysum.accountid)
              .join(Moneysum.currencyid)
              .filter(Moneysum.user == account_id).all()
              )
    for details in sorted(result):
        transpone = list(details)
        dct_lst.append({'id': transpone[0], 'account': transpone[1], 'money': str(transpone[2]) + ' ' + transpone[3]})
    return dct_lst


def insert_account(form):
    """
    This module add new value to account
    :param form: get data from form
    :return: none
    """
    wallet = form.wallet.data
    info = form.info.data
    date = form.date.data
    user = get_user_by_UUID(session["UUID"].strip()).id
    summa = form.sum.data
    currency = form.currency.data
    summa_to_update = get_to_sum(user, int(wallet), currency)
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum += float(summa)
            update_summa(
                summa_to_update, summa_to_update.moneysum, user, currency, wallet, date, info, summa, None
            )
    else:
        inser_into_money_sum(summa, user, currency, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(money=money, date=date, comments=info, addedsumma=summa, deletedsumma=None)
                database.session.add(accounts)
                database.session.commit()


def delete_data(form):
    """
    This module add new value to account
    :param form: get data from form
    :return: none
    """
    wallet = form.wallet.data
    info = form.info.data
    date = form.date.data
    user = get_user_by_UUID(session["UUID"].strip()).id
    summa = form.sum.data
    currency = form.currency.data
    summa_to_update = get_to_sum(user, int(wallet), currency)
    if summa_to_update:
        for summa_to_update in summa_to_update:
            summa_to_update.moneysum -= float(summa)
            added = None
            update_summa(
                summa_to_update, summa_to_update.moneysum, user, currency, wallet, date, info, added, summa
            )
    else:
        inser_into_money_sum(summa, user, currency, int(wallet))
        summa_to_update = get_to_sum(user, int(wallet), currency)
        if summa_to_update:
            for summa_to_update in summa_to_update:
                money = summa_to_update.id
                accounts = Accountstatus(money=money, date=date, comments=info, addedsumma=None, deletedsumma=summa)
                database.session.add(accounts)
                database.session.commit()


def get_name_account():
    """
    This module gets account name of valuex
    :return: list of account name
    """
    from financial import create_app

    with create_app().app_context():
        result = Accounts.query.all()
        return [(result.id, result.name) for result in result]
