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


def get_to_sum(user: int, wallet: str, currency: int):
    """
    This module gets to sum
    :param user: user id
    :param wallet: wallet id
    :param currency: currency of value
    :return:
    """
    money = Moneysum.query.filter_by(user=user, wallet=wallet, currency=currency).all()
    return money


def update_summa(summas, summa, user, currency, wallet, date, info, s_add) -> None:
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
    :return: None
    """
    if int(summas.wallet) != int(wallet) and int(summas.currency) != int(currency):
        inser_into_money_sum(summa, user, currency, wallet)
        accounts = Accountstatus(
            money=summas.id, date=date, comments=info, addedsumma=s_add
        )
        database.session.add(accounts)
        database.session.commit()
    else:
        summas.moneysum = summa
        database.session.add(summas)
        database.session.commit()
        accounts = Accountstatus(
            money=summas.id, date=date, comments=info, addedsumma=s_add
        )
        database.session.add(accounts)
        database.session.commit()
