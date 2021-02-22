import os
import exifread
from daos import image_dao
from GPSPhoto import gpsphoto

supported_formats = ('.jpg', '.jpeg', '.tif', '.tiff')


def none_check_str(val):
    return None if val is None else str(val)


def none_check_float(val):
    return None if val is None else float(val)


def none_check_int(val):
    return None if val is None else int(str(val))


def upload_images(bulk_dir):
    image_records = []
    for root, subdirs, files in os.walk(bulk_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_formats:
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

                image_records.insert(0, (None, None, str(imgPath), str(ext), DateTime, Latitude,
                                         Longitude, Altitude, ImageWidth, ImageLength, ExposureTime,
                                         FNumber, ISOSpeed, MeteringMode, LightSource, FocalLength,
                                         ExposureProgram, WhiteBalance, GainControl, Contrast, Saturation,
                                         Sharpness, Compression, ExifVersion, Software,
                                         Make, Model, BodySerialNumber))

    image_dao.insert_images(image_records)


def fetch_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model):
    return image_dao.select_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model)
