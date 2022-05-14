"""
This module defines a rest interface to work with departments of hospital
"""
from flask import abort, jsonify, Response
from flask_restful import reqparse, Resource

# local imports
from ..service.users import get_all_users, get_user_by_id, delete_user

# get the request parser
parser = reqparse.RequestParser()

# define the arguments which will be in a request query
parser.add_argument("name")
parser.add_argument("password")


def abort_if_department_doesnt_exist(identifier):
    """
    This function is used to prevent the access of a resource that doesn't exist
    :param identifier: the id of the resource
    """
    if get_user_by_id(identifier) is None:
        abort(Response("No users", 404))


class AllUsers(Resource):
    """
    This is the class for AllDepartments Resource available at /hospital url
    """

    @staticmethod
    def get():
        return jsonify(get_all_users())


class SingleUser(Resource):
    """
    This is the class for Department Resource available at /hospital/<id> url
    """

    @staticmethod
    def get(UUID):
        """
        This method is called when GET request is sent
        :return: the specific department in json format
        """
        abort_if_department_doesnt_exist(UUID)
        return jsonify(get_user_by_id(UUID))

    @staticmethod
    def delete(identifier):
        """
        This method is called when DELETE request is sent
        :return: the empty response with status code 204
        """
        abort_if_department_doesnt_exist(identifier)
        delete_user(identifier)
        return "User deleted", 200
