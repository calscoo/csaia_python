import os

from enums.role import roles
from managers import flight_manager, users_manager, image_manager

image_directory = 'C:/Users/Zach Kunz/Documents/CCAST_CSAIA2/CREC_FieldsP1P2P3_P4P_200ft_05092018'


users_manager.create_user_testing("user1", "pass", roles.Admin)
users_manager.create_user_testing("user2", "pass", roles.Admin)
users_manager.create_user_testing("user3", "pass", roles.Admin)

