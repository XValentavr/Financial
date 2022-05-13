from financial import database
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
