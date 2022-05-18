"""
This module defines a rest interface to work with departments of hospital
"""
from flask import jsonify
from flask_restful import reqparse, Resource

# get the request parser
from financial.service.comments import get_all_comments, reset_summa

parser = reqparse.RequestParser()

# define the arguments which will be in a request query
parser.add_argument("date")
parser.add_argument("comments")
parser.add_argument("addedsumma")
parser.add_argument("deletedsumma")
parser.add_argument("money")


class AllComments(Resource):
    """
    This is the class for AllDepartments Resource available at /hospital url
    """

    @staticmethod
    def get():
        return jsonify(get_all_comments())


class SingleComment(Resource):
    """
    This is the class for Department Resource available at /hospital/<id> url
    """

    @staticmethod
    def get(id):
        """
        This method is called when GET request is sent
        :return: the specific department in json format
        """
        ...

    @staticmethod
    def delete(identifier):
        """
        This method is called when DELETE request is sent
        :return: the empty response with status code 204
        """
        reset_summa(identifier)
        return "Summa reseted", 200
