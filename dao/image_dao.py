from mysql.connector import connect, Error

insert_images_query = """
INSERT INTO images(
flight_id, directory_location, image_extension, datetime, latitude, 
longitude, altitude, image_width, image_height, exposure_time, 
f_number, iso_speed, metering_mode, focal_length, light_source, 
exposure_mode, white_balance, gain_control, contrast, saturation, 
sharpness, image_compression, exif_version, software_version, 
hardware_make, hardware_model, hardware_serial_number)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

insert_flights_query = """
INSERT INTO flights(
user_id, flight_name, manual_notes, address, field_name, 
crop_name, average_latitude, average_longitude, average_altitude, flight_start_time, 
flight_end_time, hardware_make, hardware_model)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def execute(query, *args):
    standard_execution = True if args[0] is None else False
    try:
        with connect(
                host="localhost",
                user="root",
                password="Password1234",
                database="csaia_database",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query) if standard_execution else cursor.executemany(query, args[0])
            connection.commit()
    except Error as e:
        print(e)


def insert_images(image_records):
    execute(insert_images_query, image_records)


def insert_flights(flight_records):
    execute(insert_flights_query, flight_records)
