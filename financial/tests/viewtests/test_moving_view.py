from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestMovingView(ConfigurationTest):

    def setUp(self):
        super(TestMovingView, self).setUp()

    def test_exchange_401(self):
        app = create_app()
        app.config['LOGIN_DISABLE'] = True
        app.login_manager.init_app(app)
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get('/exchange')
        self.assertEqual(401, response.status_code)
