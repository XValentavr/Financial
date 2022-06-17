import uuid

from werkzeug.security import generate_password_hash

from financial import database
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestMoneysumService(ConfigurationTest):

    def test_reset_moneysum(self):
        """
        This module tests reset_moneysum(status_id: int, identifier: int, summa: float)
        function
        :return:None
        """
        cur = Currency("UAH")
        database.session.add(cur)
        database.session.commit()

        acc = Accounts(1, "Кошелек", "Общий ")
        database.session.add(acc)
        database.session.commit()

        usr = Users("Valentyn", generate_password_hash("12345"), uuid.uuid4())
        database.session.add(usr)
        database.session.commit()

        userroot = Userroot(115, 1, True)
        database.session.add(userroot)
        database.session.commit()

        money = Moneysum(wallet=1, moneysum=200, user=115, currency=67, isgeneral=48)
        database.session.add(money)
        database.session.commit()

        moneysum = Moneysum.query.filter_by(user=115, wallet=1).first()
        moneysum = moneysum.moneysum + 100
        self.assertEqual(300, moneysum)

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
