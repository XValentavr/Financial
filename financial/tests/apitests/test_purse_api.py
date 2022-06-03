import uuid

from werkzeug.security import generate_password_hash

from financial import database
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestPurse(ConfigurationTest):

    def test_abort(self):
        """
        This module test if wallets are in database
        :return:
        """
        purse = Moneysum.query.filter_by(user=1).all()
        self.assertEqual([], purse)

        cur = Currency('UAH')
        database.session.add(cur)
        database.session.commit()

        acc = Accounts(1, 'Кошелек', 'Общий ')
        database.session.add(acc)
        database.session.commit()

        usr = Users('Valentyn', generate_password_hash('12345'), uuid.uuid4())
        database.session.add(usr)
        database.session.commit()

        userroot = Userroot(1, 1, True)
        database.session.add(userroot)
        database.session.commit()

        money = Moneysum(
            wallet=1, moneysum=200, user=1, currency=1, isgeneral=1
        )
        database.session.add(money)
        database.session.commit()

        purse = Moneysum.query.filter_by(user=1).all()
        self.assertEqual(1, len(purse))

        database.session.query(Currency).delete()
        database.session.commit()

        database.session.query(Accounts).delete()
        database.session.commit()

        database.session.query(Users).delete()
        database.session.commit()

        database.session.query(Moneysum).delete()
        database.session.commit()

        database.session.query(Userroot).delete()
        database.session.commit()
