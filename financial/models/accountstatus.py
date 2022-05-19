from financial import database
from financial.models.wallet import Accounts


class Accountstatus(database.Model):
    #: Name of the database table storing admin
    __tablename__ = "accountstatus"

    #: admin's database id
    id = database.Column(database.Integer(), primary_key=True)

    money = database.Column(database.Integer(), database.ForeignKey("money_sum.id"))
    date = database.Column(database.DateTime())
    comments = database.Column(database.String())
    addedsumma = database.Column(database.String())
    deletedsumma = database.Column(database.String())
    number = database.Column(database.String())
    percent = database.Column(database.String())
    isexchanged = database.Column(database.BOOLEAN())
    ismoved = database.Column(database.BOOLEAN())
    ismodified = database.Column(database.String())
    pairidentificator = database.Column(database.String())
    useridentificator =database.Column(database.String())

    moneyid = database.relationship("Moneysum", backref="accountstatus")

    def json(self):
        """
        This method is used to return the department in json format
        :return: the department in json format
        """
        return {
            "account": Accounts.query.get_or_404(self.account).name
            if self.account is not None
            else None,
            "money": self.money,
        }

    def __repr__(self):
        """
        The representation of the department
        :return: the string, representing the department of hospital by its name
        """
        return "<Accountstatus: {}>".format(self.id)
