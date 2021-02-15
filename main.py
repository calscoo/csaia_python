import os
import exifread
from GPSPhoto import gpsphoto
from mysql.connector import connect, Error

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

insert_images_query = """
INSERT INTO images(flight_id, directory_location, image_extension, datetime, latitude, 
longitude, altitude, image_width, image_height, exposure_time, 
f_number, iso_speed, metering_mode, focal_length, light_source, 
exposure_mode, white_balance, gain_control, contrast, saturation, 
sharpness, image_compression, exif_version, software_version, 
hardware_make, hardware_model, hardware_serial_number)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def none_check_str(val):
    return None if val is None else str(val)


def none_check_float(val):
    return None if val is None else float(val)


def none_check_int(val):
    return None if val is None else int(str(val))

image_records = []
for root, subdirs, files in os.walk('C:\\Users\\Caleb\\Downloads\\CCAST_CSAIA2'):
    oneImage = False
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in ('.jpg', '.jpeg', '.tif', '.tiff'):
            imgPath = os.path.join(root, file)
            tags = exifread.process_file(open(imgPath, 'rb'))
            gpsData = gpsphoto.getGPSData(imgPath)

            Latitude = none_check_float(gpsData.get('Latitude'))
            Longitude = none_check_float(gpsData.get('Longitude'))
            Altitude = none_check_float(gpsData.get('Altitude'))
            DateTime = none_check_str(tags.get('Image DateTime'))
            ExposureTime = none_check_str(tags.get('EXIF ExposureTime'))
            FNumber = none_check_str(tags.get('EXIF FNumber'))
            MeteringMode = none_check_str(tags.get('EXIF MeteringMode'))
            FocalLength = none_check_str(tags.get('EXIF FocalLength'))
            ExifVersion = none_check_str(tags.get('EXIF ExifVersion'))
            Software = none_check_str(tags.get('Image Software'))
            Make = none_check_str(tags.get('Image Make'))
            Model = none_check_str(tags.get('Image Model'))
            BodySerialNumber = none_check_str(tags.get('EXIF BodySerialNumber'))
            LightSource = none_check_str(tags.get('EXIF LightSource'))
            WhiteBalance = none_check_str(tags.get('EXIF WhiteBalance'))
            GainControl = none_check_str(tags.get('EXIF GainControl'))
            Contrast = none_check_str(tags.get('EXIF Contrast'))
            Saturation = none_check_str(tags.get('EXIF Saturation'))
            Sharpness = none_check_str(tags.get('EXIF Sharpness'))
            Compression = none_check_str(tags.get('Image Compression'))

            ImageWidth = none_check_int(tags.get('Image ImageWidth')) or none_check_int(tags.get('EXIF ExifImageWidth'))
            ImageLength = none_check_int(tags.get('Image ImageLength')) or none_check_int(tags.get('EXIF ExifImageLength'))
            ISOSpeed = none_check_int(tags.get('EXIF ISOSpeed')) or none_check_int(tags.get('EXIF ISOSpeedRatings'))
            ExposureProgram = none_check_str(tags.get('EXIF ExposureProgram')) or none_check_str(tags.get('EXIF ExposureMode'))

            image_records.insert(0, (None, str(imgPath), str(ext), DateTime, Latitude,
                                     Longitude, Altitude, ImageWidth, ImageLength, ExposureTime,
                                     FNumber, ISOSpeed, MeteringMode, LightSource, FocalLength,
                                     ExposureProgram, WhiteBalance, GainControl, Contrast, Saturation,
                                     Sharpness, Compression, ExifVersion, Software,
                                     Make, Model, BodySerialNumber))

try:
    with connect(
        host="localhost",
        user="root",
        password="Password1234",
        database="csaia_database",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_images_query, image_records)
        connection.commit()
except Error as e:
    print(e)
