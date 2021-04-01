from daos import users_dao

#Create user method
def make_user(email, password):
    users_record = []
    setEmail = email
    setPassword = password
    role = 2 #Basic user
    users_record.insert(0, (setEmail, setPassword, role))
    users_dao.insert_users(users_record)

#Create Admin method
def make_admin(email, password):
    users_record = []
    setEmail = email
    setPassword = password
    role = 1 #Admin user
    users_record.insert(0, (setEmail, setPassword, role))
    users_dao.insert_users(users_record)


def update_admin(email):
    role = 1
    users_dao.update_users(email, role)


def disable_user(email):
    role = 3
    users_dao.update_users(email, role)

# Restore admin or disabled user to a normal user
def reinstate_user(email):
    role = 2
    users_dao.update_users(email, role)