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

    __tablename__ = "user"

    id = database.Column(
        database.Integer(),
        database.ForeignKey("money_sum.user"),
        primary_key=True,
        autoincrement=True,
    )

    name = database.Column(database.String(length=255), nullable=False, unique=True)

    password = database.Column(database.String(length=255), nullable=False)

    UUID = database.Column(database.String(length=255), nullable=False)


    def __init__(self, name, password, UUID):
        self.name = name
        self.password = password
        self.UUID = UUID

    def __repr__(self):
        """
        The representation of the department
        :return: the string, representing the department of hospital by its name
        """
        return "<Users: {}>".format(self.name)

    def json(self):
        """
        This method is used to return the department in json format
        :return: the department in json format
        """
        return {
            "id": self.id,
            "UUID": self.UUID,
            "user": self.name,
            "password": self.password,
        }


class SuperUser(UserMixin, database.Model):
    """
    Model representing admins
    :param str username: admin's name
    :param date password: admin's hash password

    """

    #: Name of the database table storing admin
    __tablename__ = "superuser"

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    #: admin's name
    name = database.Column(database.String(length=255), nullable=False, unique=True)

    #: admin's full name
    password = database.Column(database.String(length=255), nullable=False)

    #: admin's avatar
    UUID = database.Column(database.String(length=255), nullable=False)

    user = database.Column(database.Integer, database.ForeignKey("user.id"))

    def __init__(self, name, password, UUID):
        #: admin's name
        self.name = name
        #: admin's date of birth
        self.password = password
        #: admin's uuid
        self.UUID = UUID


class OwnUser(UserMixin, database.Model):
    """
    Model representing admins
    :param str username: admin's name
    :param date password: admin's hash password

    """

    #: Name of the database table storing admin
    __tablename__ = "ownuser"

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    #: admin's name
    name = database.Column(database.String(length=255), nullable=False, unique=True)

    #: admin's full name
    password = database.Column(database.String(length=255), nullable=False)

    #: admin's avatar
    UUID = database.Column(database.String(length=255), nullable=False)

    user = database.Column(database.Integer, database.ForeignKey("user.id"))

    def __init__(self, name, password, UUID):
        #: admin's name
        self.name = name
        #: admin's date of birth
        self.password = password
        #: admin's uuid
        self.UUID = UUID
