"""
This module defines crud operations to work with user table
"""
from financial.models.users import Users


def get_user_by_name(username: str):
    """
    This function is used to get the single user by id
    :param username: the username of the user to get
    :return: the user  with the specified username
    """
    user = Users.query.filter_by(name=username).first()
    return user if user is not None else None


def get_all_user() -> str:
    """
    This function is used to get the single user by id
    :return: the user  with the specified username
    """
    user = Users.query.all()
    return user if user is not None else None
