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
