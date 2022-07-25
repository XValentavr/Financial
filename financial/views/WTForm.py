"""
This module creates WTForm to provide security of authentication

"""
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    DateTimeLocalField,
    IntegerField,
)
from wtforms.validators import DataRequired, Length

from financial.service.accounts import get_name_account
from financial.service.currency import get_currency


class LoginForm(FlaskForm):
    """
    This class create WTForm to login admin user. There are four fields to enter data

    """

    username = StringField(
        "Логин: ",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=25,
                message="Field must be between 4 and 100 characters long.",
            ),
        ],
    )
    password = PasswordField(
        "Пароль: ", validators=[DataRequired(), Length(min=4, max=100)]
    )


class Register(FlaskForm):
    """
    This class create WTForm to login admin user. There are four fields to enter data

    """

    username = StringField(
        "Username: ",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=25,
                message="Field must be between 4 and 100 characters long.",
            ),
        ],
    )
    password = PasswordField(
        "Password: ", validators=[DataRequired(), Length(min=4, max=100)]
    )


class Income(FlaskForm):
    sum = IntegerField("Сумма: ", validators=[DataRequired()])
    currency = SelectField("Валюта", choices=[])
    wallet = SelectField("Выберите кошелек", choices=[])
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateTimeLocalField("Выберите дату", validators=[DataRequired()], default=datetime.today)

    def set_choices(self):
        self.currency.choices = get_currency()
        self.wallet.choices = get_name_account()


class Outcome(FlaskForm):
    sum = IntegerField("Сумма: ", validators=[DataRequired()])
    currency = SelectField("Валюта", choices=[])
    wallet = SelectField("Выберите кошелек", choices=[])
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateTimeLocalField("Выберите дату", validators=[DataRequired()], )

    def set_choices(self):
        self.currency.choices = get_currency()
        self.wallet.choices = get_name_account()


class Move(FlaskForm):
    sum_ = IntegerField("Сумма: ", validators=[DataRequired()])
    from_ = SelectField("Кошелек откуда", choices=[])
    currency_from = SelectField("Валюта", choices=[])
    to_ = SelectField("Кошелек куда", choices=[])
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateTimeLocalField("Выберите дату", validators=[DataRequired()], )

    def set_choices(self):
        self.currency_from.choices = get_currency()
        self.from_.choices = get_name_account()
        self.to_.choices = get_name_account()


class Wallet(FlaskForm):
    wallet = StringField("Введите название кошелька", validators=[DataRequired()])
    visibility = SelectField("Сделать видимым?", choices=["Да", "Нет"])
