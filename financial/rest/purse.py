"""
This module defines a rest interface to work with departments of hospital
"""
from flask import abort, jsonify, Response
from flask_restful import reqparse, Resource

# local imports
from ..service import accounts

# get the request parser
parser = reqparse.RequestParser()

# define the arguments which will be in a request query
parser.add_argument('name')
parser.add_argument('money')


def abort_if_department_doesnt_exist(identifier):
    """
    This function is used to prevent the access of a resource that doesn't exist
    :param identifier: the id of the resource
    """
    if accounts.get_account_money(identifier) is None:
        abort(Response("Нет кошельков", 404))


class Purse(Resource):
    """
     This is the class for AllDepartments Resource available at /hospital url
    """

    @staticmethod
    def get(identifier):
        return jsonify(accounts.get_account_money(identifier))
