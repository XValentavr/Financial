"""
This mpdule representate base configuration class of test
"""
# standard library imports
import unittest

# local imports
from financial import create_app, database

from configuration import TestingConfig


class ConfigurationTest(unittest.TestCase):
    """
    Create a configuration test case
    """

    def setUp(self):
        # create the app with the specified config
        app = create_app()
        app.config.from_object(TestingConfig)
        # specify the database connection string
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "mysql+pymysql://DjksycrbqDfktynby19991:admin@database-2-instance-1.cakkxt7tkzma.us-east-1.rds.amazonaws.com:3306/financialapp"

        database.init_app(app)
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self):
        """
        This method is executed after every test case
        :return:
        """
        # close all the session and drop the tables
        database.session.close_all()
