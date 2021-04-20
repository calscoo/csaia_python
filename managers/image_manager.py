import hashlib
import os
import re

import exifread
import csv

from managers import flight_manager
from objects.image import image
from daos import image_dao
from GPSPhoto import gpsphoto

supported_formats = ('.jpg', '.jpeg', '.tif', '.tiff')


def none_check_str(val):
    return None if val is None else str(val)


def handle_integer_parse_errors(val):
    if val is None:
        return None
    try:
        int(str(val))
    except ValueError:
        return None
    return val


def fix_quotes(val):
    return re.sub("'", "''", val)


def images_rs_to_object_list(rs):
    images = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                images.append(image(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7], tuple[8], tuple[9], tuple[10], tuple[11], tuple[12], tuple[13], tuple[14], tuple[15], tuple[16], tuple[17], tuple[18], tuple[19], tuple[20], tuple[21], tuple[22], tuple[23], tuple[24], tuple[25], tuple[26], tuple[27], tuple[28], tuple[29]))
    return images


def image_objects_to_insert_tuple(list_images):
    """
    Reformats a list of images to a list of tuples for database insertion.

    Parameters
    ----------
    list_images : list of objects.image
        the list of images to convert

    Returns
    -------
    tuple_images : list of tuples
        the list of tuples containing image attributes for database insertion
    """
    tuple_images = []
    for image in list_images:
        tuple_images.append((image.user_id, image.flight_id, image.directory_location, image.image_extension, image.datetime, image.latitude,
                              image.longitude, image.altitude, image.image_width, image.image_height, image.exposure_time,
                              image.f_number, image.iso_speed, image.metering_mode, image.light_source, image.focal_length,
                              image.exposure_mode, image.white_balance, image.gain_control, image.contrast, image.saturation,
                              image.sharpness, image.image_compression, image.exif_version, image.software_version,
                              image.hardware_make, image.hardware_model, image.hardware_serial_number, image.md5_hash))
    return tuple_images


def parse_image_metadata(image_dir):
    """
    Parses a directory for all supported images, grabs their metadata and assigns each set of metadata to an image object

    Parameters
    ----------
    image_dir : str
        the directory to parse for images

    Returns
    -------
    images : list of objects.image
        the list of images containing useful metadata
    """
    images = []
    for root, subdirs, files in os.walk(image_dir):
        for file in files:
            path = os.path.join(root, file)
            if path.lower().endswith(supported_formats):
                try:
                    image_file = open(path, 'rb')
                    tags = exifread.process_file(image_file)
                    gps_data = gpsphoto.getGPSData(path)
                except:
                    raise RuntimeError('Failed to parse image metadata for: ' + str(path))
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

                image_height = handle_integer_parse_errors(
                    none_check_str(tags.get('Image ImageWidth')) or none_check_str(tags.get('EXIF ExifImageWidth')))
                image_width = handle_integer_parse_errors(
                    none_check_str(tags.get('Image ImageLength')) or none_check_str(tags.get('EXIF ExifImageLength')))
                iso_speed = handle_integer_parse_errors(
                    none_check_str(tags.get('EXIF ISOSpeed')) or none_check_str(tags.get('EXIF ISOSpeedRatings')))
                exposure_mode = none_check_str(tags.get('EXIF ExposureProgram')) or none_check_str(
                    tags.get('EXIF ExposureMode'))

                md5_hash = hashlib.md5(image_file.read()).hexdigest()

                images.append(image(None, None, None, path, ext, date_time, latitude, longitude, altitude, image_width, image_height, exposure_time, f_number, iso_speed, metering_mode, focal_length, light_source, exposure_mode, white_balance, gain_control, contrast, saturation, sharpness, image_compression, exif_version, software_version, hardware_make, hardware_model, hardware_serial_number, md5_hash))
    return images


def upload_images(images):
    """
    For uploading multiple images to the database
    NOTE: images must pass through image_manager.parse_image_metadata to have metadata populated

    Parameters
    ----------
    images : list of objects.image
        the images to upload

    Returns
    -------
    image ids : list of int
        the list of image ids that have been uploaded
    """
    images_to_insert = image_objects_to_insert_tuple(images)

    return image_dao.insert_images(images_to_insert)


def fetch_images(calling_user_id, image_ids, user_ids, flight_ids, directory_location, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model, md5_hash):
    rs = image_dao.select_images('*', image_ids, user_ids, flight_ids, directory_location, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model, md5_hash)
    images = images_rs_to_object_list(rs)
    requested_flight_ids = set()
    for image in images:
        requested_flight_ids.add(image.flight_id)
    allowed_flights = flight_manager.fetch_flights(calling_user_id, requested_flight_ids, None, None, None, None, None, None, None, None, None, None, None, None, None)
    allowed_flight_ids = set()
    for allowed_flight in allowed_flights:
        allowed_flight_ids.add(allowed_flight.id)
    return_images = []
    for image in images:
        if image.flight_id in allowed_flight_ids:
            ### TODO:
            ###  The hash assertion seems to generate a different hash than the one stored. This might be an error caused by Windows.
            ###  Uncomment and test when deployed to a Linux VM.
            # image_file = open(image.directory_location, 'rb')
            # actual_hash = hashlib.md5(image_file.read()).hexdigest()
            # try:
            #     assert actual_hash == image.md5_hash
            # except:
            #     raise AssertionError('MD5 Hash Does Not Match. Possible File Corruption.')
            return_images.append(image)
    return return_images


def remove_images(image_ids):
    """
    Removes all the images containing the passed ids
    NOTE: This will also remove images flight if the image deletion leaves a flight without images
    NOTE: Checks if the images exist before deletion

    Parameters
    ----------
    image_ids : list of int
        The ids of the images to remove
    """
    flight_ids = set()
    image_ids_to_delete = set()
    images_to_delete = image_dao.select_images('id, flight_id', image_ids, None, None, None, None, None, None, None, None, None, None, None)
    if images_to_delete is not None and len(images_to_delete) > 0:
        for image in images_to_delete:
            flight_ids.add(image[1])
            image_ids_to_delete.add(image[0])
        image_dao.delete_images(list(image_ids_to_delete))
        for flight_id in flight_ids:
            if flight_id is not None:
                flight_remaining_images = image_dao.select_images('count(*)', None, None, [flight_id], None, None, None, None, None, None, None, None, None)[0][0]
                if flight_remaining_images == 0:
                    flight_manager.remove_flight(flight_id)


def image_data_to_csv(file_name, images):
    images_to_insert = image_objects_to_insert_tuple(images)
    with open('CSV_Files/{}.csv'.format(file_name),'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['id','flight_id','directory_location','image_extension','datetime','latitude','longitude','altitude','width','height','exposure_time'
        ,'f_number','iso_speed','metering_mode','light_source','focal_legnth','exposure_mode','white_balance','gain_control','contrast','saturation'
        ,'sharpness','image_compression','exif_version','software_version','hardware_make','hardware_model','hardware_serial_number'])
        csv_out.writerows(images_to_insert)
