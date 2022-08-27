"""
__init__.py file of views module with
imported info, employee_view and department_view submodules
Register the user blueprint and specify the logic on '/' and '/home' addresses
Also handle an error status
"""
# pylint: disable=cyclic-import

from flask import Blueprint

financial = Blueprint("financial", __name__)

from flask import render_template
from .WTForm import LoginForm
from . import income
from . import outcome
from . import moving
from . import exchange
from . import adduser
from . import changeuser
from . import resetcomments
from . import moving
from . import createwallet
from . import pay
from . import wallets
from . import auth
from . import currency


@financial.app_errorhandler(404)
def handle_404(err):
    """
    Handel 404 error and redirect to 404.html page
    """
    return render_template("404.html"), 404


@financial.app_errorhandler(401)
def handle_401(err):
    """
    Handel 401 error and redirect to 401.html page
    """
    return render_template("401.html"), 401
