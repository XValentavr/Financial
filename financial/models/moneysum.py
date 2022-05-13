from financial import database


class Moneysum(database.Model):
    #: Name of the database currency
    __tablename__ = 'money_sum'

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    #: admin's name
    moneysum = database.Column(database.FLOAT(), nullable=False)
    user = database.Column(database.Integer(), nullable=False)
    currency = database.Column(database.Integer(), nullable=False)
    wallet = database.Column(database.Integer(), nullable=False)

    userid = database.relationship('Users', backref='money_sum',
                                   lazy='dynamic')
    currencyid = database.relationship('Currency', backref='money_sum',
                                       lazy='dynamic')
    accountid = database.relationship('Accounts', backref='money_sum',
                                    lazy='dynamic')

    def __repr__(self):
        """
        The representation of the department
        :return: the string, representing the department of hospital by its name
        """
        return '<Currency: {}>'.format(self.name)
