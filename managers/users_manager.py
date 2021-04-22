from daos import users_dao
from enums.role import roles
from managers.tools import password_manager

#Create user method
from objects.user import user

import random
import string


def create_user_testing(email, password, role):
    users_record = []
    users_record.insert(0, (email, password_manager.get_hashed_password(password), role.value, 0))
    users_dao.insert_users(users_record)


def create_user(email, password, role, admin_id, admin_pass):
    assert email and password and role and admin_id and admin_pass is not None
    users_record = []
    admin_user = fetch_users([admin_id], None, None, None)[0]
    if password_manager.check_password(admin_pass, admin_user.password):
        users_record.insert(0, (email, password_manager.get_hashed_password(password), role.value, 1))
        users_dao.insert_users(users_record)
        return True
    else:
        return False


def update_user_role(user_id, role, admin_id, admin_pass):
    assert user_id and role and role and admin_id and admin_pass is not None
    admin_user = fetch_users([admin_id], None, None, None)[0]
    if password_manager.check_password(admin_pass, admin_user.password):
        if role == roles.Disabled:
            users_dao.update_user_api_key(user_id, None)
        users_dao.update_user(user_id, None, role.value, None)
        return True
    else:
        return False


# Method for updating user passwords.
def update_user_pass(user_id, old_pass, new_pass):
    user = fetch_users([user_id], None, None, None)[0]
    if user is not None and password_manager.check_password(old_pass, user.password):
        users_dao.update_user(user_id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 0)
        return True
    else:
        return False


# Method for updating user passwords. set old_pass to null to bypass previous password check
def admin_update_user_pass(user_id, new_pass, admin_id, admin_pass):
    assert user_id and new_pass and admin_id and admin_pass is not None
    user = fetch_users([user_id], None, None, None)[0]
    admin_user = fetch_users([admin_id], None, None, None)[0]
    if user is not None and password_manager.check_password(admin_pass, admin_user.password):
        users_dao.update_user(user_id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 1)
        return True
    else:
        return False


def fetch_user_role(id):
    if id is not None:
        return users_dao.select_users('role', [id], None, None, None, None, None)[0][0]


def verify_api_key(api_key):
    if api_key is None or api_key == '':
        return False

    # web interface api key
    if api_key == 'vsRV7QBUP3EQGaD4wPbMjzUC2':
        return True

    ids = users_dao.select_users('id', None, None, None, None, None, api_key)

    return len(ids) > 0


def fetch_user_api_key(id, password):
    if id is not None and password is not None:
        db_pass = users_dao.select_users('password', [id], None, None, None, None, None)

        if len(db_pass) == 0:
            return None

        if password_manager.check_password(password, db_pass[0][0]):
            api_key = users_dao.select_users('api_key', [id], None, None, None, None, None)
            return api_key[0][0]

    return None


def generate_user_api_key(id, password):
    if id is not None and password is not None:
        db_pass = users_dao.select_users('password', [id], None, None, None, None, None)

        if len(db_pass) == 0:
            return None

        if password_manager.check_password(password, db_pass[0][0]):
            api_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))

            users_dao.update_user_api_key(id, api_key)
            return api_key
    return None


# Fetch all users for admin view
def fetch_all_users():
    return users_rs_to_object_list(users_dao.select_all_users('*'))


def check_force_password_reset(user_id):
    if user_id is not None:
        return int(str(users_dao.select_users('force_reset', [user_id], None, None, None, None, None)[0][0]))


# Fetch users
def fetch_users(ids, email, password, role):
    return users_rs_to_object_list(users_dao.select_users('*', ids, email, password, None if role is None else role.value, None, None))


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
                users.append(user(tuple[0], tuple[1], tuple[2], roles(int(str(tuple[3]))), tuple[4], tuple[5]))
    return users
