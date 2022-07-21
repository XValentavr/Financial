"""
__init__.py file of views module with
imported info, employee_view and department_view submodules
Register the user blueprint and specify the logic on '/' and '/home' addresses
Also handle an error status
"""
# pylint: disable=cyclic-import
from flask import Blueprint, render_template

financial = Blueprint('financial', __name__)
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


@financial.errorhandler(404)
def handle_404(e):
    """
    Handel 404 error and redirect to 404.html page
    """
    return render_template("404.html"), 404


@financial.errorhandler(401)
def handle_401(err):
    """
    Handel 401 error and redirect to 401.html page
    """
    return render_template("401.html"), 401


@financial.errorhandler(500)
def handle_500(e):
    # note that we set the 500 status explicitly
    return render_template('404.html'), 500
