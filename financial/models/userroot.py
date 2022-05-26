"""
Employee model used to represent admin user, this module defines the
following classes:
- `Admin`, admin user  model
"""
from flask_login import UserMixin

from financial import database


class Userroot(UserMixin, database.Model):
    #: Name of the database table storing admin
    __tablename__ = "user_root"

    #: admin's database id
    id = database.Column(database.Integer(), database.ForeignKey("money_sum.isgeneral"), primary_key=True)

    #: admin's name
    username = database.Column(database.Integer(), database.ForeignKey("user.id"), nullable=False,
                               unique=True, )

    #: admin's full name
    walletname = database.Column(database.Integer(), database.ForeignKey("accounts.id"), nullable=False)

    #: admin's avatar
    isgeneral = database.Column(database.BOOLEAN, nullable=False)

    userid = database.relationship(
        "Users", foreign_keys=[username], backref="user_root"
    )
    walletid = database.relationship(
        "Accounts", foreign_keys=[walletname], backref="user_root"
    )

    def __init__(self, username, walletname, isgeneral):
        self.username = username
        self.walletname = walletname
        self.isgeneral = isgeneral
