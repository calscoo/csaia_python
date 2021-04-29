from daos import shared_flight_dao


def share_flight(flight_id, user_ids):
    """
    Makes a shared flight with a flight id and 
    one or more user ids

    Parameters
    ----------
    flight_id : integer
        The id of the flight
    user_ids : list[int]
        The ids of the users
    """
    tuple_shared_flights = []
    for user_id in user_ids:
        tuple_shared_flights.append((user_id, flight_id))
    shared_flight_dao.insert_shared_flights(tuple_shared_flights)


def fetch_shared_flight_user_ids(flight_id):
    """
    Grabs all the user ids based on the flight_id

    Parameters
    ----------
    flight_id : integer
        The id of the flight

    Returns
    -------
    user_ids : integer
        the id's of all the users that share that flight    
    """
    rs = shared_flight_dao.select_shared_flight_user_ids(flight_id)
    user_ids = []
    for tuple in rs:
        if tuple is not None:
            user_ids.append(tuple[0])
    return user_ids


def fetch_users_shared_flight_ids(user_id):
    """
    Grabs all the flight ids based on the user_id

    Parameters
    ----------
    user_id : integer
        The id of the user

    Returns
    -------
    flight_ids : integer
        the id's of all the flights that the user has access to    
    """
    rs = shared_flight_dao.select_users_shared_flight_ids(user_id)
    flight_ids = []
    for tuple in rs:
        if tuple is not None:
            flight_ids.append(tuple[0])
    return flight_ids