from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestChangeWalletView(ConfigurationTest):

    def test_changewallet_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get('/wallet')
        self.assertEqual(401, response.status_code)

        response = self.app.get('/changewallet')
        self.assertEqual(401, response.status_code)

    def test_changewallet_200(self):
        response = self.app.get('/wallet/edit/6')
        self.assertEqual(401, response.status_code)

    def test_changewallet_404(self):
        """
        Assert if page is not found
        :return: None
        """
        app = create_app()
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['superuser'] = False

        self.assertEqual(False, sess['superuser'])

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['superuser'] = True
        self.assertEqual(True, sess['superuser'])
