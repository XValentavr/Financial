import financial
from financial import database
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestWalletServie(ConfigurationTest):
    def test_get_wallets(self):
        """
        This module test get_wallet() method that returns json
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()

        wallets = Accounts.query.all()
        lst = []
        for w in wallets:
            lst.append({"id": w.id, "name": w.name, "visibility": w.visibility})
        self.assertTrue(isinstance(lst, list))
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_get_wallet_list(self):
        """
        This module test get_wallet_list() method that returns list
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()
        wallets = Accounts.query.all()
        self.assertTrue(isinstance(wallets, list))
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_get_current_wallet(self):
        """
        This module test get_current_wallet(identifier:int) method
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()
        wallets = Accounts.query.filter_by(id=2).all()

        self.assertEqual(1, len(wallets))
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_get_current_wallet_by_name(self):
        """
        This module test get_current_wallet_by_name(name:str) method
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()
        wallets = Accounts.query.filter_by(name="Мой кошелек").all()

        self.assertEqual(1, len(wallets))
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_get_current_wallet_by_id(self):
        """
        This module test get_current_wallet_by_id(id:int) method
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()
        wallets = Accounts.query.filter_by(id=2).first().name

        self.assertEqual("Мой кошелек1", wallets)
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_delete_wallet(self):
        """
        This module tests delete_wallet(identifier:int) methond
        """
        wallet1 = Accounts(1, "Мой кошелек", "Общий")
        wallet2 = Accounts(2, "Мой кошелек1", "Общий")
        database.session.add(wallet1)
        database.session.add(wallet2)
        database.session.commit()
        wallet = Accounts.query.get_or_404(2)
        database.session.delete(wallet)
        wallets = Accounts.query.all()

        self.assertEqual(len(wallets), 1)
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_insert_wallet(self):
        """
        This module tests insert_wallet(name:str,identifier:int,visibility:str) method
        """
        wallet = Accounts(identifier=1, name="Общак", visibility="Общий")
        database.session.add(wallet)
        database.session.commit()
        wallets = Accounts.query.all()

        self.assertEqual(1, len(wallets))
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_update_wallet(self):
        """
        This module tests update_wallet(name:str,identifier:int,visibility:str) method
        """
        wallet = Accounts(identifier=1, name="Общак", visibility="Общий")
        database.session.add(wallet)
        database.session.commit()
        wallets = Accounts.query.filter_by(name="Общак").first()
        wallets.name = "Кошелек"

        database.session.add(wallets)
        database.session.commit()

        wallets = Accounts.query.filter_by(name="Кошелек").first()
        self.assertTrue(isinstance(wallets, financial.models.wallet.Accounts))

        database.session.query(Accounts).delete()
        database.session.commit()
