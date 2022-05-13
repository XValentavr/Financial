from financial import database


class Accounts(database.Model):
    #: Name of the database table storing admin
    __tablename__ = "accounts"

    #: admin's database id
    id = database.Column(
        database.Integer(), database.ForeignKey("money_sum.wallet"), primary_key=True
    )

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
        return "<Account: {}>".format(self.name)
