from financial import create_app
from financial.tests.ConfigTests import ConfigurationTest


class TestResetCommentsView(ConfigurationTest):

    def setUp(self):
        super(TestResetCommentsView, self).setUp()

    def test_reset_401(self):
        app = create_app()
        app.config['LOGIN_DISABLE'] = True
        app.login_manager.init_app(app)
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get('comments/edit/8b4ac183-8e0a-4a38-8d6f-08229e1398b7')
        self.assertEqual(401, response.status_code)
