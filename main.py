import os

from enums.role import roles
from managers import flight_manager, users_manager
from daos import flight_dao
from objects.flight import flight as flight_o

image_directory = 'C:/Users/Zach Kunz/Documents/CCAST_CSAIA2/CREC_FieldsP1P2P3_P4P_200ft_05092018'

# rs = flight_dao.select_flights('*', None, None, None, None, None, None, None, None, None, None, None, None, None, None)
# flights = flight_manager.flights_rs_to_object_list(rs)
# for flight in flights:
#     lat = flight.average_latitude
#     lon = flight.average_longitude
#     if lat is not None and lon is not None and flight.address is None:
#         address = flight_manager.flight_address(lat, lon)
#         address_flight_object = flight_o(None, None, None, None, address, None, None, None, None, None, None, None, None, None, None)
#         print(address_flight_object.address)
#         flight_dao.update_flight(flight.id, address_flight_object)


# users_manager.create_user("user", "pass", roles.Admin)
# directory_name = 'CSV_Files'
# file_name = '12345_' + cur_time
# csv_name = directory_name
# os.mkdir(directory_name)
flight_manager.remove_flight(2049)
