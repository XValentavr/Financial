from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestWalletView(ConfigurationTest):
    def test_wallet_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/walletinfo/Мой%20кошелек")
        self.assertEqual(401, response.status_code)

    def test_income_404(self):
        """
        Assert if page is not found
        :return: None
        """
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/walletinfo/Мой%20кошелек23415")
        self.assertEqual(404, response.status_code)
