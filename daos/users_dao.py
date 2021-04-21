from pypika import Query, Table
from daos.tools import dao_tools
import mysql.connector

insert_users_query = """ 
INSERT INTO users(email, password, role) 
VALUES (%s, %s, %s)"""

update_users_query = """
    UPDATE users 
    SET role = %s
    WHERE email = %s
    """

def insert_users(users_records):
    return dao_tools.execute(insert_users_query, users_records)


def update_user(id, password, role, force_reset):
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


def update_user_api_key(id, password, api_key):
    if id is not None and (password is not None or api_key is not None):
        users = Table('users')
        select_user_query = Query.update(users)
        if password is not None:
            select_user_query = select_user_query.set(users.password, password)
        if api_key is not None:
            select_user_query = select_user_query.set(users.api_key, api_key)
        select_user_query = select_user_query.where(users.id.isin([id]))
        dao_tools.execute(select_user_query)


def select_users(select_columns, ids, email, password, role, force_reset, api_key):
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
    return select_users(select_columns, None, None, None, None, None, None)
