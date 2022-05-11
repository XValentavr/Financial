"""
This is the __init__.py file for financial module.
Imports all the necessary modules and submodules.
Defines all the needed variables for proper app functioning
"""
# standard library imports
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuration import Config
from flask_login import LoginManager
from flask_migrate import Migrate

database = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # create app
    app = Flask(__name__)
    app.config.from_object(Config)
    # to create an api and register the routes

    database.init_app(app)
    login_manager.init_app(app)
    # migrate database
    Migrate(app, database, directory=os.path.join('financial', 'migrations'))
    from .views import financial as financial_blueprint
    login_manager.init_app(app)
    from .models.users import Users

    app.register_blueprint(financial_blueprint)
    return app
