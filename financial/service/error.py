import datetime

from flask import redirect, request

from financial import database
from financial.models.error import Error


def add_error(form):
    """
    this module add error from popup form
    :param form:from to get info from
    :return: None
    """
    message = form.get("errormessage")
    date = datetime.datetime.today().replace(microsecond=0)

    error = Error(message, date)
    database.session.add(error)
    database.session.commit()
