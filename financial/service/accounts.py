import os

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from financial.models.accounts import Accounts
from financial.models.accountstatus import Accountstatus
from financial.service.users import get_user_by_UUID


def get_account_money(UUID: str):
    """
    This module get account status of user
    :param UUID: user
    :return: list of values
    """
    dct_lst = []
    get_user = get_user_by_UUID(UUID)
    account_id = get_user.id
    engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    session = sessionmaker(bind=engine)
    session = session()
    result = (session.query(
        Accounts.name,
        func.sum(Accountstatus.money).label("money")
    ).join(Accountstatus.accountid)
              .filter(Accountstatus.user == account_id)
              .group_by(Accountstatus.account).all()
              )
    for details in result:
        transpone = list(details)
        dct_lst.append({'account': transpone[0], 'money': transpone[1]})
    return dct_lst
