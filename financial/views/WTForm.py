"""
This module creates WTForm to provide security of authentication

"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    DateField,
    IntegerField,
    FloatField,
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
    date = DateField("Выберите дату", validators=[DataRequired()])

    def set_choices(self, where, ch=None):
        if where == "edit":
            self.currency.choices = ch[0]
            self.wallet.choices = ch[1]
        else:
            self.currency.choices = get_currency()
            self.wallet.choices = get_name_account()


class Outcome(FlaskForm):
    sum = IntegerField("Сумма: ", validators=[DataRequired()])
    currency = SelectField("Валюта", choices=[])
    wallet = SelectField("Выберите кошелек", choices=[])
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateField("Выберите дату", validators=[DataRequired()])

    def set_choices(self, where, ch=None):
        if where == "edit":
            self.currency.choices = ch[0]
            self.wallet.choices = ch[1]
        else:
            self.currency.choices = get_currency()
            self.wallet.choices = get_name_account()


class Move(FlaskForm):
    sum_ = IntegerField("Сумма: ", validators=[DataRequired()])
    from_ = SelectField("Выберите кошелек", choices=[])
    currency_from = SelectField("Валюта", choices=[])
    to_ = SelectField("Выберите кошелек", choices=[])
    currency_to = SelectField("Валюта", choices=[])
    rate = FloatField("Введите курс", validators=[DataRequired()])
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateField("Выберите дату", validators=[DataRequired()])

    def set_choices(self, where, ch=None):
        if where == "move":
            self.currency_from.choices = ch[0]
            self.currency_to.choices = ch[1]
            self.from_.choices = ch[2]
            self.to_.choices = ch[3]
        else:
            self.currency_from.choices = get_currency()
            self.currency_to.choices = get_currency()
            self.from_.choices = get_name_account()
            self.to_.choices = get_name_account()


class Wallet(FlaskForm):
    wallet = StringField("Введите название кошелька", validators=[DataRequired()])
    visibility = SelectField("Сделать видимым для всех?", choices=["Да", "Нет"])
