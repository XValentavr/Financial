from financial import database


class Currency(database.Model):
    #: Name of the database currency
    __tablename__ = 'currency'

    #: admin's database id
    id = database.Column(database.Integer(),  database.ForeignKey('money_sum.currency'),primary_key=True)

    #: admin's name
    name = database.Column(database.String(length=255), nullable=False, unique=True)

    def __init__(self, name):
        #: admin's name
        self.name = name

    def __repr__(self):
        """
        The representation of the department
        :return: the string, representing the department of hospital by its name
        """
        return '<Currency: {}>'.format(self.name)