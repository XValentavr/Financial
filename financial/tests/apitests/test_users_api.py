import uuid

from werkzeug.security import generate_password_hash

from financial import database
from financial.models.users import Users
from financial.tests.ConfigTests import ConfigurationTest


class TestAllUsersApi(ConfigurationTest):

    def test_abort(self):
        """
        This function tests if user exists
        :return: None
        """
        user = Users('Valentyn', generate_password_hash('12345'), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        user = Users.query.filter_by(id=42).first()
        self.assertEqual('<Users: Valentyn>', repr(user))

        database.session.query(Users).delete()
        database.session.commit()

        user = Users.query.filter_by(id=42).first()
        self.assertEqual(None, user)

    def test_get_users(self):
        """
        This module tests get all users
        :return: None
        """
        user = Users('Valentyn', generate_password_hash('12345'), uuid.uuid4())
        user1 = Users('Valentyn1', generate_password_hash('12345'), uuid.uuid4())
        database.session.add(user)
        database.session.add(user1)
        database.session.commit()

        users = Users.query.all()
        self.assertEqual(2, len(users))

        database.session.query(Users).delete()
        database.session.commit()


class TestSingleUser(ConfigurationTest):

    def test_get_uuid(self):
        """
        This module tests get user by UUID
        :return: None
        """

        UUID = uuid.uuid4()
        user = Users('Valentyn', generate_password_hash('12345'), UUID)
        database.session.add(user)
        database.session.commit()

        user = Users.query.filter_by(UUID=UUID).first()
        self.assertEqual('<Users: Valentyn>', repr(user))

        user2 = Users.query.filter_by(UUID=uuid.uuid4()).first()
        self.assertEqual(None, user2)

        database.session.query(Users).delete()
        database.session.commit()

    def test_delete_user(self):
        """
        This module tests delete user command
        :return: None
        """
        UUID = uuid.uuid4()
        user = Users('Valentyn', generate_password_hash('12345'), UUID)
        database.session.add(user)
        database.session.commit()

        responce = self.app.delete('/api/users/1')
        self.assertEqual(200, responce.status_code)
        responce = self.app.delete('/api/users/50')
        self.assertEqual(404, responce.status_code)

        database.session.query(Users).delete()
        database.session.commit()
