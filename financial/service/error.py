import datetime
from financial import database
from financial.models.error import Error


def add_error(message):
    """
    this module add error from popup form
    :param form:from to get info from
    :return: None
    """
    date = datetime.datetime.today().replace(microsecond=0)

    error = Error(message, date)
    database.session.add(error)
    database.session.commit()
