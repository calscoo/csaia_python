import csv
from geopy.geocoders import Nominatim
from daos import flight_dao
from managers import image_manager, shared_flight_manager
from objects.flight import flight
from objects.flight_derived_metadata import flight_derived_metadata
from enums.privacy import privacy as privacy_enum


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
    times.sort()
    if times.__len__() > 0:
        start_time = times[0]
        end_time = times[-1]
    return flight_derived_metadata(average_latitude, average_longitude, average_altitude, start_time, end_time, make, model)


def flights_rs_to_object_list(rs):
    flights = []
    if rs is not None:
        for tuple in rs:
            if tuple is not None:
                flights.append(flight(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7], tuple[8], tuple[9], tuple[10], tuple[11], tuple[12], tuple[13], privacy_enum(tuple[14])))
    return flights


def build_flight(path, flight_name, manual_notes, field_name, crop_name, privacy, shared_users):
    images = image_manager.parse_image_metadata(path)
    flight_metadata = calculate_derived_flight_metadata(images)
    user_id = None
    address = flight_address(flight_metadata.average_latitude, flight_metadata.average_longitude)
    flight_records = [(user_id, flight_name, manual_notes, address, field_name,
        crop_name, flight_metadata.average_latitude, flight_metadata.average_longitude, flight_metadata.average_altitude,
        flight_metadata.flight_start_time, flight_metadata.flight_end_time, flight_metadata.hardware_make,
        flight_metadata.hardware_model, privacy.value)]

    flight_id = flight_dao.insert_flights(flight_records)[0]

    if privacy == privacy_enum.Shared:
        shared_flight_manager.share_flight(flight_id, shared_users)

    for image in images:
        image.flight_id = flight_id
    ids = image_manager.upload_images(images)
    # return {
    #     'flight-id': flight_id,
    #     'user-id': user_id,
    #     'flight-name': flight_name,
    #     'manual-notes': manual_notes,
    #     'address': address,
    #     'field-name': field_name,
    #     'crop-name': crop_name,
    #     'average-latitude': flight_metadata.average_latitude,
    #     'average-longitude': flight_metadata.average_longitude,
    #     'average-altitude': flight_metadata.average_altitude,
    #     'start-time': flight_metadata.flight_start_time,
    #     'end-time': flight_metadata.flight_end_time,
    #     'make': flight_metadata.hardware_make,
    #     'model': flight_metadata.hardware_model,
    #     'image_ids': ids
    # }


def fetch_flights(calling_user_id, flight_ids, user_ids, flight_name, manual_notes, address, field_name, crop_name, start_datetime_range, end_datetime_range, latitude_range, longitude_range, altitude_range, make, model):
    rs = flight_dao.select_flights('*', flight_ids, user_ids, flight_name, manual_notes, address, field_name, crop_name, start_datetime_range, end_datetime_range, latitude_range, longitude_range, altitude_range, make, model)
    flights = flights_rs_to_object_list(rs)
    for flight in flights:
        if flight.privacy == privacy_enum.Private and flight.user_id != calling_user_id:
            flights.remove(flight)
        elif flight.privacy == privacy_enum.Shared:
            shared_users = shared_flight_manager.fetch_shared_flight_users(flight.id)
            if calling_user_id not in shared_users:
                flights.remove(flight)
    return flights


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
    flight_to_delete = flight_dao.select_flights('id', [flight_id], None, None, None, None, None, None, None, None, None, None, None, None, None)
    flight_id_to_delete = None if len(flight_to_delete) == 0 else flight_to_delete[0][0]
    flight_dao.delete_flight(flight_id_to_delete)

def flight_data_to_tuple(flight):
    tuple_flights = []
    for f in flight:
        tuple_flights.append((f.id, f.user_id, f.flight_name, f.manual_notes, f.address, f.field_name, f.crop_name, str(f.average_latitude), str(f.average_longitude), str(f.average_altitude), str(f.flight_start_time), str(f.flight_end_time), f.hardware_make, f.hardware_model, str(f.privacy)))
    return tuple_flights

def flight_data_to_csv(file_name, flight_id):
    flights = fetch_flights(flight_id, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    flight_to_insert = flight_data_to_tuple(flights)
    with open('CSV_Files/{}.csv'.format(file_name),'w', newline='') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['flight_id','user_id','flight_name','manual_notes','address','field_name','crop_name','average_latitude','average_longitude','average_altitude','start_time'
        ,'end_time','hardware_make','hardware_model','privacy'])
        csv_out.writerow(flight_to_insert)

def flight_address(latitude, longitude):
    address_coordinates = "{}, {}".format(latitude, longitude)
    geolocator = Nominatim(user_agent = "CSAIA")
    location = geolocator.reverse(address_coordinates)
    return location.address