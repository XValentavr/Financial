from flask import jsonify
from flask_restful import Resource

from financial.service.currency import get_api_currency, get_current_currency_by_name, delete_currency


class AllCurrencies(Resource):
    @staticmethod
    def get():
        return jsonify(get_api_currency())


class SingleCurrency(Resource):

    @staticmethod
    def get(name):
        """
        This method is called when GET request is sent
        :return: the specific currency in json format
        """
        currency = get_current_currency_by_name(name)
        if currency is not None:
            return jsonify()
        return "No such currency", 404

    @staticmethod
    def delete(identifier):
        """
        This method is called when DELETE request is sent
        :return: the empty response with status code 204
        """
        delete_currency(identifier)
        return "Currency deleted", 200
