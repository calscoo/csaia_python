from pypika import Query, Table
from daos.tools import dao_tools
from daos import image_dao, flight_dao

from objects.flight_derived_metadata import flight_derived_metadata


def calculate_derived_flight_metadata(images):
    lat_count, lat_total, lon_count, lon_total, alt_count, alt_total = 0, 0, 0, 0, 0, 0
    times = []
    make, model = None, None
    for image in images:
        make = image[26] if image[26] is not None else make
        model = image[27] if image[27] is not None else model
        time = image[5]
        if time is not None:
            times.append(time)
        lat = image[6]
        if lat is not None:
            lat = float(lat)
            lat_count = lat_count + 1
            lat_total = lat_total + lat
        lon = image[7]
        if lon is not None:
            lon = float(lon)
            lon_count = lon_count + 1
            lon_total = lon_total + lon
        alt = image[8]
        if alt is not None:
            alt = float(alt)
            alt_count = alt_count + 1
            alt_total = alt_total + alt
    average_latitude = None if lat_count == 0 else lat_total / lat_count
    average_longitude = None if lon_count == 0 else lon_total / lon_count
    average_altitude = None if alt_count == 0 else alt_total / alt_count
    times.sort()
    start_time = None if len(times) == 0 else times[0]
    end_time = None if len(times) == 0 else times[-1]
    return flight_derived_metadata(average_latitude, average_longitude, average_altitude, start_time, end_time, make, model)


def trim_name(name):
    parts = name.split('/')[-4:]
    trimmed_name = ''
    for part in parts:
        trimmed_name = trimmed_name + '/' + part
    return trimmed_name[1:][:-1]


def update_flight(flight_derived_md, flight_id, flight_name):
    flights = Table('flights')
    update_flight_query = Query.update(flights)
    if flight_derived_md.average_latitude is not None:
        update_flight_query = update_flight_query.set(flights.average_latitude, flight_derived_md.average_latitude)
    if flight_derived_md.average_longitude is not None:
        update_flight_query = update_flight_query.set(flights.average_longitude, flight_derived_md.average_longitude)
    if flight_derived_md.average_altitude is not None:
        update_flight_query = update_flight_query.set(flights.average_altitude, flight_derived_md.average_altitude)
    if flight_derived_md.flight_start_time is not None:
        update_flight_query = update_flight_query.set(flights.flight_start_time, flight_derived_md.flight_start_time)
    if flight_derived_md.flight_end_time is not None:
        update_flight_query = update_flight_query.set(flights.flight_end_time, flight_derived_md.flight_end_time)
    if flight_derived_md.hardware_make is not None:
        update_flight_query = update_flight_query.set(flights.hardware_make, flight_derived_md.hardware_make)
    if flight_derived_md.hardware_model is not None:
        update_flight_query = update_flight_query.set(flights.hardware_model, flight_derived_md.hardware_model)
    return dao_tools.execute(update_flight_query.set(flights.flight_name, trim_name(flight_name)).where(flights.id.isin([flight_id])))


flight_info = flight_dao.select_all_flights('id, flight_name')
for flight in flight_info:
    flight_id = flight[0]
    flight_name = flight[1]
    flights_images = image_dao.select_images('*', None, None, [flight_id], None, None, None, None, None, None, None)
    flight_derived_md = calculate_derived_flight_metadata(flights_images)
    update_flight(flight_derived_md, flight_id, flight_name)
