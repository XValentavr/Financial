"""This is the __init__.py file of rest module.
Imports the department_of_hospital_api and employee_api submodules and registers the api links
"""
# standard library imports
from flask_restful import Api

# local imports
from . import purse, users, wallets, comments


def create_api(application):
    api = Api(application)

    api.add_resource(purse.Purse, "/api/purse/<identifier>")

    # for users
    api.add_resource(users.AllUsers, "/api/users")
    api.add_resource(users.SingleUser, "/api/users/<identifier>")

    # for wallets
    api.add_resource(wallets.AllWallets, "/api/wallets")
    api.add_resource(wallets.SingleWallet, "/api/wallet/<identifier>")

    # for comments
    api.add_resource(comments.AllComments, "/api/comments")
    api.add_resource(comments.SingleComment, "/api/reset/<identifier>")
    api.add_resource(comments.SingleCommentDate, "/api/comments/<identifier>")
    return api
