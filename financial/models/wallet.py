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

    visibility = database.Column(database.String(length=50), nullable=False)

    def __init__(self, identifier, name, visibility):
        self.id = identifier
        self.name = name
        self.visibility = visibility

    def json(self):
        """
        This method is used to return the department in json format
        :return: the department in json format
        """
        from financial.service.moneysum import get_count_users
        wallet = get_count_users(self.id)
        if wallet:
            users = wallet[0][1] if wallet[0][0] == self.id else 0
        else:
            users = 0
        if self.visibility.strip() == 'No':
            self.visibility = 'Приватный'
        elif self.visibility.strip() == 'Yes':
            self.visibility = 'Общий'
        return {
            "id": self.id,
            'users': users,
            "name": self.name,
            'visibility': self.visibility
        }
