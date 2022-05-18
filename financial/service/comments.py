import os

import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from financial.models.accountstatus import Accountstatus
from financial.models.moneysum import Moneysum
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.service.accounts import get_account_status_by_identifier
from financial.service.moneysum import reset_moneysum


def get_all_comments():
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    comments = []
    result = (
        session.query(
            Accountstatus.date,
            Accountstatus.comments,
            Accountstatus.addedsumma,
            Accountstatus.deletedsumma,
            Users.name,
            Accounts.name,
            Users.UUID,
            Accounts.visibility,
            Accountstatus.id,
            Accountstatus.number,
            Accountstatus.isexchanged,
            Accountstatus.ismoved
        )
            .join(Moneysum.userid)
            .join(Moneysum.accountinfo)
            .join(Moneysum.accountid)
            .order_by(desc(Accountstatus.id))
            .all()
    )
    if result:
        for details in result:
            transpone = list(details)
            comments.append(
                {
                    "id": transpone[8],
                    "date": transpone[0],
                    "comment": transpone[1],
                    "addedsumma": transpone[2],
                    "deletedsumma": transpone[3],
                    "user": transpone[4],
                    "wallet": transpone[5],
                    "UUID": transpone[6],
                    "visibility": transpone[7],
                    "number": transpone[9],
                    "exchanged": transpone[10],
                    'moved': transpone[11]
                }
            )
    return comments


def reset_summa(identifier):
    status = get_account_status_by_identifier(identifier)
    if status.deletedsumma is None:
        reset_moneysum(status.id, status.money, 0 - float(status.addedsumma.split()[0]))
    elif status.addedsumma is None:
        reset_moneysum(status.id, status.money, float(status.deletedsumma.split()[0]))
