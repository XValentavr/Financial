from financial import database


class Error(database.Model):
    #: Name of the database table storing admin
    __tablename__ = "error"

    #: admin's database id
    id = database.Column(
        database.Integer(),
        database.ForeignKey("money_sum.wallet"),
        primary_key=True,
        autoincrement=True,
    )

    #: admin's name
    text = database.Column(database.String(), nullable=False, unique=True)

    date = database.Column(database.DateTime())

    def __init__(self, text, date):
        self.text = text
        self.date = date
