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

def update_users(email, role):
    users = Table('users')
    update_query = Query.update(users).set(users.role, role).where(users.email == email)
    dao_tools.execute(update_query)


def select_users(select_columns, email, password, role):
    users = Table('users')
    select_users_query = Query.from_(users).select('*' if select_columns is None else select_columns)
    if email is not None:
        select_users_query = select_users_query.where(users.email.like('%' + email + '%'))
    if password is not None:
        select_users_query = select_users_query.where(users.password.like('%' + password + '%'))
    if role is not None:
        select_users_query = select_users_query.where(users.role.isin(role))
    return dao_tools.execute(select_users_query)

def select_all_users(select_columns):
    select_users(select_columns, None, None, None)
'''
def make_admin(email):
    admin = select_users('id', email, None, None)
    user_ids_to_promote = None if len(admin[0]) == 0 else admin[0]
    if admin is not None:
        users = Table('flights')
        make_admin_query = Query.from_(users).update(role = 1).where(users.id.isin([user_ids_to_promote]))
        dao_tools.execute(make_admin_query.get_sql(quote_char=None))

def disable_user(email):
    admin = select_users('id', email, None, None)
    user_ids_to_promote = None if len(admin[0]) == 0 else admin[0]
    if admin is not None:
        users = Table('flights')
        make_admin_query = Query.from_(users).update(role = 3).where(users.id.isin([user_ids_to_promote]))
        dao_tools.execute(make_admin_query.get_sql(quote_char=None))
'''   
