"""
This module defines a rest interface to work with departments of hospital
"""
import re
import time
from urllib.parse import unquote

from flask import jsonify, request, Response
from flask_restful import reqparse, Resource, abort

# get the request parser
from financial.service.comments import (
    get_all_comments,
    reset_summa,
    get_comment_by_wallet_name_and_dates,
    get_comment_by_wallet_name,
)

parser = reqparse.RequestParser()

# define the arguments which will be in a request query
parser.add_argument("date")
parser.add_argument("comments")
parser.add_argument("addedsumma")
parser.add_argument("deletedsumma")
parser.add_argument("money")
parser.add_argument("identifier")


def validate_date(date):
    """
    This function checks whether th date matches the mm/dd/yyyy pattern
    :param date: date to check
    :return: true, if date matches the pattern, false if not
    """

    if re.search("[a-zA-Zа-яА-ЯҐґ]", date):
        return False
    try:
        return bool(time.strptime(date, "%Y/%m/%d"))
    except ValueError:
        return False


class AllComments(Resource):
    """
    This is the class for AllDepartments Resource available at /hospital url
    """

    @staticmethod
    def get():
        return jsonify(get_all_comments())


class SingleCommentDate(Resource):
    """
    This is the class for Department Resource available at /hospital/<id> url
    """

    @staticmethod
    def get(identifier):
        args = request.args
        if (
            len(args) == 2
            and validate_date(args["start_date"].replace("-", "/"))
            and validate_date(args["end_date"].replace("-", "/"))
        ):
            return jsonify(
                get_comment_by_wallet_name_and_dates(
                    unquote(identifier),
                    start=args["start_date"].replace("-", "/"),
                    end=args["end_date"].replace("-", "/"),
                )
            )
        if (
            len(args) == 2
            and validate_date(args["start_date"].replace("-", "/"))
            and not validate_date(args["end_date"].replace("-", "/"))
        ):
            return jsonify(
                get_comment_by_wallet_name_and_dates(
                    unquote(identifier), start=args["start_date"].replace("-", "/")
                )
            )
        if (
            len(args) == 2
            and not validate_date(args["start_date"].replace("-", "/"))
            and not validate_date(args["end_date"].replace("-", "/"))
        ):
            return jsonify(get_comment_by_wallet_name(unquote(identifier)))
        if len(args) == 0:
            return jsonify(get_comment_by_wallet_name(unquote(identifier)))
        return abort(Response("Couldn't perform search. Invalid data", 400))


class SingleComment(Resource):
    """
    This is the class for Department Resource available at /hospital/<id> url
    """

    @staticmethod
    def delete(identifier):
        """
        This method is called when DELETE request is sent
        :return: the empty response with status code 204
        """
        reset_summa(identifier)
        return "Summa reseted", 200
