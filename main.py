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
sharpness, image_compression, bits_per_sample, exif_version, software_version, 
hardware_make, hardware_model, hardware_serial_number)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
image_records = []
for root, subdirs, files in os.walk('Z:\\Pics\\2021'):
    oneImage = False
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in ('.jpg', '.jpeg', '.tif', '.tiff'):
            imgPath = os.path.join(root, file)
            f = open(imgPath, 'rb')
            tags = exifread.process_file(f)
            gpsData = gpsphoto.getGPSData(imgPath)
            #TODO change dict calls to .get to avoid KeyErrors
            if ext in ('.jpg', '.jpeg'):
                image_records.insert(0, (None, str(imgPath), str(ext), str(tags['Image DateTime']), float(gpsData['Latitude']),
                                         float(gpsData['Longitude']), float(gpsData['Altitude']), int(str(tags['EXIF ExifImageWidth'])), int(str(tags['EXIF ExifImageLength'])), str(tags['EXIF ExposureTime']),
                                         str(tags['EXIF FNumber']), int(str(tags['EXIF ISOSpeedRatings'])), str(tags['EXIF MeteringMode']), str(tags['EXIF LightSource']), str(tags['EXIF FocalLength']),
                                         str(tags['EXIF ExposureMode']), str(tags['EXIF WhiteBalance']), str(tags['EXIF GainControl']), str(tags['EXIF Contrast']), str(tags['EXIF Saturation']),
                                         str(tags['EXIF Sharpness']), None, None, str(tags['EXIF ExifVersion']), str(tags['Image Software']),
                                         str(tags['Image Make']), str(tags['Image Model']), str(tags['EXIF BodySerialNumber'])))
            else:
                image_records.insert(0, (None, str(imgPath), str(ext), str(tags['Image DateTime']), float(gpsData['Latitude']),
                                         float(gpsData['Longitude']), float(gpsData['Altitude']), int(str(tags['Image ImageWidth'])), int(str(tags['Image ImageLength'])), str(tags['EXIF ExposureTime']),
                                         str(tags['EXIF FNumber']), int(str(tags['EXIF ISOSpeed'])), str(tags['EXIF MeteringMode']), None, str(tags['EXIF FocalLength']),
                                         str(tags['EXIF ExposureProgram']), None, None, None, None,
                                         None,  str(tags['Image Compression']), int(str(tags['Image BitsPerSample'])), str(tags['EXIF ExifVersion']), str(tags['Image Software']),
                                         str(tags['Image Make']), str(tags['Image Model']), str(tags['EXIF BodySerialNumber'])))

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
