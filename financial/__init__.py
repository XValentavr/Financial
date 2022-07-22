"""
This is the __init__.py file for financial module.
Imports all the necessary modules and submodules.
Defines all the needed variables for proper app functioning
"""
# standard library imports
import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from configuration import Config

database = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # create app
<<<<<<< HEAD

    application = Flask(__name__)
    application.config.from_object(Config)
=======
    app = Flask(__name__)
    app.config.from_object(Config)
>>>>>>> debugger
    # to create an api and register the routes
    from .rest import create_api
    create_api(application)

    database.init_app(application)
    login_manager.init_app(application)
    # migrate database
<<<<<<< HEAD
    Migrate(application, database, directory=os.path.join("financial", "migrations"))
    from .views import financial as financial_blueprint

    login_manager.init_app(application)
    from .models.users import Users

    application.register_blueprint(financial_blueprint)
    return application
=======
    Migrate(app, database, directory=os.path.join("financial", "migrations"))

    login_manager.init_app(app)
    from financial.views import financial
    from .models.users import Users

    app.register_blueprint(financial)
    return app
>>>>>>> debugger
