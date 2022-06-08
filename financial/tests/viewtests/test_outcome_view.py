from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestOutcomeView(ConfigurationTest):
    def test_outcome_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/outcome")
        self.assertEqual(401, response.status_code)

    def test_outcome_200(self):
        app = create_app()
        app.config["LOGIN_DISABLED"] = True
        app.login_manager.init_app(app)
        self.app = app.test_client()
        response = self.app.get("/outcome")
        self.assertEqual(200, response.status_code)
