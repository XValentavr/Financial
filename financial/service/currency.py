def get_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency
    from financial import create_app

    with create_app().app_context():
        currency = Currency.query.all()
        return [(currency.id, currency.name) for currency in currency]


def get_current_currency(identifier: int):
    from financial.models.currency import Currency

    currency = Currency.query.filter_by(id=identifier).first()
    return currency


def get_list_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency

    currency = Currency.query.all()
    return [currency for currency in currency]
