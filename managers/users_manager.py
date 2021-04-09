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


# Fetch all users for admin view
def fetch_all_users():
    return users_rs_to_object_list(users_dao.select_all_users('*'))


# Fetch all users for admin view
def fetch_users(id, email, password, role):
    return users_rs_to_object_list(users_dao.select_users('*', id, email, password, None if role is None else role.value))


def does_user_exist(email):
    return fetch_users(None, email, None, None).__len__() > 0


def users_rs_to_object_list(rs):
    users = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                users.append(user(tuple[0], tuple[1], tuple[2], roles(int(str(tuple[3])))))
    return users
