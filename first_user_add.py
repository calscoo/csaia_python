import os

from enums.role import roles
from managers import flight_manager, users_manager, image_manager


# Creates the very first user in CSAIA.
# This file needs to be executed on the command line, since user creation typically requires an admin and non exist yet.
# This method is NOT available through the API
users_manager.create_user_testing("user1", "pass", roles.Admin)
