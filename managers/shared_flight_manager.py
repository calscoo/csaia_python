

#Update Admin method still a work in progress
from daos import shared_flight_dao


def share_flight(flight_id, user_ids):
    # TODO: Fetch user ids and only share the flight if the users exist
    tuple_shared_flights = []
    for user_id in user_ids:
        tuple_shared_flights.append((user_id, flight_id))
    shared_flight_dao.insert_shared_flights(tuple_shared_flights)


def fetch_shared_flight_users(flight_id):
    rs = shared_flight_dao.select_shared_flight_users(flight_id)
    user_ids = []
    for tuple in rs:
        if tuple is not None:
            user_ids.append(tuple[0])
    return user_ids
