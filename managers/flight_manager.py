import csv

from geopy.geocoders import Nominatim
from daos import flight_dao, shared_flight_dao
from managers import image_manager, shared_flight_manager, users_manager
from objects.flight import flight
from objects.flight_derived_metadata import flight_derived_metadata
from enums.privacy import privacy as privacy_enum
import os.path as Path
import shutil


def calculate_derived_flight_metadata(images):
    """
    Calculates the necessary metadata for a flight, from a list of image objects
    Supports None latitude, longitude and altitude values.
    Supports None make and model values.

    Parameters
    ----------
    images : list of objects.image
        The list of images to calculate the flight metadata on

    Returns
    -------
    flight_metadata : objects.flight_derived_metadata
        object containing the metadata for a flight
    """
    lat_count, lat_total, lon_count, lon_total, alt_count, alt_total = 0, 0, 0, 0, 0, 0
    times = []
    start_time = None
    end_time = None
    make, model = None, None
    for image in images:
        make = image.hardware_make if image.hardware_make is not None else make
        model = image.hardware_model if image.hardware_model is not None else model
        datetime = image.datetime
        if datetime is not None:
            times.append(datetime)
        lat = image.latitude
        if lat is not None:
            lat = float(lat)
            lat_count = lat_count + 1
            lat_total = lat_total + lat
        lon = image.longitude
        if lon is not None:
            lon = float(lon)
            lon_count = lon_count + 1
            lon_total = lon_total + lon
        alt = image.altitude
        if alt is not None:
            alt = float(alt)
            alt_count = alt_count + 1
            alt_total = alt_total + alt
    average_latitude = None if lat_count == 0 else lat_total / lat_count
    average_longitude = None if lon_count == 0 else lon_total / lon_count
    average_altitude = None if alt_count == 0 else alt_total / alt_count
    average_latitude = None if average_latitude == 0 else average_latitude
    average_longitude = None if average_longitude == 0 else average_longitude
    average_altitude = None if average_altitude == 0 else average_altitude
    times.sort()
    if times.__len__() > 0:
        start_time = times[0]
        end_time = times[-1]
    return flight_derived_metadata(average_latitude, average_longitude, average_altitude, start_time, end_time, make,
                                   model)


def flights_rs_to_object_list(rs):
    """
    Takes all given flight data and stores passed data into a list

    Parameters
    ----------
    rs : selection of flights
        The flights selected to be condensed

    Returns
    -------
    flights: a list of flights
    """
    flights = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                flights.append(
                    flight(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7], tuple[8],
                           tuple[9], tuple[10], tuple[11], tuple[12], tuple[13], privacy_enum(tuple[14])))
    return flights


def build_flight(owner_id, path, flight_name, manual_notes, field_name, crop_name, privacy, shared_users):
    """
    Creates a flight given by the user and the scraped flight image data

    Parameters
    ----------
    owner_id : integer
        The user's id 
    path : string
        The location of the directory where the images are at
    flight_name : string
        The name of the flight
    manual_notes : string
        Any additional notes the user wishes to add
    field_name : string
        The name of the field where the data is taken from
    crop_name : string
        The name of the crop from where the data is taken from
    privacy : privacy
        The number code to determine what privacy setting the flight is
    shared_users : list[int]
        The ids of other users who can see this flight

    """
    # parse the image metadata into images objects
    images = image_manager.parse_image_metadata(path)
    if len(images) > 0:
        # parse the flight metadata into flight metadata objects
        flight_metadata = calculate_derived_flight_metadata(images)
        # calculate the common address
        address = flight_address(flight_metadata.average_latitude, flight_metadata.average_longitude)

        # remove the owner_id from the shared users and fetch the shared_users
        # if owner_id in shared_users:
        #     shared_users.remove(owner_id)
        # valid_shared_users = users_manager.fetch_users(shared_users, None, None, None)
        shareable_ids = users_manager.fetch_shareable_user_ids(owner_id, shared_users)
        if privacy == privacy_enum.Shared and len(shareable_ids) == 0:
            privacy = privacy_enum.Private

        # prepare the flight record for database insert
        flight_records = [(owner_id, flight_name, manual_notes, address, field_name,
                           crop_name, flight_metadata.average_latitude, flight_metadata.average_longitude,
                           flight_metadata.average_altitude,
                           flight_metadata.flight_start_time, flight_metadata.flight_end_time,
                           flight_metadata.hardware_make,
                           flight_metadata.hardware_model, privacy.value)]

        # insert the flight record into the database
        flight_id = flight_dao.insert_flights(flight_records)[0]

        # if the flight is shared, insert the shared records
        if privacy == privacy_enum.Shared:
            shared_flight_manager.share_flight(flight_id, shareable_ids)

        # set the flight and owner id on the image objects
        for image in images:
            image.flight_id = flight_id
            image.user_id = owner_id

        # insert the image objects into the database
        image_manager.upload_images(images)
        return True
    else:
        # No images to build flight from, delete the upload
        if Path.exists(path):
            shutil.rmtree(path)
        return False


