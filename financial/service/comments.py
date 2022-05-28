import datetime
import os

import sqlalchemy
from flask import session as s
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from financial import database
from financial.models.accountstatus import Accountstatus
from financial.models.moneysum import Moneysum
from financial.models.userroot import Userroot
from financial.models.users import Users
from financial.models.wallet import Accounts
from financial.service.accounts import get_account_status_by_identifier
from financial.service.accounts import get_by_pair, get_pair, get_to_sum
from financial.service.currency import (
    get_current_currency,
    get_current_currency_by_name,
)
from financial.service.moneysum import reset_moneysum
from financial.service.userroot import get_user_root
from financial.service.users import get_user_by_UUID
from financial.service.wallet import get_current_wallet_by_name


def get_comment_by_wallet_name_and_dates(name, start, end=None):
    """
    This module gets comments by wallet and date
    :param name: name of wallet
    :param start: start date
    :param end: finish date
    :return: result of searching
    """
    if end is None:
        now = datetime.datetime.today().replace(microsecond=0)
        end = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        end = str(end) + " " + str(datetime.datetime.now().time().isoformat("seconds"))
        end = datetime.datetime.strptime(end.strip(), "%Y/%m/%d %H:%M:%S")

    start = str(start) + " " + str(datetime.datetime.now().time().isoformat("seconds"))
    start = datetime.datetime.strptime(start.strip(), "%Y/%m/%d %H:%M:%S")
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    comments = []
    result = (
        session.query(
            Accountstatus.date,
            Accountstatus.comments,
            Accountstatus.addedsumma,
            Accountstatus.deletedsumma,
            Users.name,
            Accounts.name,
            Users.UUID,
            Accounts.visibility,
            Accountstatus.id,
            Accountstatus.number,
            Accountstatus.isexchanged,
            Accountstatus.ismoved,
            Accountstatus.pairidentificator,
            Accountstatus.ismodified,
            Accountstatus.isdeleted,
            Userroot.isgeneral,
        )
            .join(Moneysum.userid)
            .join(Moneysum.accountinfo)
            .join(Moneysum.accountid)
            .join(Moneysum.roots)
            .filter(Accounts.name == name, Accountstatus.date.between(start, end))
            .order_by(desc(Accountstatus.id))
            .all()
    )
    return create_result_comments(result, comments)


def get_comment_by_wallet_name(name) -> list[dict]:
    """
    This module gets comment by wallet name
    :return:
    """
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    comments = []
    result = (
        session.query(
            Accountstatus.date,
            Accountstatus.comments,
            Accountstatus.addedsumma,
            Accountstatus.deletedsumma,
            Users.name,
            Accounts.name,
            Users.UUID,
            Accounts.visibility,
            Accountstatus.id,
            Accountstatus.number,
            Accountstatus.isexchanged,
            Accountstatus.ismoved,
            Accountstatus.pairidentificator,
            Accountstatus.ismodified,
            Accountstatus.isdeleted,
            Userroot.isgeneral,
        )
            .join(Moneysum.userid)
            .join(Moneysum.accountinfo)
            .join(Moneysum.accountid)
            .join(Moneysum.roots)
            .filter(Accounts.name == name)
            .order_by(desc(Accountstatus.id))
            .all()
    )
    return create_result_comments(result, comments)


def get_all_comments() -> list[dict]:
    """
    This module gets all comments from database to show
    :return: json of get data
    """
    engine = sqlalchemy.create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))
    session = sessionmaker(bind=engine)
    session = session()
    comments = []
    result = (
        session.query(
            Accountstatus.date,
            Accountstatus.comments,
            Accountstatus.addedsumma,
            Accountstatus.deletedsumma,
            Users.name,
            Accounts.name,
            Users.UUID,
            Accounts.visibility,
            Accountstatus.id,
            Accountstatus.number,
            Accountstatus.isexchanged,
            Accountstatus.ismoved,
            Accountstatus.pairidentificator,
            Accountstatus.ismodified,
            Accountstatus.isdeleted,
            Userroot.isgeneral,
        )
            .join(Moneysum.userid)
            .join(Moneysum.accountinfo)
            .join(Moneysum.accountid)
            .join(Moneysum.roots)
            .order_by(desc(Accountstatus.id))
            .all()
    )
    return create_result_comments(result, comments)


