import uuid

from werkzeug.security import generate_password_hash

from financial import create_app, database
from financial.models.users import Users
from financial.tests.ConfigTests import ConfigurationTest


class TestAddUserView(ConfigurationTest):

    def test_add_401(self):
        app = create_app()
        # specify the database connection string
        self.app = app.test_client()
        response = self.app.get('/add')
        self.assertEqual(401, response.status_code)

    def test_add_200(self):
        app = create_app()
        app.config['LOGIN_DISABLED '] = True
        app.login_manager.init_app(app)
        response = app.test_client().get('/add')
        assert 200 == response.status_code

    def test_if_user_already_in(self):
        UUID = uuid.uuid4()
        user = Users('Valentyn', generate_password_hash('12345'), UUID)
        database.session.add(user)
        database.session.commit()

        users = Users.query.filter_by(id=72).first()

        self.assertEqual('<Users: Valentyn>', repr(users))
        responce = self.app.get('/add')
        self.assertEqual(401, responce.status_code)

    def test_if_not_in(self):
        users = Users.query.filter_by(id=100).first()

        self.assertEqual('None', repr(users))
        responce = self.app.get('/income')
        self.assertEqual(401, responce.status_code)
