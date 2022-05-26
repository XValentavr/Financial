from financial import database


class Moneysum(database.Model):
    #: Name of the database currency
    __tablename__ = "money_sum"

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    #: admin's name
    moneysum = database.Column(database.FLOAT(), nullable=False)
    user = database.Column(database.Integer(), nullable=False)
    currency = database.Column(database.Integer(), nullable=False)
    wallet = database.Column(database.Integer(), nullable=False)
    isgeneral = database.Column(database.Integer(), nullable=False)

    userid = database.relationship(
        "Users", backref="money_sum", lazy="dynamic", cascade="all,delete"
    )
    currencyid = database.relationship(
        "Currency", backref="money_sum", lazy="dynamic", cascade="all,delete"
    )
    accountid = database.relationship(
        "Accounts", backref="money_sum", lazy="dynamic", cascade="all,delete"
    )
    accountinfo = database.relationship(
        "Accountstatus", backref="money_sum", lazy="dynamic", cascade="all,delete"
    )
    roots = database.relationship(
        "Userroot", backref="money_sum"
    )
