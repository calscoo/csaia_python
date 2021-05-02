from daos import users_dao
from enums.role import roles
from managers.tools import password_manager

#Create user method
from objects.user import user

import random
import string

# This method is no longer used. Was previously used for testing purposes
def create_user_testing(email, password, role):
    users_record = []
    users_record.insert(0, (email, password_manager.get_hashed_password(password), role.value, 0))
    users_dao.insert_users(users_record)


def create_user(email, password, role, admin_id, admin_pass):
    """
    Creates a new user

    Parameters
    ----------
    email : string
        The user's email
    password : string
        The user's password
    role : roles
        The users role in the application.
    admin_id : integer
        The user's id if an admin
    admin_pass : string
        The user's admin password

    Returns
    -------
    True if account was successfully created. False if the account failed to be created    
    """
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
    """
    Updates the role of a user, can be used to upgrade or disable users

    Parameters
    ----------
    user_id : integer
        The id of the user
    role : roles
        The users role in the application.
    admin_id : integer
        The user's admin id
    admin_pass : string
        The user's admin password

    Returns
    -------
    True if account was successfully updated. False if the account failed to be updated    
    """
    assert user_id and role and role and admin_id and admin_pass is not None
    admin_user = fetch_users([admin_id], None, None, None)[0]
    if password_manager.check_password(admin_pass, admin_user.password):
        if role == roles.Disabled:
            users_dao.update_user_api_key(user_id, None)
        users_dao.update_user(user_id, None, role.value, None)
        return True
    else:
        return False


def update_user_pass(user_id, old_pass, new_pass):
    """
    Updates the user's password

    Parameters
    ----------
    users_id : integer
        The id of the user
    old_pass : string
        The user's old password
    new_pass : string
        The user's new password that's to replace old_pass

    Returns
    -------
    True if account was successfully updated. False if the account failed to be updated    
    """
    user = fetch_users([user_id], None, None, None)[0]
    if user is not None and password_manager.check_password(old_pass, user.password):
        users_dao.update_user(user_id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 0)
        return True
    else:
        return False



def admin_update_user_pass(user_id, new_pass, admin_id, admin_pass):
    """
    Method for updating user passwords. set old_pass to null to bypass previous password check

    Parameters
    ----------
    user_id : integer
        The id of the user
    new_pass : string
        The new password to replace previous password
    admin_id : integer
        The user's id if an admin
    admin_pass : string
        The user's admin password

    Returns
    -------
    True if account was successfully updated. False if the account failed to be updated    
    """
    assert user_id and new_pass and admin_id and admin_pass is not None
    user = fetch_users([user_id], None, None, None)[0]
    admin_user = fetch_users([admin_id], None, None, None)[0]
    if user is not None and password_manager.check_password(admin_pass, admin_user.password):
        users_dao.update_user(user_id, password_manager.get_hashed_password(new_pass).decode('utf-8'), None, 1)
        return True
    else:
        return False


def fetch_user_role(id):
    """
    Fetches users role based on the passed id

    Parameters
    ----------
    id : integer
        The id of the user to be found

    Returns
    -------
    user : user object 
        Returns the users with the matching id
    """
    if id is not None:
        return users_dao.select_users('role', [id], None, None, None, None, None)[0][0]


def verify_api_key(api_key):
    """
    Verifies the user's api key to make sure the user is valid

    Parameters
    ----------
    api_key : string
        The passed api_key that's to be verified

    Returns
    -------
    True if account was successfully verified. False if the account isn't verified    
    """
    if api_key is None or api_key == '':
        return False

    # web interface api key
    if api_key == 'vsRV7QBUP3EQGaD4wPbMjzUC2':
        return True

    ids = users_dao.select_users('id', None, None, None, None, None, api_key)

    return len(ids) > 0


def fetch_user_api_key(id, password):
    """
    Obtains the user's api key

    Parameters
    ----------
    id : integer
        The user's id
    password : string
        The user's password

    Returns
    -------
    api_key : string
        Returns the user's api key. Return's None if there is no password found 
    """
    if id is not None and password is not None:
        db_pass = users_dao.select_users('password', [id], None, None, None, None, None)

        if len(db_pass) == 0:
            return None

        if password_manager.check_password(password, db_pass[0][0]):
            api_key = users_dao.select_users('api_key', [id], None, None, None, None, None)
            return api_key[0][0]

    return None


def generate_user_api_key(id, password):
    """
    Generates an api key for a user

    Parameters
    ----------
    id : integer
        The user's id
    password : string
        The user's password

    """
    if id is not None and password is not None:
        db_pass = users_dao.select_users('password', [id], None, None, None, None, None)

        if len(db_pass) == 0:
            return None

        if password_manager.check_password(password, db_pass[0][0]):
            api_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))

            users_dao.update_user_api_key(id, api_key)
            return api_key
    return None


def fetch_all_users():
    """
    Fetch all users for admin view

    Parameters
    ----------
    None

    Returns
    -------
    List of all users
    """
    return users_rs_to_object_list(users_dao.select_all_users('*'))


def check_force_password_reset(user_id):
    if user_id is not None:
        return int(str(users_dao.select_users('force_reset', [user_id], None, None, None, None, None)[0][0]))


def fetch_shareable_user_ids(sharing_id, share_ids):
    """
    Fetch the valid user ids to share a flight with
    The sharing user, disabled users and non-existent users will be filtered out.

    Parameters
    ----------
    sharing_id : integer
        The user id that is sharing the flight
    share_ids : list[int]
        The user ids that the flight will be shared with

    Returns
    -------
    List of valid ids to share the flight with
    """
    sharable_ids = []
    potential_sharable_users = users_rs_to_object_list(users_dao.select_users('*', share_ids, None, None, None, None, None))
    for user in potential_sharable_users:
        if not (user.role == roles.Disabled or str(user.id) == str(sharing_id)):
            sharable_ids.append(user.id)

    return sharable_ids


def fetch_users(ids, email, password, role):
    """
    Fetch all users based on the passed values

    Parameters
    ----------
    ids : list[int]
        The ids of the users
    email : string
        The email of the users
    password : string
        The password of the users
    role : roles
        The role of the users

    Returns
    -------
    List of all users that have the passed parameters
    """
    return users_rs_to_object_list(users_dao.select_users('*', ids, email, password, None if role is None else role.value, None, None))


def does_user_exist(email):
    """
    Determines if the user exists in the database

    Parameters
    ----------
    email : string
        The user's email

    Returns
    -------
    Return whether the email exists in the system
    """
    return fetch_users(None, email, None, None).__len__() > 0


def validate_login_credentials(email, password):
    """
    A validation method used for login

    Parameters
    ----------
    email : string
        The user's email
    password : string
        The user's password

    Returns
    -------
    Returns the id of the user if the login is successful, -1 otherwise.
    """
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
    """
    Stores all users into a list of users

    Parameters
    ----------
    rs : user objects
        Data of a user

    Returns
    -------
    users[list]
        Returns a list of users
    """
    users = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                users.append(user(tuple[0], tuple[1], tuple[2], roles(int(str(tuple[3]))), tuple[4], tuple[5]))
    return users
