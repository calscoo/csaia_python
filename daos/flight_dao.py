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
