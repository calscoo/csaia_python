from pypika import Query, Table
from daos.tools import dao_tools
import mysql.connector

insert_users_query = """ 
INSERT INTO users(email, password, role, force_reset) 
VALUES (%s, %s, %s, %s)"""

update_users_query = """
    UPDATE users 
    SET role = %s
    WHERE email = %s
    """

def insert_users(users_records):
    return dao_tools.execute(insert_users_query, users_records)


def update_user(id, password, role, force_reset):
    """
    Updates user data to passed data in the SQL database

    Parameters
    ----------
    id : integer
    password : string
    role : integer
    force_reset : integer or None

    """
    if id is not None and (password is not None or role is not None):
        users = Table('users')
        update_user_query = Query.update(users)
        if password is not None:
            update_user_query = update_user_query.set(users.password, password)
        if role is not None:
            update_user_query = update_user_query.set(users.role, role)
        if force_reset is not None:
            update_user_query = update_user_query.set(users.force_reset, force_reset)
        update_user_query = update_user_query.where(users.id.isin([id]))
        dao_tools.execute(update_user_query)


def update_user_api_key(id, api_key):
    """
    Updates the user's API key based on the passed user id

    Parameters
    ----------
    id : integer
    api_key : string or None

    """
    if id is not None:
        users = Table('users')
        select_user_query = Query.update(users)
        select_user_query = select_user_query.set(users.api_key, api_key)
        select_user_query = select_user_query.where(users.id.isin([id]))
        dao_tools.execute(select_user_query)


def select_users(select_columns, ids, email, password, role, force_reset, api_key):
    """
    Selects users based on the passed parameters

    Parameters
    ----------
    select_columns : string or None
    ids : integer
    email: string
    password : string
    role : integer
    force_reset : integer or None
    api_key : string or None

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    users = Table('users')
    select_users_query = Query.from_(users).select('*' if select_columns is None else select_columns)
    if ids is not None:
        select_users_query = select_users_query.where(users.id.isin(ids))
    if email is not None:
        select_users_query = select_users_query.where(users.email.isin([email]))
    if password is not None:
        select_users_query = select_users_query.where(users.password.isin([password]))
    if role is not None:
        select_users_query = select_users_query.where(users.role.isin([role]))
    if force_reset is not None:
        select_users_query = select_users_query.where(users.force_reset.isin([force_reset]))
    if api_key is not None:
        select_users_query = select_users_query.where(users.api_key.isin([api_key]))

    return dao_tools.execute(select_users_query)

def select_all_users(select_columns):
    """
    Selects all users based on the passed column

    Parameters
    ----------
    select_columns : string

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    return select_users(select_columns, None, None, None, None, None, None)
