import os

import requests
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.moneysum import Moneysum


def inser_into_money_sum(money: float, user: int, currency: int, wallet: int):
    """
    This module inserts data to moneysum
    :param money: money to enter
    :param user: user of transaction
    :param currency: currency of transaction
    :return:
    """
    money = Moneysum(wallet=wallet, moneysum=money, user=user, currency=currency)
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
        return money
    return None


def update_summa(
        summas, summa, user, currency, wallet, date, info, s_add, s_delete
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
    if int(summas.wallet) != int(wallet) and int(summas.currency) != int(currency):
        inser_into_money_sum(summa, user, currency, wallet)
        accounts = Accountstatus(
            money=summas.id,
            date=date,
            comments=info,
            addedsumma=s_add,
            deletedsumma=s_delete,
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
            addedsumma=s_add,
            deletedsumma=s_delete,
        )
        database.session.add(accounts)
        database.session.commit()


def exchange_rate(valuta: str):
    """
    This module gets currency rate onlina
    :param valuta: valluta to get rate
    :return: dict of acrual currency
    """
    url = f"https://v6.exchangerate-api.com/v6/727a8cafbfa682e3187bc8ab/latest/{valuta}"
    response = requests.get(url)
    return response.json()


def get_count_users(identifier: int):
    """
    This module gets users wallet group by wallets
    :return: list of number of wallets
    """
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    with session as session:
        result = session.query(Moneysum.wallet, func.count(Moneysum.wallet)).filter_by(wallet=identifier).group_by(
            Moneysum.wallet).all()
    res_list = []
    if result:
        res_list.append(list(result[0]))
    return res_list


def get_new_transfered_sum(
        sum_: float, currency_from: float, currency_to: float
) -> float:
    """
    This module exchange valuta
    :param sum_: summa to exchange
    :param currency_from: from exchange
    :param currency_to: to exchage
    :return: new summa
    """
    final_sum = 0
    if currency_from == 1 and currency_to == 2:
        rate = exchange_rate("USD")
        exchange = rate["conversion_rates"].get("EUR")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 1 and currency_to == 3:
        rate = exchange_rate("USD")
        exchange = rate["conversion_rates"].get("RUB")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 1 and currency_to == 4:
        rate = exchange_rate("USD")
        exchange = rate["conversion_rates"].get("UAH")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 2 and currency_to == 1:
        rate = exchange_rate("EUR")
        exchange = rate["conversion_rates"].get("USD")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 2 and currency_to == 3:
        rate = exchange_rate("EUR")
        exchange = rate["conversion_rates"].get("RUB")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 2 and currency_to == 4:
        rate = exchange_rate("EUR")
        exchange = rate["conversion_rates"].get("UAH")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 3 and currency_to == 1:
        rate = exchange_rate("RUB")
        exchange = rate["conversion_rates"].get("USD")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 3 and currency_to == 2:
        rate = exchange_rate("RUB")
        exchange = rate["conversion_rates"].get("EUR")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 3 and currency_to == 4:
        rate = exchange_rate("RUB")
        exchange = rate["conversion_rates"].get("UAH")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 4 and currency_to == 1:
        rate = exchange_rate("UAH")
        exchange = rate["conversion_rates"].get("USD")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 4 and currency_to == 2:
        rate = exchange_rate("UAH")
        exchange = rate["conversion_rates"].get("EUR")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    elif currency_from == 4 and currency_to == 3:
        rate = exchange_rate("UAH")
        exchange = rate["conversion_rates"].get("EUR")
        new_entered_summa = round(sum_ * exchange, 2)
        final_sum = new_entered_summa
    return final_sum
