from financial import create_app


def get_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency
    with create_app().app_context():
        currency = Currency.query.all()
        return [(currency.name, currency.name) for currency in currency]