def reset_summa(identifier) -> None:
    """
    This module resets data when reset was pressed
    :param identifier: int of account identifier
    :return: none
    """
    status = get_account_status_by_identifier(identifier)
    pairs = get_by_pair(get_pair(identifier))
    if len(pairs) < 2:
        reseted_by_status(status)
    else:
        for prs in pairs:
            status = get_account_status_by_identifier(prs.id)
            reseted_by_status(status)


def reseted_by_status(status) -> None:
    """
    This module resets data
    :param status: status to reset
    :return:
    """
    if status.deletedsumma is None:
        reset_moneysum(status.id, status.money, 0 - float(status.addedsumma.split()[0]))
    elif status.addedsumma is None:
        reset_moneysum(status.id, status.money, float(status.deletedsumma.split()[0]))


def update_comment(form, uuid: str, from_where: str, summa_changed: float, ispay=None):
    """
    This module updates income or outcome data
    :param form: form to get info from
    :param uuid: unique identifier
    :param from_where: type of transaction
    :return: new changed data
    """
    if ispay is not None:
        number = form.get("number")
        percent = form.get("percent")
        wallet = form.get("wallet")
        summa = form.get("summa")
        if int(percent) > 0:
            summa = int(summa) - (int(summa) * (int(percent) / 100))
        else:
            summa = int(summa)
        info = form.get("comments")
        currency = form.get("valuta")
        date = str(form.get("date")) + " " + str(datetime.datetime.now().time())

    else:
        number = (None,)
        percent = (None,)
        wallet = form.wallet.data
        summa = form.sum.data
        info = form.info.data
        currency = form.currency.data
        date = str(form.date.data) + " " + str(datetime.datetime.now().time())
    user_ = get_user_by_UUID(s["UUID"].strip())
    user = user_.get("id")
    wallet = get_current_wallet_by_name(wallet)
    currency = get_current_currency_by_name(currency).id
    summa_to_update = get_to_sum(user, int(wallet), currency)
    currency_name = get_current_currency(currency).name
    user_to_reset = user_.get("UUID")
    if summa_to_update is None:
        user = Accountstatus.query.filter_by(pairidentificator=uuid).first()
        user_ = get_user_by_UUID(user.useridentificator.strip())
        summa_to_update = get_to_sum(user_.get("id"), int(wallet), currency)
        user_to_reset = user.useridentificator
    if summa_to_update:
        for summa_to_update in summa_to_update:
            status = Accountstatus.query.filter_by(pairidentificator=uuid).first()
            database.session.delete(status)
            database.session.commit()
            # if from where is income then insert income value
            if from_where == "income":
                summa_to_update.moneysum -= summa_changed
                summa_to_update.moneysum += float(summa)
                database.session.add(summa_to_update)
                database.session.commit()
                accounts = Accountstatus(
                    money=summa_to_update.id,
                    date=date,
                    comments=info,
                    addedsumma=str(summa) + " " + currency_name if summa else None,
                    deletedsumma=None,
                    number=number,
                    percent=percent,
                    isexchanged=0,
                    ismoved=0,
                    ismodified=s["UUID"],
                    isdeleted=False,
                    pairidentificator=uuid,
                    useridentificator=user_to_reset,
                )
                database.session.add(accounts)
                database.session.commit()

            else:
                # if from where is outcome then insert outcome value
                summa_to_update.moneysum += summa_changed
                summa_to_update.moneysum += 0 - float(summa)
                database.session.add(summa_to_update)
                database.session.commit()
                accounts = Accountstatus(
                    money=summa_to_update.id,
                    date=date,
                    comments=info,
                    addedsumma=None,
                    deletedsumma=str(summa) + " " + currency_name if summa else None,
                    number=number,
                    percent=percent,
                    isexchanged=0,
                    ismoved=0,
                    isdeleted=False,
                    ismodified=s["UUID"],
                    pairidentificator=uuid,
                    useridentificator=user_to_reset,
                )
                database.session.add(accounts)
                database.session.commit()


