import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from financial import database
from financial.models.users import Users, SuperUser
from financial.tests.ConfigTests import ConfigurationTest


class TestUserService(ConfigurationTest):
    def test_get_user_by_enter_name(self):
        """
        This function test get_user_by_name(name:str) function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        users = Users.query.filter_by(name="Valentyn").first()

        self.assertEqual("<Users: Valentyn>", repr(users))

        database.session.query(Users).delete()
        database.session.commit()

    def test_get_user_by_name(self):
        """
        This module test get_user_by_name(name:str,password:str) function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        users = Users.query.filter_by(name="Valentyn").first()

        self.assertEqual("<Users: Valentyn>", repr(users))
        self.assertTrue(check_password_hash(users.password, "12345"))
        database.session.query(Users).delete()
        database.session.commit()

    def test_get_all_user(self):
        """
        This module test get_all_user() function
        """
        user1 = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        user2 = Users("Valentyn2", generate_password_hash("12345"), uuid.uuid4())
        database.session.add(user1)
        database.session.add(user2)
        database.session.commit()
        users = Users.query.all()

        self.assertEqual(2, len(users))

        database.session.query(Users).delete()
        database.session.commit()

        users = Users.query.all()
        self.assertListEqual([], users)

    def test_get_super_user_by_name(self):
        """
        Thins module tests get_super_user_by_name(username:str) function
        """
        suser = SuperUser("Valentyn", generate_password_hash("1234"), uuid.uuid4(), 81)

        database.session.add(suser)
        database.session.commit()

        suser = SuperUser.query.filter_by(name="Valentyn").all()

        self.assertEqual(1, len(suser))
        database.session.query(SuperUser).delete()
        database.session.query(Users).delete()
        database.session.commit()
        suser = SuperUser.query.filter_by(name="Valentyn").all()

        self.assertListEqual([], suser)

    def test_user_by_UUID(self):
        """
        This module tests get_yser_by_UUID(UUID:str) function
        """
        UUID = uuid.uuid4()
        user = Users("Valentyn", generate_password_hash("12345"), UUID)

        database.session.add(user)
        database.session.commit()

        user = Users.query.filter_by(UUID=UUID).first()

        self.assertEqual("<Users: Valentyn>", repr(user))
        database.session.query(Users).delete()
        database.session.commit()

    def test_get_user_by_id(self):
        """
        This module test get_user_by_id(identifier:int) function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())

        database.session.add(user)
        database.session.commit()

        user = Users.query.filter_by(id=84).first()

        self.assertEqual("<Users: Valentyn>", repr(user))
        database.session.query(Users).delete()
        database.session.commit()

    def test_add_user(self):
        """
        This module tests add_user() function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        user2 = Users("Valentyn1", generate_password_hash("12345"), uuid.uuid4())
        user3 = Users("Valentyn2", generate_password_hash("12345"), uuid.uuid4())

        database.session.add(user)
        database.session.add(user2)
        database.session.add(user3)

        database.session.commit()

        user = Users.query.all()

        self.assertEqual(3, len(user))
        database.session.query(Users).delete()
        database.session.commit()

    def test_delete_user(self):
        """
        This module test delete_user() function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        user2 = Users("Valentyn1", generate_password_hash("12345"), uuid.uuid4())
        user3 = Users("Valentyn2", generate_password_hash("12345"), uuid.uuid4())

        database.session.add(user)
        database.session.add(user2)
        database.session.add(user3)

        database.session.commit()
        user = Users.query.filter_by(name="Valentyn2").first()
        database.session.delete(user)
        database.session.commit()

        user = Users.query.all()

        self.assertEqual(2, len(user))
        database.session.query(Users).delete()
        database.session.commit()

    def test_update_user(self):
        """
        This module test update_user() function
        """
        user = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())

        database.session.add(user)
        database.session.commit()

        user = Users.query.filter_by(name="Valentyn").first()
        user.name = "Valentyn12345"
        database.session.add(user)
        database.session.commit()

        user = Users.query.first()

        self.assertEqual("<Users: Valentyn12345>", repr(user))
        database.session.query(Users).delete()
        database.session.commit()
