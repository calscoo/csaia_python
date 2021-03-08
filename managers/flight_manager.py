from daos import flight_dao
from managers import image_manager
from objects.flight_metadata import flight_metadata


def calculate_flight_metadata(images):
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
    flight_metadata : objects.flight_metadata
        object containing the metadata for a flight
    """
    lat_count, lat_total, lon_count, lon_total, alt_count, alt_total = 0, 0, 0, 0, 0, 0
    times = []
    make, model = None, None
    for image in images:
        make = image.hardware_make if image.hardware_make is not None else make
        model = image.hardware_model if image.hardware_model is not None else model
        times.append(image.datetime)
        lat = float(image.latitude)
        if lat is not None:
            lat_count = lat_count + 1
            lat_total = lat_total + lat
        lon = float(image.longitude)
        if lon is not None:
            lon_count = lon_count + 1
            lon_total = lon_total + lon
        alt = float(image.altitude)
        if alt is not None:
            alt_count = alt_count + 1
            alt_total = alt_total + alt
    average_latitude = lat_total / lat_count
    average_longitude = lon_total / lon_count
    average_altitude = alt_total / alt_count
    times.sort()
    start_time = times[0]
    end_time = times[-1]
    return flight_metadata(average_latitude, average_longitude, average_altitude, start_time, end_time, make, model)


def build_flight(path, flight, notes, field, crop):
    images = image_manager.parse_image_metadata(path)
    flight_metadata = calculate_flight_metadata(images)
    user_id = None
    flight_name = flight  # input("File name: ")
    manual_notes = notes  # input("Notes: ")
    address = 'Test'  # Using google maps for this field
    field_name = field  # input("Field: ")
    crop_name = crop  # input("Crop: ")
    '''
    print(type(user_id), type(flight_name), type(manual_notes), type(address), type(field_name), type(crop_name),
          type(average_latitude), type(average_longitude), type(average_altitude), type(flight_start_time), type(flight_end_time),
          type(hardware_make), type(hardware_model))
    '''
    flight_records = [(user_id, flight_name, manual_notes, address, field_name,
        crop_name, flight_metadata.average_latitude, flight_metadata.average_longitude, flight_metadata.average_altitude,
        flight_metadata.flight_start_time, flight_metadata.flight_end_time, flight_metadata.hardware_make,
        flight_metadata.hardware_model)]

    flight_id = flight_dao.insert_flights(flight_records)[0]
    for image in images:
        image.flight_id = flight_id
    ids = image_manager.upload_images(images)
    return {
        'flight-id' : flight_id,
        'user-id' : user_id,
        'flight-name' : flight_name,
        'manual-notes' : manual_notes,
        'address' : address,
        'field-name' : field_name,
        'crop-name' : crop_name,
        'average-latitude' : flight_metadata.average_latitude,
        'average-longitude' : flight_metadata.average_longitude,
        'average-altitude' : flight_metadata.average_altitude,
        'start-time' : flight_metadata.flight_start_time,
        'end-time' : flight_metadata.flight_end_time,
        'make' : flight_metadata.hardware_make,
        'model' : flight_metadata.hardware_model,
        'image_ids' : ids
    }


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
