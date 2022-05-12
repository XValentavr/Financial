from financial.models.accountstatus import Accountstatus


def get_account_money(account_id: int):
    """
    This module get account status of user
    :param account_id: user
    :return: list of values
    """
    status = Accountstatus.query.filter_by(user=account_id).all()
    return [status.json() for status in status]
