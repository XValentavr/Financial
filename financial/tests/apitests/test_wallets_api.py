
from financial import database
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestAllWalletsApi(ConfigurationTest):

    def test_get_all_wallets(self):
        """
        This module test if wallets are in database
        :return: None
        """
        wallet_1 = Accounts(1, 'Мой кошелек', 'Общий')
        wallet_2 = Accounts(2, 'Мой кошелек1', 'Общий')
        database.session.add(wallet_1)
        database.session.add(wallet_2)
        database.session.commit()
        response = self.app.get('/api/wallets')
        self.assertEqual(200, response.status_code)
        database.session.query(Accounts).delete()
        database.session.commit()


class TestSingleWallet(ConfigurationTest):

    def test_get_single_wallet(self):
        """
        This module tests get single wallet
        :return:None
        """
        wallet_1 = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet_1)
        database.session.commit()
        response = self.app.get('/api/wallets/1')
        self.assertEqual(200, response.status_code)
        response = self.app.get('/api/wallets/200')
        self.assertEqual(404, response.status_code)
        database.session.query(Accounts).delete()
        database.session.commit()

    def test_delete_single_wallet(self):
        """
        This module tests delete api command
        :return: None
        """
        wallet_1 = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet_1)
        database.session.commit()
        responce = self.app.delete('/api/wallets/1')
        self.assertEqual(200, responce.status_code)
        responce = self.app.delete('/api/wallets/10')
        self.assertEqual(404, responce.status_code)

