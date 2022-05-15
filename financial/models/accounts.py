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

    def __init__(self, identifier, name):
        #: admin's name
        #: admin's name
        self.id = identifier
        self.name = name

    def json(self):
        """
        This method is used to return the department in json format
        :return: the department in json format
        """
        from financial.service.moneysum import get_count_users
        wallet = get_count_users(self.id)
        if wallet:
            users = wallet[0][1] if wallet[0][0] == self.id else 0
            print(users)
        else:
            users = 0
        return {
            "id": self.id,
            'users': users,
            "name": self.name
        }
