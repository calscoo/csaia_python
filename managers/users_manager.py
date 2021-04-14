from daos import users_dao
from enums.role import roles

#Create user method
from objects.user import user


def create_user(email, password, role):
    users_record = []
    users_record.insert(0, (email, password, role.value))
    users_dao.insert_users(users_record)


def update_user_role(id, role):
    users_dao.update_user(id, None, role.value)


def fetch_user_role(id):
    if id is not None:
        return users_dao.select_users('role', id, None, None, None)[0][0]


# Fetch all users for admin view
def fetch_all_users():
    return users_rs_to_object_list(users_dao.select_all_users('*'))


# Fetch all users for admin view
def fetch_users(id, email, password, role):
    return users_rs_to_object_list(users_dao.select_users('*', id, email, password, None if role is None else role.value))


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
    if user.password != password or user.role == roles.Disabled:
        return -1
    return user.id


def users_rs_to_object_list(rs):
    users = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                users.append(user(tuple[0], tuple[1], tuple[2], roles(int(str(tuple[3])))))
    return users
