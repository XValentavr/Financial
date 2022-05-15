"""
This module defines a rest interface to work with departments of hospital
"""
from flask import jsonify
from flask_restful import reqparse, Resource

# local imports
from ..service.wallet import get_wallets, get_current_wallet, delete_wallet

# get the request parser
parser = reqparse.RequestParser()

# define the arguments which will be in a request query
parser.add_argument("name")
parser.add_argument("users")


class AllWallets(Resource):
    """
    This is the class for AllDepartments Resource available at /hospital url
    """

    @staticmethod
    def get():
        jsonify(get_wallets())
        return jsonify(get_wallets())


class SingleWallet(Resource):
    """
    This is the class for Department Resource available at /hospital/<id> url
    """

    @staticmethod
    def get(identifier):
        """
        This method is called when GET request is sent
        :return: the specific department in json format
        """
        return jsonify(get_current_wallet(identifier))

    @staticmethod
    def delete(identifier):
        """
        This method is called when DELETE request is sent
        :return: the empty response with status code 204
        """
        delete_wallet(identifier)
        return "User deleted", 200
