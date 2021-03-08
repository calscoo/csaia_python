from pypika import Query, Table
from daos.tools import dao_tools

insert_flights_query = """
INSERT INTO flights(
user_id, flight_name, manual_notes, address, field_name, 
crop_name, average_latitude, average_longitude, average_altitude, flight_start_time, 
flight_end_time, hardware_make, hardware_model)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def insert_flights(flight_records):
    return dao_tools.execute(insert_flights_query, flight_records)


def select_flights(select_columns, flight_ids, user_ids, flight_name, manual_notes, address, field_name, crop_name, start_datetime_range, end_datetime_range, latitude_range, longitude_range, altitude_range, make, model):
    """
    General purpose flight selection method built to cover a broad demand of queries.
    Every parameter can be None and list values can accept any number of elements including 0.
    This was built to flesh out flight selections in the manager without having to write complex queries.

    Parameters
    ----------
    select_columns : string or None
        The optional comma delimited string of columns to select on
        NOTE: if this value is None, all (*) columns will be selected
    flight_ids : list[int]
        The optional list of flight ids
    user_ids : list[int]
        The optional list of user ids
    flight_name : str
        The optional flight_name
        NOTE: Uses a LIKE comparision, full flight_name is not necessary, case IN-sensitive
    manual_notes : str
        The optional manual_notes
        NOTE: Uses a LIKE comparision, full manual_notes is not necessary, case IN-sensitive
    address : str
        The optional address
        NOTE: Uses a LIKE comparision, full address is not necessary, case IN-sensitive
    field_name : str
        The optional field_name
        NOTE: Uses a LIKE comparision, full field_name is not necessary, case IN-sensitive
    crop_name : str
        The optional crop_name
        NOTE: Uses a LIKE comparision, full crop_name is not necessary, case IN-sensitive
    start_datetime_range : objects.range
        The optional range of datetimes for the start of the flight
    end_datetime_range : objects.range
        The optional range of datetimes for the end of the flight
    latitude_range : objects.range
        The optional range of latitudes
    longitude_range : objects.range
        The optional range of longitudes
    altitude_range : objects.range
        The optional range of altitudes
    make : str
        The optional hardware make
        NOTE: Uses a LIKE comparision, full hardware make is not necessary, case IN-sensitive
    model : str
        The optional hardware model
        NOTE: Uses a LIKE comparision, full hardware model is not necessary, case IN-sensitive

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    flights = Table('flights')
    select_flights_query = Query.from_(flights).select('*' if select_columns is None else select_columns)
    if flight_ids is not None and len(flight_ids) > 0:
        select_flights_query = select_flights_query.where(flights.id.isin(flight_ids))
    if user_ids is not None and len(user_ids) > 0:
        select_flights_query = select_flights_query.where(flights.user_id.isin(user_ids))
    if flight_name is not None:
        select_flights_query = select_flights_query.where(flights.flight_name.like('%' + flight_name + '%'))
    if manual_notes is not None:
        select_flights_query = select_flights_query.where(flights.manual_notes.like('%' + manual_notes + '%'))
    if address is not None:
        select_flights_query = select_flights_query.where(flights.address.like('%' + address + '%'))
    if field_name is not None:
        select_flights_query = select_flights_query.where(flights.field_name.like('%' + field_name + '%'))
    if crop_name is not None:
        select_flights_query = select_flights_query.where(flights.crop_name.like('%' + crop_name + '%'))
    if start_datetime_range is not None:
        select_flights_query = select_flights_query.where(flights.flight_start_time >= start_datetime_range.begin).where(flights.flight_start_time <= start_datetime_range.end)
    if end_datetime_range is not None:
        select_flights_query = select_flights_query.where(flights.flight_end_time >= end_datetime_range.begin).where(flights.flight_end_time <= end_datetime_range.end)
    if latitude_range is not None:
        select_flights_query = select_flights_query.where(flights.average_latitude >= latitude_range.begin).where(flights.average_latitude <= latitude_range.end)
    if longitude_range is not None:
        select_flights_query = select_flights_query.where(flights.average_longitude >= longitude_range.begin).where(flights.average_longitude <= longitude_range.end)
    if altitude_range is not None:
        select_flights_query = select_flights_query.where(flights.average_altitude >= altitude_range.begin).where(flights.average_altitude <= altitude_range.end)
    if make is not None:
        select_flights_query = select_flights_query.where(flights.hardware_make.like('%' + make + '%'))
    if model is not None:
        select_flights_query = select_flights_query.where(flights.hardware_model.like('%' + model + '%'))
    return dao_tools.execute(select_flights_query.get_sql(quote_char=None))


def select_all_flights(select_columns):
    """
    Delegates to flight_dao.select_flights
    Used for selecting on all flights without restrictions

    Parameters
    ----------
    select_columns : string or None
        The optional comma delimited string of columns to select on
        NOTE: if this value is None, all (*) columns will be selected

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    return select_flights(select_columns, None, None, None, None, None, None, None, None, None, None, None, None, None, None)


def delete_flight(flight_id):
    if flight_id is not None:
        flights = Table('flights')
        delete_flight_query = Query.from_(flights).delete().where(flights.id.isin([flight_id]))
        dao_tools.execute(delete_flight_query.get_sql(quote_char=None))
