

#Update Admin method still a work in progress
from daos import shared_flight_dao
from managers import users_manager


def share_flight(flight_id, user_ids):
    valid_users = users_manager.fetch_users(user_ids, None, None, None)
    tuple_shared_flights = []
    for user in valid_users:
        tuple_shared_flights.append((user.id, flight_id))
    shared_flight_dao.insert_shared_flights(tuple_shared_flights)


def fetch_shared_flight_user_ids(flight_id):
    rs = shared_flight_dao.select_shared_flight_user_ids(flight_id)
    user_ids = []
    for tuple in rs:
        if tuple is not None:
            user_ids.append(tuple[0])
    return user_ids


def fetch_users_shared_flight_ids(user_id):
    rs = shared_flight_dao.select_users_shared_flight_ids(user_id)
    flight_ids = []
    for tuple in rs:
        if tuple is not None:
            flight_ids.append(tuple[0])
    return flight_ids