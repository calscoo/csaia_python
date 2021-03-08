from managers import flight_manager, image_manager
from objects.range import range

image_directory = 'C:\\Users\\Caleb\\Downloads\\CCAST_CSAIA2'

# result = flight_manager.build_flight(image_directory, 'Test1', 'Test1', 'Test1', 'Test1')
# print(str(result))
# flight_manager.build_flight(image_directory, 'Test2', 'Test2', 'Test2', 'Test2')
image_manager.remove_images([24])
flight_manager.remove_flight(4)
flight_manager.remove_flight(1)
flight_manager.remove_flight(3)

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
