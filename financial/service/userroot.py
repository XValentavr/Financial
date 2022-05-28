from financial import database
from financial.models.userroot import Userroot
from financial.service.users import get_all_user
from financial.service.wallet import get_wallet_list


def add_all_possible_pairs():
    """ "
    This module add all possible combination of users and wallets
    """
    users = get_all_user()
    wallets = get_wallet_list()
    for us in users:
        for wa in wallets:
            rts = Userroot.query.filter_by(username=us.id, walletname=wa.id).all()
            if rts:
                continue
            roots = Userroot(username=us.id, walletname=wa.id, isgeneral=0)
            database.session.add(roots)
            database.session.commit()


def update_roots(identifier: int, general: int, username=None):
    """
    This module updates  all users by wallet id if ALL checker is selected
    :param username: user unique identificator
    :param identifier: wallet identificator
    :return: None
    """
    if username is not None:
        roots = Userroot.query.filter_by(walletname=identifier, username=username).all()
    else:
        roots = Userroot.query.filter_by(walletname=identifier).all()
    for r in roots:
        r.isgeneral = general
        database.session.commit()


def get_user_root_id(username: int, walletname: int):
    """
    This function gets root id to chain to tables
    :param username: id of user
    :param walletname: id of wallet
    :return: int
    """
    root = Userroot.query.filter_by(username=walletname, walletname=username).first()
    return root.id


def get_user_root(username: int, walletname: int):
    """
    This function gets root id to chain to tables
    :param username: id of user
    :param walletname: id of wallet
    :return: int
    """
    return Userroot.query.filter_by(username=username, walletname=walletname).first()


def get_user_root_by_name_for_comments(username: int):
    """
    This function gets root id to chain to tables
    :param username: id of user
    :return: int
    """
    return Userroot.query.filter_by(username=username).all()
