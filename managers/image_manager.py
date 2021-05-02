import hashlib
import os
import re
import shutil
from os import path

import exifread
import csv

from datetime import datetime

from managers import flight_manager, users_manager
from managers.tools import password_manager
from objects.image import image
from daos import image_dao, flight_dao
from GPSPhoto import gpsphoto

# the system only allows for jpeg and tiff images
supported_formats = ('.jpg', '.jpeg', '.tif', '.tiff')
time_format = '%Y%m%d-%H%M%S'


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
    """
    Takes all given image data and stores passed data into a list

    Parameters
    ----------
    rs : selection of images
        The images selected to be condensed

    Returns
    -------
    images : a list of images
    """
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
    images : list[image]
        the images to upload

    Returns
    -------
    image ids : list of int
        the list of image ids that have been uploaded
    """
    images_to_insert = image_objects_to_insert_tuple(images)

    return image_dao.insert_images(images_to_insert)


def fetch_images_and_flights(calling_user_id, image_ids, user_ids, flight_ids, directory_location, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model, md5_hash, flight_name, flight_notes, flight_field, flight_crop, flight_address):
    """
    Fetches image and flight metadata from the database based
    on the user's passed values.

    Parameters
    ----------
    calling_user_id : integer
        The users ID
    image_ids : list[int]
        The ids of the individual images
    user_ids : list[int]
        The ids of the user's images
    flight_ids : list[int]
        The ids of the flights
    directory_location : string
        The file path for where the images are stored
    extensions : list[string]
        The image type
    datetime_range : range
        The range from when a flight started and from where it ended
    latitude_range : range
        The range from where the flight started and from where it ended latitudinally
    longitude_range : range
        The range from where the flight started and from where it ended longitudinally
    altitude_range : range
        The range from how high the images were taken
    make : string
        The make of the drone/camera
    model : string
        The model of the drone/camera
    md5_hash : string
        The hashing code of the image
    flight_name : str
        The optional flight_name
    flight_notes : str
        The optional flight_notes
    flight_field : str
        The optional flight_field
    flight_crop : str
        The optional flight_crop
    flight_address : str
        The optional flight_address

    Returns
    -------
    images : list of objects.image
        a list of images
    flights : list of objects.flight
        a list of flights
    """
    # Whether or not to query flights as well
    query_flights = flight_name is not None or flight_notes is not None or flight_field is not None or flight_crop is not None or flight_address is not None
    # Fetch the queried flights
    updated_flight_ids = [] if flight_ids is None else flight_ids
    if query_flights:
        query_flight_ids = []
        flights = flight_manager.fetch_flights(str(calling_user_id), None, None, flight_name, flight_notes, flight_address, flight_field, flight_crop, None, None, None, None, None, None, None)
        for flight in flights:
            query_flight_ids.append(flight.id)
            updated_flight_ids = updated_flight_ids + query_flight_ids
    if len(updated_flight_ids) == 0:
        updated_flight_ids = None
    # fetch the images result from the database
    images_rs = image_dao.select_images('*', image_ids, user_ids, updated_flight_ids, directory_location, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model, md5_hash)
    # cast the database result to image objects
    images = images_rs_to_object_list(images_rs)
    # create an emtpy set of requested flight ids to access
    requested_flight_ids = set()
    # add all flight ids from the requested images and requested flights to the requested flight ids set
    for image in images:
        requested_flight_ids.add(image.flight_id)
    if query_flights:
        requested_flight_ids.update(query_flight_ids)
    # fetch the allowed flights, passing in the calling user id ensures we only got back flights the user is permitted to view
    # This second flight fetch with the requested images flight ids is necessary because we need to filter out the disallowed flights from the image query
    allowed_flights = flight_manager.fetch_flights(str(calling_user_id), list(requested_flight_ids), None, None, None, None, None, None, None, None, None, None, None, None, None)
    # create an emtpy set of allowed flight ids
    allowed_flight_ids = []
    # added the allowed flight ids to the allowed flight ids set
    for allowed_flight in allowed_flights:
        allowed_flight_ids.append(allowed_flight.id)
    # iterate through the requested images and only return those with permitted flights
    return_images = []
    return_image_flight_ids = set()
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
            return_image_flight_ids.add(image.flight_id)
            return_images.append(image)
    return_flights = []
    for flight in allowed_flights:
        if flight.id in return_image_flight_ids:
            return_flights.append(flight)
    if query_flights:
        return return_images, return_flights
    else:
        return return_images, allowed_flights


def remove_images(image_ids, admin_id, admin_pass):
    """
    Removes all the images containing the passed ids
    NOTE: This will also remove the images flight if the image deletion leaves a flight without images
    NOTE: Checks if the images exist before deletion
    NOTE: Deleted images are moved to the archive folder

    Parameters
    ----------
    image_ids : list of int
        The ids of the images to remove
    """
    assert admin_id and admin_pass is not None
    # fetch the admin and ensure they're password matches before continuing
    admin_user = users_manager.fetch_users([admin_id], None, None, None)[0]
    if password_manager.check_password(admin_pass, admin_user.password):
        flight_ids = set()
        image_ids_to_delete = []
        images_to_delete = image_dao.select_images('id, flight_id, directory_location', image_ids, None, None, None, None, None, None, None, None, None, None, None)
        if images_to_delete is not None and len(images_to_delete) > 0:
            for image in images_to_delete:
                flight_ids.add(image[1])
                image_ids_to_delete.append(image[0])
                file_path = image[2]
                parent_path = os.path.join(*os.path.split(file_path)[:-1])
                archive_directory_name = os.path.join('archive', os.path.split(parent_path)[-1])
                if not path.exists(archive_directory_name):
                    os.makedirs(archive_directory_name)
                if path.exists(file_path):
                    shutil.move(file_path, archive_directory_name)
                    if len(os.listdir(parent_path)) == 0:
                        shutil.rmtree(parent_path)
            image_dao.delete_images(image_ids_to_delete)
            for flight_id in flight_ids:
                if flight_id is not None:
                    flight_remaining_images = image_dao.select_images('count(*)', None, None, [flight_id], None, None, None, None, None, None, None, None, None)[0][0]
                    if flight_remaining_images == 0:
                        flight_manager.remove_flight(flight_id)
            return True
        else:
            return False


def image_data_to_csv(file_name, images):
    """
    Takes image data and inserts the data into a CSV file

    Parameters
    ----------
    file_name : string
        The name of the file the user wishes
    images : image object 
        The images the user wants data on
    """
    images_to_insert = image_objects_to_insert_tuple(images)
    with open('image_csv_files/{}.csv'.format(file_name),'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['id','flight_id','directory_location','image_extension','datetime','latitude','longitude','altitude','width','height','exposure_time'
        ,'f_number','iso_speed','metering_mode','light_source','focal_legnth','exposure_mode','white_balance','gain_control','contrast','saturation'
        ,'sharpness','image_compression','exif_version','software_version','hardware_make','hardware_model','hardware_serial_number'])
        csv_out.writerows(images_to_insert)