def update_moving_commands(form, summa_add, summa_delete, added):
    sum_ = form.sum_.data
    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")
    user_to_reset = ""
    info = form.info.data
    date = str(form.date.data) + " " + str(datetime.datetime.now().time())

    # gets deleted
    from_ = form.from_.data
    rate = form.rate.data
    from_ = get_current_wallet_by_name(from_)
    currency_from = form.currency_from.data
    summa_to_delete = get_to_sum(user, int(from_), currency_from)

    if summa_to_delete is None:
        currency_from = get_current_currency_by_name(currency_from).id
        user = Accountstatus.query.filter_by(pairidentificator=added).first()
        user_sum = get_user_by_UUID(user.useridentificator.strip())
        summa_to_delete = get_to_sum(user_sum.get("id"), int(from_), currency_from)
        user_to_reset = user.useridentificator.strip()
    for summa_to_delete in summa_to_delete:
        summa_to_delete.moneysum += float(summa_add)
        summa_to_delete.moneysum += 0 - float(sum_)
    status = Accountstatus.query.filter_by(pairidentificator=added).all()
    for ss in status:
        database.session.delete(ss)
        database.session.commit()

    # add new data
    database.session.add(summa_to_delete)
    database.session.commit()
    accounts = Accountstatus(
        money=summa_to_delete.id,
        date=date,
        comments=info,
        addedsumma=None,
        deletedsumma=str(sum_) + " " + form.currency_from.data if sum_ else None,
        number=None,
        percent=None,
        isexchanged=0,
        ismoved=1,
        ismodified=s["UUID"],
        isdeleted=False,
        pairidentificator=added,
        useridentificator=user_to_reset,
    )
    database.session.add(accounts)
    database.session.commit()

    # get added
    to_ = form.to_.data
    to_ = get_current_wallet_by_name(to_)
    currency_to = form.currency_to.data
    summa_to_add = get_to_sum(user.id, int(to_), currency_to)
    new_entered_summa = sum_ * rate

    # if summa is none then get user
    if summa_to_add is None:
        currency_to = get_current_currency_by_name(currency_to).id
        user = Accountstatus.query.filter_by(pairidentificator=added).first()
        user_sum = get_user_by_UUID(user.useridentificator.strip())
        summa_to_add = get_to_sum(user_sum.get("id"), int(to_), currency_to)
        user_to_reset = user.useridentificator.strip()
    for summa_to_add in summa_to_add:
        summa_to_add.moneysum -= float(summa_delete)
        summa_to_add.moneysum += float(new_entered_summa)

    # add new data
    database.session.add(summa_to_add)
    database.session.commit()
    accounts = Accountstatus(
        money=summa_to_add.id,
        date=date,
        comments=info,
        addedsumma=str(new_entered_summa) + " " + form.currency_to.data
        if new_entered_summa
        else None,
        deletedsumma=None,
        number=None,
        percent=None,
        isexchanged=0,
        ismoved=1,
        ismodified=s["UUID"],
        isdeleted=False,
        pairidentificator=added,
        useridentificator=user_to_reset,
    )
    database.session.add(accounts)
    database.session.commit()


