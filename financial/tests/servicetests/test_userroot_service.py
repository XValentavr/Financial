import uuid

from werkzeug.security import generate_password_hash

from financial import database
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestUserrootService(ConfigurationTest):

    def test_get_user_root_by_name_for_comments(self):
        """
        This module test get_user_root_by_name_for_comments(name:str) function
        """
        wallet = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet)
        database.session.commit()

        user = Users('Valentyn', generate_password_hash('1234'), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        userroot = Userroot(98, 1, 1)
        database.session.add(userroot)
        database.session.commit()

        roots = Userroot.query.filter_by(username=98).first()

        self.assertEqual('<Userroot 32>', repr(roots))

        database.session.query(Accounts).delete()
        database.session.query(Userroot).delete()
        database.session.query(Users).delete()

        database.session.commit()

    def test_get_user_root(self):
        """
        This module test get_user_root(username:str,walletname:str) function
        """
        wallet = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet)
        database.session.commit()

        user = Users('Valentyn', generate_password_hash('1234'), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        userroot = Userroot(99, 1, 1)
        database.session.add(userroot)
        database.session.commit()

        roots = Userroot.query.filter_by(username=99, walletname=1).first()

        self.assertEqual('<Userroot 33>', repr(roots))

        database.session.query(Accounts).delete()
        database.session.query(Userroot).delete()
        database.session.query(Users).delete()

        database.session.commit()

    def test_get_user_root_id(self):
        """
        This module test get_user_root_id(username:str,wallentame:str) function
        """
        wallet = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet)
        database.session.commit()

        user = Users('Valentyn', generate_password_hash('1234'), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        userroot = Userroot(101, 1, 1)
        database.session.add(userroot)
        database.session.commit()

        roots = Userroot.query.filter_by(username=101, walletname=1).first().id

        self.assertEqual(35, roots)

        database.session.query(Accounts).delete()
        database.session.query(Userroot).delete()
        database.session.query(Users).delete()

        database.session.commit()

    def test_update_roots(self):
        """
        This module test update_roots(identifier: int, general: int, username=None) function
        """
        wallet = Accounts(1, 'Мой кошелек', 'Общий')
        database.session.add(wallet)
        database.session.commit()

        user = Users('Valentyn', generate_password_hash('1234'), uuid.uuid4())
        database.session.add(user)
        database.session.commit()

        userroot = Userroot(104, 1, 1)
        database.session.add(userroot)
        database.session.commit()

        roots = Userroot.query.filter_by(username=104).first()
        roots.isgeneral = 0
        database.session.add(roots)
        database.session.commit()

        roots = Userroot.query.filter_by(username=104).first().isgeneral
        self.assertFalse(roots)

        database.session.query(Accounts).delete()
        database.session.query(Userroot).delete()
        database.session.query(Users).delete()

        database.session.commit()
