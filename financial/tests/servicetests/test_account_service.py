from financial.tests.ConfigTests import ConfigurationTest


class TestAccountService(ConfigurationTest):
    def test_get_account_money(self):
        """
        This module tests get_account_money(UUID:str) function
        """
        ...

    def test_insert_account(self):
        """
        This module tests insert_account() function
        """
        ...

    def test_delete_data(self):
        """
        This module tests delete_data() function
        """
        ...

    def test_get_name_account(self):
        """
        This module tests get_name_account() function
        """
        ...

    def test_get_name_account_checker(self):
        """
        This module tests get_name_account_checker() function
        """
        ...

    def test_merge_dict(self):
        """
        This module tests merge_dict(dct_list: list[dict]) -> list[dict] function
        """
        ...

    def test_restrict_dict(self):
        """
        This function tests restrict_dict(dct: list[dict]) function
        """
        ...

    def test_check_keys(self):
        """
        This function tests check_keys(dct: list[dict]) -> None: function
        """
        ...

    def test_insert_pay_account(self):
        """
        this module tests insert_pay_account() function
        """
        ...

    def test_get_account_status_by_identifier(self):
        """
        this module tests get_account_status_by_identifier(identifier:int) function
        """
        ...

    def test_delete_accountstatus(self):
        """
        This module tests delete_accountstatus(identifier: int) function
        """
        ...

    def test_get_by_account_status(self):
        """
        This module tests get_by_account_status(identifier:str) function
        """
        ...

    def test_get_pair(self):
        """
        This module tests get_pair(identifier:str) function
        """
        ...

    def test_get_by_pair(self):
        """
        This module tests get_by_pair(pairid: str) function
        """
        ...
