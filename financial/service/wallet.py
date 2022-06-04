from financial import database
from financial.models.userroot import Userroot
from financial.models.wallet import Accounts


def get_wallets():
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallets = Accounts.query.all()
    return [wallet.json() for wallet in wallets]


def get_wallet_list():
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallets = Accounts.query.all()
    return [wallet for wallet in wallets]




def get_current_wallet(identifier):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallet = Accounts.query.filter_by(id=identifier).first()
    return wallet.json() if wallet else None


def get_current_wallet_by_name(name):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallet = Accounts.query.filter_by(name=name.strip()).first()
    return wallet.id


def get_current_wallet_by_id(id):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    wallet = Accounts.query.filter_by(id=id).first()
    return wallet.name


def delete_wallet(identifier):
    """
    This module gets all wallets in database
    :return: list of wallets
    """
    Userroot.query.filter_by(walletname=identifier).delete()
    wallet = Accounts.query.get_or_404(identifier)
    database.session.delete(wallet)
    database.session.commit()


def insert_wallet(identifier: int, name: str, visibility: str):
    """
    This module insert new wallet into database
    :param identifier: wallet id
    :param name: name of wallet to add
    :return:
    """
    if visibility.strip() == "Да":
        visibility = "Общий"
    else:
        visibility = "Приватный"
    wallet = Accounts(identifier=identifier, name=name, visibility=visibility)
    database.session.add(wallet)
    database.session.commit()


def update_wallet(identifier: int, name: str, visibility: str) -> None:
    """
    This function is used to update an existing department
    :param identifier: the id of the department of hospital to update
    :param name: the name of the department of hospital to update
    :param to_do: the description of the department of hospital to update
    """
    wallet = Accounts.query.filter_by(id=identifier).first()
    wallet.name = name
    if visibility.strip() == "Да":
        visibility = "Общий"
    else:
        visibility = "Приватный"
    wallet.visibility = visibility
    wallet.id = identifier
    database.session.add(wallet)
    database.session.commit()
