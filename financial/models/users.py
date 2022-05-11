"""
Employee model used to represent admin user, this module defines the
following classes:
- `Admin`, admin user  model
"""
from flask_login import UserMixin

from financial import database


class Users(UserMixin, database.Model):
    """
        Model representing admins
    :param str username: admin's name
    :param date password: admin's hash password

    """

    #: Name of the database table storing admin
    __tablename__ = 'user'

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    #: admin's name
    name = database.Column(database.String(length=255), nullable=False, unique=True)

    #: admin's full name
    password = database.Column(database.String(length=255), nullable=False)

    #: admin's avatar
    UUID = database.Column(database.String(length=255), nullable=False)

    def __init__(self, name, password, UUID):
        #: admin's name
        self.name = name
        #: admin's date of birth
        self.password = password
        #: admin's uuid
        self.UUID = UUID
