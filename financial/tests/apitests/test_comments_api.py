import datetime
import time
import uuid

from werkzeug.security import generate_password_hash

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.currency import Currency
from financial.models.moneysum import Moneysum
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.tests.ConfigTests import ConfigurationTest


class TestGetAllComments(ConfigurationTest):

    def test_if_date_is_currect(self):
        """
        if insert date if currect then True else False
        :return: None
        """

        self.assertEqual(True, bool(time.strptime('1999/12/12', "%Y/%m/%d")))

    def test_get_all_comments(self):
        """
        Tests get all comments. If currect then 200
        :return: None
        """
        stts = Accountstatus.query.all()
        self.assertEqual([], stts)

        cur = Currency('UAH')
        database.session.add(cur)
        database.session.commit()

        acc = Accounts(1, 'Кошелек', 'Общий ')
        database.session.add(acc)
        database.session.commit()

        usr = Users('Valentyn', generate_password_hash('12345'), uuid.uuid4())
        database.session.add(usr)
        database.session.commit()

        userroot = Userroot(62, 1, True)
        database.session.add(userroot)
        database.session.commit()

        money = Moneysum(
            wallet=1, moneysum=200, user=62, currency=37, isgeneral=26
        )
        database.session.add(money)
        database.session.commit()

        status = Accountstatus(
            money=22,
            date=datetime.datetime.now(),
            comments='Hello',
            addedsumma=str(200) + " " + 'UAH',
            deletedsumma=None,
            number=None,
            percent=None,
            isexchanged=False,
            ismoved=False,
            ismodified=False,
            isdeleted=False,
            pairidentificator=uuid.uuid4(),
            useridentificator=uuid.uuid4(),
        )

        database.session.add(status)
        database.session.commit()

        stts = Accountstatus.query.all()
        self.assertEqual(1, len(stts))
