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


def update_user(id, password, role):
    if id is not None and (password is not None or role is not None):
        users = Table('users')
        select_user_query = Query.update(users)
        if password is not None:
            select_user_query = select_user_query.set(users.password, password)
        if role is not None:
            select_user_query = select_user_query.set(users.role, role)
        select_user_query = select_user_query.where(users.id.isin([id]))
        dao_tools.execute(select_user_query)


def select_users(select_columns, id, email, password, role):
    users = Table('users')
    select_users_query = Query.from_(users).select('*' if select_columns is None else select_columns)
    if id is not None:
        select_users_query = select_users_query.where(users.id.isin([id]))
    if email is not None:
        select_users_query = select_users_query.where(users.email.isin([email]))
    if password is not None:
        select_users_query = select_users_query.where(users.password.isin([password]))
    if role is not None:
        select_users_query = select_users_query.where(users.role.isin([role]))
    return dao_tools.execute(select_users_query)

def select_all_users(select_columns):
    return select_users(select_columns, None, None, None, None)
