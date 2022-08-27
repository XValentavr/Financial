from financial import database
from financial.models.accountstatus import Accountstatus


def get_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency

    currency = Currency.query.all()
    return [(currency.id, currency.name) for currency in currency]


def get_current_currency(identifier: int):
    from financial.models.currency import Currency

    currency = Currency.query.filter_by(id=identifier).first()
    return currency


def get_current_currency_by_name(name: str):
    from financial.models.currency import Currency

    currency = Currency.query.filter_by(name=name).first()
    return currency


def get_list_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency

    currency = Currency.query.all()
    return [currency for currency in currency]


def get_api_currency():
    """
    This module gets currency from database
    :return: list of curencies
    """
    from financial.models.currency import Currency

    currency = Currency.query.all()
    return [currency.json() for currency in currency]


def insert_new_currency(name: str):
    """
    This module creates new currency
    :param name:name of currency
    :return: None
    """
    from financial.models.currency import Currency

    cur = Currency(name=name)
    database.session.add(cur)
    database.session.commit()


def change_currency(old_name: str, new_name: str):
    """
    This module creates new currency
    :param old_name:old_name of currency
    :param new_name: new name of currency
    :return: None
    """
    from financial.models.currency import Currency

    old_name = get_current_currency(identifier=int(old_name)).name

    change_comment(old_name, new_name)
    cur = Currency.query.filter_by(name=old_name).first()
    cur.name = new_name
    database.session.add(cur)
    database.session.commit()


def change_comment(currency, old):
    """
    This module changes currency in comment
    :param currency: current currency
    :return: None
    """
    added_comment = Accountstatus.query.filter(Accountstatus.addedsumma.like(f'%{currency}%')).all()
    deleted_comment = Accountstatus.query.filter(Accountstatus.deletedsumma.like(f'%{currency}%')).all()
    if added_comment is not None:
        for a_c in added_comment:
            to_change = a_c.addedsumma.split(' ')
            to_change[1] = old
            to_change = ' '.join(map(str, to_change))
            a_c.addedsumma = to_change
            database.session.add(a_c)
            database.session.commit()
    elif deleted_comment is not None:
        for a_c in added_comment:
            to_change = a_c.deleted_comment.split(' ')
            to_change[1] = old
            to_change = ' '.join(map(str, to_change))
            a_c.deletedsumma = to_change
            database.session.add(a_c)
            database.session.commit()


def delete_currency(name: str):
    """
    This module deletes currency
    :param name: name of currency
    :return: None
    """
    from financial.models.currency import Currency
    Currency.query.filter_by(name=name).delete()
    cur = Currency.query.get_or_404(name)
    database.session.delete(cur)
    database.session.commit()
