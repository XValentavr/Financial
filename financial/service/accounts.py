from financial.models.accounts import Accounts
from financial.models.accountstatus import Accountstatus
from financial.service.moneysum import inser_into_money_sum, get_to_sum, update_summa
from financial import database


def get_account_money(UUID: str):
    """
    This module get account status of user
    :param UUID: user
    :return: list of values
    """
    ...


""" dct_lst = []
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
 return dct_lst"""


def insert_account(
    form, summa: float, currency: str, wallet: str, info: str, date: str, user: int
):
    """
    This module add new value to account
    :param summa: summa of transaction
    :param currency: currency on transaction
    :param wallet: wallet to add
    :param info: information about
    :param date: date of add
    :param user: user to add
    :return: none
    """
    symbol = dict(form.currency.choices)[int(form.currency.data)]
    currency = form.currency.data
    summas = get_to_sum(user, wallet, currency)
    if summas:
        for summas in summas:
            summas.moneysum += float(summa)
            update_summa(
                summas, summas.moneysum, user, currency, wallet, date, info, summa
            )
    else:
        inser_into_money_sum(summa, user, currency, wallet)
        accounts = Accountstatus(money=85, date=date, comments=info, addedsumma=summa)
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
