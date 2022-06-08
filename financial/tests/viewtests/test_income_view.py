from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestIncomeView(ConfigurationTest):
    def setUp(self):
        super(TestIncomeView, self).setUp()

    def test_income_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/income")
        self.assertEqual(401, response.status_code)

    def test_income_200(self):
        app = create_app()
        app.config["LOGIN_DISABLED"] = True
        app.login_manager.init_app(app)
        self.app = app.test_client()
        response = self.app.get("/income")
        self.assertEqual(200, response.status_code)
