class flight:
    def __init__(self, id, user_id, flight_name, manual_notes, address, field_name, crop_name, average_latitude,
                 average_longitude, average_altitude, flight_start_time, flight_end_time, hardware_make,
                 hardware_model):
        self.id = id
        self.user_id = user_id
        self.flight_name = flight_name
        self.manual_notes = manual_notes
        self.address = address
        self.field_name = field_name
        self.crop_name = crop_name
        self.average_latitude = average_latitude
        self.average_longitude = average_longitude
        self.average_altitude = average_altitude
        self.flight_start_time = flight_start_time
        self.flight_end_time = flight_end_time
        self.hardware_make = hardware_make
        self.hardware_model = hardware_model

    def _get_id(self):
        return self.id

    def _set_id(self, id):
        self.id = id

    def _get_user_id(self):
        return self.user_id

    def _set_user_id(self, user_id):
        self.user_id = user_id

    def _get_flight_name(self):
        return self.flight_name

    def _set_flight_name(self, flight_name):
        self.flight_name = flight_name

    def _get_manual_notes(self):
        return self.manual_notes

    def _set_manual_notes(self, manual_notes):
        self.manual_notes = manual_notes

    def _get_address(self):
        return self.address

    def _set_address(self, address):
        self.address = address

    def _get_field_name(self):
        return self.field_name

    def _set_field_name(self, field_name):
        self.field_name = field_name

    def _get_crop_name(self):
        return self.crop_name

    def _set_crop_name(self, crop_name):
        self.crop_name = crop_name

    def _get_average_latitude(self):
        return self.average_latitude

    def _set_average_latitude(self, average_latitude):
        self.average_latitude = average_latitude

    def _get_average_longitude(self):
        return self.average_longitude

    def _set_average_longitude(self, average_longitude):
        self.average_longitude = average_longitude

    def _get_average_altitude(self):
        return self.average_altitude

    def _set_average_altitude(self, average_altitude):
        self.average_altitude = average_altitude

    def _get_flight_start_time(self):
        return self.flight_start_time

    def _set_flight_start_time(self, flight_start_time):
        self.flight_start_time = flight_start_time

    def _get_flight_end_time(self):
        return self.flight_end_time

    def _set_flight_end_time(self, flight_end_time):
        self.flight_end_time = flight_end_time

    def _get_hardware_make(self):
        return self.hardware_make

    def _set_hardware_make(self, hardware_make):
        self.hardware_make = hardware_make

    def _get_hardware_model(self):
        return self.hardware_model

    def _set_hardware_model(self, hardware_model):
        self.hardware_model = hardware_model

    def __str__(self):
        return \
            "flight: { id: " + str(self.id) + ", " + \
            "user_id: " + str(self.user_id) + ", " + \
            "flight_name: " + str(self.flight_name) + ", " + \
            "manual_notes: " + str(self.manual_notes) + ", " + \
            "address: " + str(self.address) + ", " + \
            "field_name: " + str(self.field_name) + ", " + \
            "crop_name: " + str(self.crop_name) + ", " + \
            "average_latitude: " + str(self.average_latitude) + ", " + \
            "average_longitude: " + str(self.average_longitude) + ", " + \
            "average_altitude: " + str(self.average_altitude) + ", " + \
            "flight_start_time: " + str(self.flight_start_time) + ", " + \
            "flight_end_time: " + str(self.flight_end_time) + ", " + \
            "hardware_make: " + str(self.hardware_make) + ", " + \
            "hardware_model: " + str(self.hardware_model) + " }"
