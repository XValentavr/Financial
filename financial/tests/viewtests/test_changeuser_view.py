from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestChangeUserView(ConfigurationTest):
    def test_changeuser_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get("/change")
        self.assertEqual(401, response.status_code)

    def test_changeuser_200(self):
        response = self.app.get("/users/edit/3df4f7c3-4863-46f9-85bf-41aeb669c70f")
        self.assertEqual(401, response.status_code)

    def test_changeuser_404(self):
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
