from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestExchangeView(ConfigurationTest):
    def setUp(self):
        super(TestExchangeView, self).setUp()

    def test_exchange_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/exchange")
        self.assertEqual(401, response.status_code)
