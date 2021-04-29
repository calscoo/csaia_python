from pypika import Table, Query

from daos.tools import dao_tools

insert_shared_flights_query = """ 
INSERT INTO shared_flights(user_id, flight_id) 
VALUES (%s, %s)"""


def insert_shared_flights(shared_flights_records):
    return dao_tools.execute(insert_shared_flights_query, shared_flights_records)


def select_shared_flight_user_ids(flight_id):
    """
    Selects shared flights based on the passed flight id

    Parameters
    ----------
    flight_id : integer

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    shared_flights = Table('shared_flights')
    shared_flights_users_query = Query.from_(shared_flights).select('user_id').where(shared_flights.flight_id.isin(0 if flight_id is None else [flight_id]))
    return dao_tools.execute(shared_flights_users_query)


def select_users_shared_flight_ids(user_id):
    """
    Selects flight ids based on the passed user id

    Parameters
    ----------
    user_id : integer

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    shared_flights = Table('shared_flights')
    shared_flights_flight_query = Query.from_(shared_flights).select('flight_id').where(shared_flights.user_id.isin(0 if user_id is None else [user_id]))
    return dao_tools.execute(shared_flights_flight_query)


def delete_shared_flight(flight_id):
    """
    Deletes all shared_flights containing the passed flight_id

    Parameters
    ----------
    flight_id : integer
    """
    if flight_id is not None:
        shared_flights = Table('shared_flights')
        delete_shared_flight_query = Query.from_(shared_flights).delete().where(shared_flights.flight_id.isin([flight_id]))
        dao_tools.execute(delete_shared_flight_query)
