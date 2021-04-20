from pypika import Table, Query

from daos.tools import dao_tools

insert_shared_flights_query = """ 
INSERT INTO shared_flights(user_id, flight_id) 
VALUES (%s, %s)"""

def insert_shared_flights(shared_flights_records):
    return dao_tools.execute(insert_shared_flights_query, shared_flights_records)

def select_shared_flight_user_ids(flight_id):
    shared_flights = Table('shared_flights')
    shared_flights_users_query = Query.from_(shared_flights).select('user_id').where(shared_flights.flight_id.isin([flight_id]))
    return dao_tools.execute(shared_flights_users_query)

def select_users_shared_flight_ids(user_id):
    shared_flights = Table('shared_flights')
    shared_flights_flight_query = Query.from_(shared_flights).select('flight_id').where(shared_flights.user_id.isin([user_id]))
    return dao_tools.execute(shared_flights_flight_query)