def update_exchange_commands(form, summa_add, summa_delete, added):
    sum_ = form.get("summa")
    user = get_user_by_UUID(s["UUID"].strip())
    user = user.get("id")
    user_to_reset = ""
    info = form.get("comments")
    date = str(form.get("date")) + " " + str(datetime.datetime.now().time())

    # gets deleted
    from_ = form.get("wallet_from")
    from_ = get_current_wallet_by_name(from_)
    currency_from = form.get("valuta_sold")
    summa_to_delete = get_to_sum(user, int(from_), currency_from)

    if summa_to_delete is None:
        currency_from = get_current_currency_by_name(currency_from).id
        user = Accountstatus.query.filter_by(pairidentificator=added).first()
        user_sum = get_user_by_UUID(user.useridentificator.strip())
        summa_to_delete = get_to_sum(user_sum.get("id"), int(from_), currency_from)
        user_to_reset = user.useridentificator.strip()
    for summa_to_delete in summa_to_delete:
        summa_to_delete.moneysum += float(summa_add)
        summa_to_delete.moneysum += 0 - float(sum_)
    status = Accountstatus.query.filter_by(pairidentificator=added).all()
    for ss in status:
        database.session.delete(ss)
        database.session.commit()

    # add new data
    database.session.add(summa_to_delete)
    database.session.commit()
    accounts = Accountstatus(
        money=summa_to_delete.id,
        date=date,
        comments=info,
        addedsumma=None,
        deletedsumma=str(sum_) + " " + form.get("valuta_sold") if sum_ else None,
        number=None,
        percent=None,
        isexchanged=1,
        ismoved=0,
        ismodified=s["UUID"],
        isdeleted=False,
        pairidentificator=added,
        useridentificator=user_to_reset,
    )
    database.session.add(accounts)
    database.session.commit()

    # get added
    to_ = form.get("wallet_to")
    to_ = get_current_wallet_by_name(to_)
    currency_to = form.get("valuta_buy")
    summa_to_add = get_to_sum(user.id, int(to_), currency_to)
    print(form.get("rate_exchange"))
    new_entered_summa = float(sum_) * float(form.get("rate_exchange"))
    # if summa is none then get user
    if summa_to_add is None:
        currency_to = get_current_currency_by_name(currency_to).id
        user = Accountstatus.query.filter_by(pairidentificator=added).first()
        user_sum = get_user_by_UUID(user.useridentificator.strip())
        summa_to_add = get_to_sum(user_sum.get("id"), int(to_), currency_to)
        user_to_reset = user.useridentificator.strip()
    for summa_to_add in summa_to_add:
        summa_to_add.moneysum -= float(summa_delete)
        summa_to_add.moneysum += float(new_entered_summa)

    # add new data
    database.session.add(summa_to_add)
    database.session.commit()
    accounts = Accountstatus(
        money=summa_to_add.id,
        date=date,
        comments=info,
        addedsumma=str(new_entered_summa) + " " + form.get("valuta_buy")
        if new_entered_summa
        else None,
        deletedsumma=None,
        number=None,
        percent=None,
        isexchanged=1,
        ismoved=0,
        ismodified=s["UUID"],
        isdeleted=False,
        pairidentificator=added,
        useridentificator=user_to_reset,
    )
    database.session.add(accounts)
    database.session.commit()


def create_dict(comments: list, transpone: list, user: int) -> list[dict]:
    """
    This module create dict of current list
    :param comments: list to change
    :param transpone: tuple to transpone into list
    :param user: current user
    :return: new created dict
    """
    comments.append(
        {
            "id": transpone[8],
            "date": transpone[0],
            "comment": transpone[1],
            "addedsumma": transpone[2],
            "deletedsumma": transpone[3],
            "user": transpone[4],
            "wallet": transpone[5],
            "UUID": transpone[6],
            "visibility": transpone[7],
            "number": transpone[9],
            "exchanged": transpone[10],
            "moved": transpone[11],
            "pairs": transpone[12].strip(),
            "modified": user,
            "deleted": transpone[14],
            "superuser": s["superuser"],
            "general": transpone[15]
        }
    )
    return comments


def create_result_comments(result: list[tuple], comments: list) -> list[dict]:
    """
    This module creates list of comments to show user
    :param result: result of query database
    :param comments: list to add new data
    :return: list of dicts of comments
    """
    if result:
        for details in result:
            transpone = list(details)
            user = get_user_by_UUID(transpone[13].strip())
            if user is not None:
                user = user.get("user")
            else:
                user = None
            if s["superuser"]:
                # if superuser then check only with user roots
                '''wallet = get_current_wallet_by_name(transpone[5])
                usr = get_user_by_UUID(transpone[6].strip()).get("id")
                root = get_user_root(usr, wallet).isgeneral
                if root:'''
                create_dict(comments, transpone, user)
            else:
                # check current user roots
                wallet = get_current_wallet_by_name(transpone[5])
                usr = get_user_by_UUID(s["UUID"].strip()).get("id")
                root = get_user_root(usr, wallet).isgeneral
                if not root and transpone[6] == s["UUID"]:
                    create_dict(comments, transpone, user)
                elif root and (transpone[6] == s["UUID"] or transpone[6] != s["UUID"]):
                    # if if general then check each user root
                    wallet = get_current_wallet_by_name(transpone[5])
                    usr = get_user_by_UUID(transpone[6].strip()).get("id")
                    root = get_user_root(usr, wallet).isgeneral
                    if root:
                        create_dict(comments, transpone, user)
    return comments
