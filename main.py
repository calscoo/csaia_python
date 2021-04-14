import os
import re

from enums.privacy import privacy
from enums.role import roles
from managers import flight_manager, image_manager, users_manager, shared_flight_manager
from objects.range import range

image_directory = 'C:/Users/Caleb/Downloads/csaia/CCAST_CSAIA2/CREC_FieldsP1P2P3_P4P_200ft_05092018'

# flight_manager.build_flight(image_directory, 'Test1', 'Test1', 'Test1', 'Test1', privacy.Public, None)
# print(image_manager.fetch_images(1, [5, 6, 7, 8], None, None, None, None, None, None, None, None, None, None, None))
# cur_time = datetime.now().strftime(time_format)
# flight_manager.build_flight(image_directory,'Test2', 'Test2', 'Test2', 'Test2')
# image_manager.remove_images([314, 315, 316, 317, 318, 319, 320, 321])
# users_manager.make_admin('JohnTestAdmin@ThisIsATest.com', 'Passw0rd')
# users_manager.reinstate_user('JohnTestAdmin@ThisIsATest.com')
# users_manager.update_admin('JohnTest@ThisIsATest.com')
# shared_flight_manager.share_flight(1666, [4, 5])
# users = shared_flight_manager.fetch_shared_flight_users(1700)
# print(users)

# image_manager.image_data_to_csv(image_manager.parse_image_metadata(image_directory))
print(users_manager.fetch_user_role(5))


"""
image_ids = None
user_ids = None
flight_ids = [1666, 1667, 1668]
# extensions = ['.png', '.jpg', '.tif']
# datetime_range = range('2012-01-01 00:00:00', '2022-01-01 00:00:00')
# latitude_range = range(44, 50)
# longitude_range = range(-200, 200)
# altitude_range = range(100, 1000)
extensions = None
datetime_range = None
latitude_range = None
longitude_range = None
altitude_range = None
make = None
model = None
# #
images = image_manager.fetch_images(6, image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model)
flight_ids_returned = set()
for image in images:
    flight_ids_returned.add(image.flight_id)
print(flight_ids_returned)
# for image in images:
#     print(str(image))
"""
"""
test = "this/is/a/string/directory/of/foo/bar/goodness/butt/cheese/accident"
parts = test.split('/')[-4:]
result = ""
for part in parts:
    result = result + part + "/"
print("in: " + test)
print("out: " + result)
"""