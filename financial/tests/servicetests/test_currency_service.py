from financial import database
from financial.models.currency import Currency
from financial.tests.ConfigTests import ConfigurationTest


class TestCurrencyService(ConfigurationTest):
    def test_get_currency(self):
        """
        This module test get_currency() function
        """
        cur1 = Currency("UAH")
        database.session.add(cur1)
        database.session.commit()

        currency = Currency.query.filter_by(name="UAH").all()
        lst = [(currency.id, currency.name) for currency in currency]
        self.assertEqual([(55, "UAH")], lst)
        database.session.query(Currency).delete()
        database.session.commit()

    def test_get_current_currency(self):
        """
        This module test get_current_currency(identifier:int) function
        """
        cur1 = Currency("UAH")
        cur2 = Currency("UAH1")
        database.session.add(cur1)
        database.session.add(cur2)
        database.session.commit()

        currency = Currency.query.filter_by(id=50).first()
        self.assertEqual("<Currency 50>", repr(currency))
        database.session.query(Currency).delete()
        database.session.commit()

    def test_get_current_currency_by_name(self):
        """
        This module tests get_current_currency_by_name(name:str) function
        """
        cur1 = Currency("UAH")
        cur2 = Currency("UAH1")
        database.session.add(cur1)
        database.session.add(cur2)
        database.session.commit()

        currency = Currency.query.filter_by(name="UAH1").first()
        self.assertEqual("<Currency 43>", repr(currency))
        database.session.query(Currency).delete()
        database.session.commit()

    def test_get_list_currency(self):
        """
        This module tests get_list_currency() function
        """
        cur1 = Currency("UAH")
        cur2 = Currency("UAH1")
        database.session.add(cur1)
        database.session.add(cur2)
        database.session.commit()

        currency = Currency.query.all()

        self.assertEqual(2, len(currency))

        database.session.query(Currency).delete()
        database.session.commit()
