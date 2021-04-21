from daos import users_dao
from enums.role import roles
from managers.tools import password_manager

#Create user method
from objects.user import user

import random
import string

def create_user(email, password, role):
    users_record = []
    users_record.insert(0, (email, password_manager.get_hashed_password(password), role.value))
    users_dao.insert_users(users_record)


def update_user_role(id, role):
    users_dao.update_user(id, None, role.value, None)

def verify_api_key(id, api_key):
    # web interface api key
    if api_key == 'vsRV7QBUP3EQGaD4wPbMjzUC2':
        return True

    api_keys = users_dao.select_users('api_key', [id], None, None, None, None)

    if len(api_keys) == 0:
        return False

    if api_key == api_keys[0][0]:
        return True

    return False


# Method for updating user passwords. set old_pass to null to bypass previous password check
def update_user_pass(id, old_pass, new_pass):
    user = fetch_users([id], None, None, None)[0]
    if user is not None and old_pass is None:
        users_dao.update_user(id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 1)
        return True
    elif user is not None and password_manager.check_password(old_pass, user.password):
        users_dao.update_user(id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 0)
        return True
    else:
        return False


def fetch_user_role(id):
    if id is not None:
        return users_dao.select_users('role', [id], None, None, None, None)[0][0]


def fetch_user_api_key(id, password):
    if id is not None and password is not None:
        users = users_dao.select_users('api_key', [id], None, password, None, None)

        if len(users) == 0:
            return None

        return users[0][0]

        
def generate_user_api_key(id, password):
    if id is not None and password is not None:
        users = users_dao.select_users('api_key', [id], None, password, None, None)

        if len(users) == 0:
            return None

        api_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))

        users_dao.update_user_api_key(id, password, api_key)

        return api_key

    return None


# Fetch all users for admin view
def fetch_all_users():
    return users_rs_to_object_list(users_dao.select_all_users('*'))


def check_force_password_reset(user_id):
    if user_id is not None:
        return int(str(users_dao.select_users('force_reset', [user_id], None, None, None, None)[0][0]))


# Fetch users
def fetch_users(ids, email, password, role):
    return users_rs_to_object_list(users_dao.select_users('*', ids, email, password, None if role is None else role.value, None))


# Return whether the email exists in the system
def does_user_exist(email):
    return fetch_users(None, email, None, None).__len__() > 0


# fetches a user by email and returns the id of the user if the login is successful, -1 otherwise.
def validate_login_credentials(email, password):
    users = fetch_users(None, email, None, None)
    # If no user exists or more than one exists, fail login
    if users is None or len(users) != 1:
        return -1
    user = users[0]
    # If provided password doesn't match or the user is disabled, fail login
    if not password_manager.check_password(password, user.password) or user.role == roles.Disabled:
        return -1
    return user.id


def users_rs_to_object_list(rs):
    users = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                users.append(user(tuple[0], tuple[1], tuple[2], roles(int(str(tuple[3]))), tuple[4]))
    return users
