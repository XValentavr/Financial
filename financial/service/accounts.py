import os

import sqlalchemy
from flask import session
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from financial.models.wallet import Accounts
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
    account_id = get_user.get("id")
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    checker = get_name_account_checker()
    for check in checker:
        if check.visibility == 'Приватный':
            result = (
                session.query(Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name)
                    .join(Moneysum.accountid)
                    .join(Moneysum.currencyid)
                    .filter(Moneysum.user == account_id, Accounts.visibility == check.visibility,
                            Accounts.name == check.name)
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
        elif check.visibility == 'Общий':
            result = (
                session.query(Moneysum.wallet, Accounts.name, Moneysum.moneysum, Currency.name)
                    .join(Moneysum.accountid)
                    .join(Moneysum.currencyid)
                    .filter(Accounts.visibility == check.visibility, Accounts.name == check.name).all()
            )
            summa_usd = 0
            summa_eur = 0
            summa_rub = 0
            summa_uah = 0
            for details in sorted(result):
                transpone = list(details)
                if transpone[3] == '$':
                    summa_usd += transpone[2]
                if transpone[3] == '€':
                    summa_eur += transpone[2]
                if transpone[3] == '₽':
                    summa_rub += transpone[2]
                if transpone[3] == '₴':
                    summa_uah += transpone[2]
            count_usd = count_uah = count_rub = count_eur = 0
            for details in sorted(result):
                transpone = list(details)
                if transpone[3] == '$' and count_usd == 0:
                    count_usd += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_usd) + " " + transpone[3],
                        }
                    )
                if transpone[3] == '€' and count_eur == 0:
                    count_eur += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_eur) + " " + transpone[3],
                        }
                    )
                if transpone[3] == '₽' and count_rub == 0:
                    count_rub += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_rub) + " " + transpone[3],
                        }
                    )
                if transpone[3] == '₴' and count_uah == 0:
                    count_uah += 1
                    dct_lst.append(
                        {
                            "id": transpone[0],
                            "account": transpone[1],
                            "money": str(summa_uah) + " " + transpone[3],
                        }
                    )

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
    user = get_user_by_UUID(session["UUID"].strip())
    user = user.get("id")
    summa = form.sum.data
    currency = form.currency.data
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
                    addedsumma=summa,
                    deletedsumma=None,
                )
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
    user = get_user_by_UUID(session["UUID"].strip()).get("id")
    summa = form.sum.data
    currency = form.currency.data
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
                    deletedsumma=summa,
                )
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


def get_name_account_checker():
    """
    This module gets account name of valuex
    :return: list of account name
    """
    result = Accounts.query.all()
    return [result for result in result]
