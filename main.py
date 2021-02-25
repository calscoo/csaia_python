from managers import image_manager
from objects.range import range

image_directory = 'C:\\Users\\Caleb\\Downloads\\CCAST_CSAIA2'

# image_manager.upload_images(image_directory)

image_ids = [1, 2, 45]
user_ids = None
flight_ids = None
extensions = ['.png', '.jpg', '.tif']
datetime_range = range('2012-01-01 00:00:00', '2022-01-01 00:00:00')
latitude_range = range(46, 48)
longitude_range = range(-100, -98)
altitude_range = range(450, 500)
make = 'mica'
model = 'edge'

print(image_manager.fetch_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model))
