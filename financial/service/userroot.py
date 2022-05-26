from financial import database
from financial.models.userroot import Userroot
from financial.service.users import get_all_user
from financial.service.wallet import get_wallet_list


def add_all_possible_pairs():
    database.session.query(Userroot).delete()
    database.session.commit()
    users = get_all_user()
    wallets = get_wallet_list()
    for us in users:
        for wa in wallets:
            roots = Userroot(username=us.id, walletname=wa.id, isgeneral=0)
            database.session.add(roots)
            database.session.commit()
