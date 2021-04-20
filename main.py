import os

from enums.role import roles
from managers import flight_manager, users_manager
from daos import flight_dao
from objects.flight import flight as flight_o

image_directory = 'C:/Users/Zach Kunz/Documents/CCAST_CSAIA2/CREC_FieldsP1P2P3_P4P_200ft_05092018'


users_manager.create_user("user1", "pass", roles.Admin)
users_manager.create_user("user2", "pass", roles.Admin)
users_manager.create_user("user3", "pass", roles.Admin)
