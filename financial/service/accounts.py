from collections import Counter, defaultdict

from funcy import join_with

from financial.models.accountstatus import Accountstatus
from financial.service.users import get_user_by_UUID


def get_account_money(UUID: str):
    """
    This module get account status of user
    :param UUID: user
    :return: list of values
    """
    dct = {}
    get_user = get_user_by_UUID(UUID)
    account_id = get_user.id
    status = Accountstatus.query.filter_by(user=account_id).all()
    return [status.json() for status in status]
