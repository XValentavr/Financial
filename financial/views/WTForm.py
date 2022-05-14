"""
This module creates WTForm to provide security of authentication

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from financial.service.currency import get_currency
from financial.service.accounts import get_name_account


class LoginForm(FlaskForm):
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
    sum = StringField("Сумма: ", validators=[DataRequired()])
    currency = SelectField("Валюта", choices=get_currency())
    wallet = SelectField("Выберите кошелек", choices=get_name_account())
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateField("Выберите дату", validators=[DataRequired()])


class Outcome(FlaskForm):
    sum = StringField("Сумма: ", validators=[DataRequired()])
    currency = SelectField("Валюта", choices=get_currency())
    wallet = SelectField("Выберите кошелек", choices=get_name_account())
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateField("Выберите дату", validators=[DataRequired()])


class Move(FlaskForm):
    sum_ = StringField("Сумма: ", validators=[DataRequired()])
    from_ = SelectField("Выберите кошелек", choices=get_name_account())
    currency_from = SelectField("Валюта", choices=get_currency())
    to_ = SelectField("Выберите кошелек", choices=get_name_account())
    currency_to = SelectField("Валюта", choices=get_currency())
    info = StringField("Введите комментарий: ", validators=[DataRequired()])
    date = DateField("Выберите дату", validators=[DataRequired()])
