"""
This module defines crud operations to work with user table
"""
import uuid

from flask import session

from financial import database

from werkzeug.security import check_password_hash, generate_password_hash

from financial.models.users import Users, SuperUser, OwnUser


def get_user_by_enter_name(username: str):
    """
    This function is used to get the single user by id
    :param username: the username of the user to get
    :return: the user  with the specified username
    """
    user = Users.query.filter_by(name=username).all()
    users = [user for user in user]
    print(users)
    for usr in users:
        return usr


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


def get_user_by_UUID(UUID: str):
    """
    This module gets user by UUID
    :param UUID: string of uuid code
    :return: current user
    """
    user = Users.query.filter_by(UUID=UUID).first()
    return user.json() if user is not None else None


def get_user_by_id(identifier: str):
    """
    This module gets user by UUID
    :param identifier string of uuid code
    :return: current user
    """
    user = Users.query.filter_by(id=identifier).first()
    return user.json() if user is not None else None


def add_user(username: str, password: str):
    """
    This module helps to register new user
    :param username: username
    :param password: password of user
    :return: None
    """
    user = Users(
        name=username, password=generate_password_hash(password), UUID=uuid.uuid4()
    )
    database.session.add(user)
    database.session.commit()


def get_all_users():
    """
    This module gets user by UUID
    :param UUID: string of uuid code
    :return: current user
    """

    users = Users.query.all()
    return [user.json() for user in users if user.UUID != str(session["UUID"]).strip()]


def delete_user(identifier: int) -> None:
    """
    This function is used to delete an existing department
    :param identifier: the id of the department of hospital to delete
    """
    user = Users.query.get_or_404(identifier)
    database.session.delete(user)
    database.session.commit()


def update_user(UUID: int, name: str, password: str) -> None:
    """
    This function is used to update an existing department
    :param identifier: the id of the department of hospital to update
    :param name: the name of the department of hospital to update
    :param to_do: the description of the department of hospital to update
    """
    user = Users.query.filter_by(UUID=UUID).first()
    user.name = name
    user.password = password
    user.UUID = UUID
    database.session.add(user)
    database.session.commit()
