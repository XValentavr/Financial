"""Specify configurations"""
import os
from datetime import timedelta
from financial import osenvironment


class Config(object):
    """
    Base configuration
    """

    PERMANENT_SESSION_LIFETIME = timedelta(days=24)
    MAX_CONTENT_LENGTH = 1024 * 1024
    SECRET_KEY = "7b0342f12ee64296aaaa9738c72ca2c4"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False


class TestingConfig(object):
    """
    Testing configurations
    """

    # Activates the testing mode of Flask extensions. This allows us to use testing properties
    # that could for instance have an increased runtime cost, such as unittest helpers.
    SQLALCHEMY_ECHO = False