def fetch_flights(calling_user_id, flight_ids, user_ids, flight_name, manual_notes, address, field_name, crop_name,
                  start_datetime_range, end_datetime_range, latitude_range, longitude_range, altitude_range, make,
                  model):
    """
    Fetches flights from the database based
    on the user's passed values.

    Parameters
    ----------
    calling_user_id : string or None
        User's own id
    flight_ids : list[int]
        The optional list of flight ids
    user_ids : list[int]
        The optional list of user ids
    flight_name : string
        The optional flight_name
        NOTE: Uses a LIKE comparision, full flight_name is not necessary, case IN-sensitive
    manual_notes : string
        The optional manual_notes
        NOTE: Uses a LIKE comparision, full manual_notes is not necessary, case IN-sensitive
    address : string
        The optional address
        NOTE: Uses a LIKE comparision, full address is not necessary, case IN-sensitive
    field_name : string
        The optional field_name
        NOTE: Uses a LIKE comparision, full field_name is not necessary, case IN-sensitive
    crop_name : string
        The optional crop_name
        NOTE: Uses a LIKE comparision, full crop_name is not necessary, case IN-sensitive
    start_datetime_range : range
        The optional range of datetimes for the start of the flight
    end_datetime_range : range
        The optional range of datetimes for the end of the flight
    latitude_range : range
        The optional range of latitudes
    longitude_range : range
        The optional range of longitudes
    altitude_range : range
        The optional range of altitudes
    make : string
        The optional hardware make
        NOTE: Uses a LIKE comparision, full hardware make is not necessary, case IN-sensitive
    model : string
        The optional hardware model
        NOTE: Uses a LIKE comparision, full hardware model is not necessary, case IN-sensitive

    Returns
    -------
    flights : set(flights)
        returns a set of flights
    """
    # fetch the flights result
    rs = flight_dao.select_flights('*', flight_ids, user_ids, flight_name, manual_notes, address, field_name, crop_name,
                                   start_datetime_range, end_datetime_range, latitude_range, longitude_range,
                                   altitude_range, make, model)
    # convert the database result to flight objects
    flights = flights_rs_to_object_list(rs)
    # create an empty set to add flights to remove to
    flights_to_remove = set()
    for flight in flights:
        # if the flight is private, and the calling user is not the owner, add the flight to the remove set
        if flight.privacy == privacy_enum.Private and flight.user_id != int(calling_user_id):
            flights_to_remove.add(flight)
        # if the flight is shared, and the calling user is not shared on the flight, add the flight to the remove set
        elif flight.privacy == privacy_enum.Shared and flight.user_id != int(calling_user_id):
            shared_user_ids = shared_flight_manager.fetch_shared_flight_user_ids(flight.id)
            if int(str(calling_user_id)) not in shared_user_ids:
                flights_to_remove.add(flight)
    # return the set of original flights without the disallowed flights.
    return set(flights).difference(flights_to_remove)


def remove_flight(flight_id):
    """
    Removes the flight matching the passed id
    NOTE: This will remove all of the flights images as well as the flight itself
    NOTE: Checks if the flight exists before deletion

    Parameters
    ----------
    flight_id : int
        The id of the flight to remove
    """
    flight_to_delete = flight_dao.select_flights('id', [flight_id], None, None, None, None, None, None, None, None,
                                                 None, None, None, None, None)
    flight_id_to_delete = None if len(flight_to_delete) == 0 else flight_to_delete[0][0]
    shared_flight_dao.delete_shared_flight(flight_id_to_delete)
    flight_dao.delete_flight(flight_id_to_delete)


def flight_data_to_tuple(flight):
    """
    Takes a single flight and condenses it into a tuple

    Parameters
    ----------
    flight : flight object
        A singular flight

    Returns
    -------
    tuple_flights: a flight tuple
        A flight organized into a tuple
    """
    tuple_flights = []
    for f in flight:
        tuple_flights.append((f.id, f.user_id, f.flight_name, f.manual_notes, f.address, f.field_name, f.crop_name,
                              str(f.average_latitude), str(f.average_longitude), str(f.average_altitude),
                              str(f.flight_start_time), str(f.flight_end_time), f.hardware_make, f.hardware_model,
                              str(f.privacy)))
    return tuple_flights


def flight_address(latitude, longitude):
    """
    Takes the latitude and longitude of a flight and
    returns the address of the specified coordinates

    Parameters
    ----------
    latitude : decimal
        The latitudinal coordinates of a flight (North to South)
    longitude : decimal
        The longitudinal coordinates of a flight (East to West)

    Returns
    -------
    address: string
        The exact location in a readable manner
    """
    address = None
    if latitude is not None and longitude is not None:
        address_coordinates = "{}, {}".format(latitude, longitude)
        geo_locator = Nominatim(user_agent="CSAIA")
        location = geo_locator.reverse(address_coordinates)
        address = location.address
    return address


def flight_data_to_csv(file_name, flights):
    """
    Takes a flight and orgainizes it into a CSV file

    Parameters
    ----------
    file_name : string
        The name of the file the user wishes
    flights : flight object
        The flights the user wants data on

    """
    flights_to_insert = flight_data_to_tuple(flights)
    with open('flight_csv_files/{}.csv'.format(file_name), 'w', newline='') as out:
        csv_out = csv.writer(out)
        csv_out.writerow([
            'id',
            'user_id',
            'flight_name',
            'manual_notes',
            'address',
            'field_name',
            'crop_name',
            'average_latitude',
            'average_longitude',
            'average_altitude',
            'flight_start_time',
            'flight_end_time',
            'hardware_make',
            'hardware_model',
            'privacy'])
        csv_out.writerows(flights_to_insert)
