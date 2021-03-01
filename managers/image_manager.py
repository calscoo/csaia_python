import os
import exifread
import re
from objects.image import image
from daos import image_dao
from GPSPhoto import gpsphoto

supported_formats = ('.jpg', '.jpeg', '.tif', '.tiff')


def none_check_str(val):
    return None if val is None else str(val)

def get_Latitude():
    return sum(latitudeList) / len(latitudeList)

def get_Longitude():
    return sum(longitudeList) / len(longitudeList)

def get_Altitude():
    return sum(altitudeList) / len(altitudeList)

def get_start_Time():
    timeList.sort()
    return timeList[0]

def get_end_Time():
    timeList.sort()
    return timeList[-1]

def get_Make():
    return makeList[0]

def get_Model():
    return modelList[0]

latitudeList = []
longitudeList = []
altitudeList = []
timeList = []
makeList = []
modelList = []

def handle_integer_parse_errors(val):
    if val is None:
        return None
    try:
        int(str(val))
    except ValueError:
        return None
    return val


def fix_quotes(val):
    return re.sub("'", "\\'", val)


def images_rs_to_object_list(rs):
    images = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                images.append(image(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7], tuple[8], tuple[9], tuple[10], tuple[11], tuple[12], tuple[13], tuple[14], tuple[15], tuple[16], tuple[17], tuple[18], tuple[19], tuple[20], tuple[21], tuple[22], tuple[23], tuple[24], tuple[25], tuple[26], tuple[27], tuple[28]))
    return images


def upload_images(bulk_dir):
    image_records = []
    for root, subdirs, files in os.walk(bulk_dir):
        for file in files:
            path = os.path.join(root, file)
            if path.lower().endswith(supported_formats):
                try:
                    tags = exifread.process_file(open(path, 'rb'))
                    gps_data = gpsphoto.getGPSData(path)
                except:
                    raise RuntimeError('Failed to parse image metadata for: ' + str(path))
                path_to_store = fix_quotes(path)
                ext = os.path.splitext(file)[1].lower()
                latitude = none_check_str(gps_data.get('Latitude'))
                longitude = none_check_str(gps_data.get('Longitude'))
                altitude = none_check_str(gps_data.get('Altitude'))
                date_time = none_check_str(tags.get('Image DateTime'))
                exposure_time = none_check_str(tags.get('EXIF ExposureTime'))
                f_number = none_check_str(tags.get('EXIF FNumber'))
                metering_mode = none_check_str(tags.get('EXIF MeteringMode'))
                focal_length = none_check_str(tags.get('EXIF FocalLength'))
                exif_version = none_check_str(tags.get('EXIF ExifVersion'))
                software_version = none_check_str(tags.get('Image Software'))
                hardware_make = none_check_str(tags.get('Image Make'))
                hardware_model = none_check_str(tags.get('Image Model'))
                hardware_serial_number = none_check_str(tags.get('EXIF BodySerialNumber'))
                light_source = none_check_str(tags.get('EXIF LightSource'))
                white_balance = none_check_str(tags.get('EXIF WhiteBalance'))
                gain_control = none_check_str(tags.get('EXIF GainControl'))
                contrast = none_check_str(tags.get('EXIF Contrast'))
                saturation = none_check_str(tags.get('EXIF Saturation'))
                sharpness = none_check_str(tags.get('EXIF Sharpness'))
                image_compression = none_check_str(tags.get('Image Compression'))

                image_height = handle_integer_parse_errors(none_check_str(tags.get('Image ImageWidth')) or none_check_str(tags.get('EXIF ExifImageWidth')))
                image_width = handle_integer_parse_errors(none_check_str(tags.get('Image ImageLength')) or none_check_str(tags.get('EXIF ExifImageLength')))
                iso_speed = handle_integer_parse_errors(none_check_str(tags.get('EXIF ISOSpeed')) or none_check_str(tags.get('EXIF ISOSpeedRatings')))
                exposure_mode = none_check_str(tags.get('EXIF ExposureProgram')) or none_check_str(tags.get('EXIF ExposureMode'))

                latitudeList.insert(0, float(latitude))
                longitudeList.insert(0, float(longitude))
                altitudeList.insert(0, float(altitude))
                timeList.insert(0, date_time)
                makeList.insert(0, hardware_make)
                modelList.insert(0, hardware_model)

                image_records.insert(0, (None, None, str(path_to_store), str(ext), date_time, latitude,
                                         longitude, altitude, image_width, image_height, exposure_time,
                                         f_number, iso_speed, metering_mode, light_source, focal_length,
                                         exposure_mode, white_balance, gain_control, contrast, saturation,
                                         sharpness, image_compression, exif_version, software_version,
                                         hardware_make, hardware_model, hardware_serial_number))

    image_dao.insert_images(image_records)


def fetch_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model):
    rs = image_dao.select_images('*', image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model)
    return images_rs_to_object_list(rs)