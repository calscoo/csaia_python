class flight_derived_metadata:

    def __init__(self, average_latitude, average_longitude, average_altitude, flight_start_time, flight_end_time, hardware_make, hardware_model):
        self._set_average_latitude(average_latitude)
        self._set_average_longitude(average_longitude)
        self._set_average_altitude(average_altitude)
        self._set_flight_start_time(flight_start_time)
        self._set_flight_end_time(flight_end_time)
        self._set_hardware_make(hardware_make)
        self._set_hardware_model(hardware_model)

    def _set_average_latitude(self, average_latitude):
        self.average_latitude = average_latitude

    def _get_average_latitude(self):
        return self.average_latitude

    def _set_average_longitude(self, average_longitude):
        self.average_longitude = average_longitude

    def _get_average_longitude(self):
        return self.average_longitude

    def _set_average_altitude(self, average_altitude):
        self.average_altitude = average_altitude

    def _get_average_altitude(self):
        return self.average_altitude

    def _set_flight_start_time(self, flight_start_time):
        self.flight_start_time = flight_start_time

    def _get_flight_start_time(self):
        return self.flight_start_time

    def _set_flight_end_time(self, flight_end_time):
        self.flight_end_time = flight_end_time

    def _get_flight_end_time(self):
        return self.flight_end_time

    def _set_hardware_make(self, hardware_make):
        self.hardware_make = hardware_make

    def _get_hardware_make(self):
        return self.hardware_make

    def _set_hardware_model(self, hardware_model):
        self.hardware_model = hardware_model

    def _get_hardware_model(self):
        return self.hardware_model

    def __str__(self):
        return \
            "flight_partial_metadata: { average_latitude: " + str(self.average_latitude) + ", " + \
            "average_longitude: " + str(self.average_longitude) + ", " + \
            "average_altitude: " + str(self.average_altitude) + ", " + \
            "flight_start_time: " + str(self.flight_start_time) + ", " + \
            "flight_end_time: " + str(self.flight_end_time) + ", " + \
            "hardware_make: " + str(self.hardware_make) + ", " + \
            "hardware_model: " + str(self.hardware_model) + " }"
