import os

from enums.role import roles
from managers import flight_manager, users_manager, image_manager


# Creates a user without admin credentials, this can't be done via the api
users_manager.create_user_testing("user1", "pass", roles.Admin)

# Creates a user the standard way, with admin id and password credentials
users_manager.create_user("user_email", "user_pass", roles.Admin, 1, "admin_pass")

# Allows an admin to update a user role
users_manager.update_user_role(1, roles.Admin, 1, "admin_pass")

# Allows a user to update their own password
users_manager.update_user_pass(1, "old_pass", "new_pass")

# Allows an admin to updates a users password
users_manager.admin_update_user_pass(1, "new_pass", 1, "admin_pass")