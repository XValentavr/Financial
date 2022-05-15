from financial import database
from financial.models.accounts import Accounts


def get_wallets():
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallets = Accounts.query.all()
    return [wallet.json() for wallet in wallets]


def get_current_wallet(identifier):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallet = Accounts.query.filter_by(id=identifier).first()
    return wallet.json() if wallet else None


def delete_wallet(identifier):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallet = Accounts.query.get_or_404(identifier)
    database.session.delete(wallet)
    database.session.commit()


def insert_wallet(identifier: int, name: str):
    """
    This module insert new wallet into database
    :param identifier: wallet id
    :param name: name of wallet to add
    :return:
    """
    wallet = Accounts(identifier=identifier, name=name)
    database.session.add(wallet)
    database.session.commit()
