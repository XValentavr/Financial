from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestPayView(ConfigurationTest):
    def test_pay_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/pay")
        self.assertEqual(401, response.status_code)

    def test_pay_200(self):
        app = create_app()
        app.config["LOGIN_DISABLED"] = True
        app.login_manager.init_app(app)
        self.app = app.test_client()
        response = self.app.get("/outcome")
        self.assertEqual(200, response.status_code)

    def test_pay_404(self):
        """
        Assert if page is not found
        :return: None
        """
        app = create_app()
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess["superuser"] = False

        self.assertEqual(False, sess["superuser"])

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess["superuser"] = True
        self.assertEqual(True, sess["superuser"])
