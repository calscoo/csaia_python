import re

from managers import flight_manager, image_manager, users_manager
from objects.range import range

image_directory = 'C:/Users/Zach Kunz/Documents/CCAST_CSAIA2/CREC_FieldsP1P2P3_P4P_200ft_05092018'

# flight_manager.build_flight(image_directory,'Test1', 'Test1', 'Test1', 'Test1')
# flight_manager.build_flight(image_directory,'Test2', 'Test2', 'Test2', 'Test2')
# image_manager.remove_images([314, 315, 316, 317, 318, 319, 320, 321])
users_manager.make_admin('JohnTest2@ThisIsATest.com', 'Passw0rd')
# users_manager.update_admin('JohnTest@ThisIsATest.com')

# image_ids = None
# user_ids = None
# flight_ids = None
# extensions = ['.png', '.jpg', '.tif']
# datetime_range = range('2012-01-01 00:00:00', '2022-01-01 00:00:00')
# latitude_range = range(44, 50)
# longitude_range = range(-200, 200)
# altitude_range = range(100, 1000)
# make = None
# model = None
# #
# images = image_manager.fetch_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model)
# for image in images:
#     print(str(image))
"""
test = "this/is/a/string/directory/of/foo/bar/goodness/butt/cheese/accident"
parts = test.split('/')[-4:]
result = ""
for part in parts:
    result = result + part + "/"
print("in: " + test)
print("out: " + result)
"""