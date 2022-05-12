"""
This module defines crud operations to work with user table
"""
from werkzeug.security import check_password_hash

from financial.models.users import Users, SuperUser, OwnUser


def get_user_by_name(username: str, password: str):
    """
    This function is used to get the single user by id
    :param username: the username of the user to get
    :return: the user  with the specified username
    """
    user = Users.query.filter_by(name=username).all()
    users = [user for user in user]
    for usr in users:
        if usr.name == username and check_password_hash(usr.password, password):
            return usr


def get_all_user() -> str:
    """
    This function is used to get the single user by id
    :return: the user  with the specified username
    """
    user = Users.query.all()
    return user if user is not None else None


def get_super_user_by_name(username: str, password: str):
    """
    This function is used to get the single user by id
    :param username: the username of the user to get
    :return: the user  with the specified username
    """
    suser = SuperUser.query.filter_by(name=username).all()
    suser = [suser for suser in suser]
    for usr in suser:
        if usr.name == username and check_password_hash(usr.password, password):
            return usr


def get_own_user_by_name(username: str):
    """
    This function is used to get the single user by id
    :param username: the username of the user to get
    :return: the user  with the specified username
    """
    ownuser = OwnUser.query.filter_by(name=username).first()
    return ownuser if ownuser is not None else None
