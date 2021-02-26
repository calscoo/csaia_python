class image:
    def __init__(self, id, user_id, flight_id, directory_location, image_extension, datetime, latitude, longitude, altitude, image_width, image_height, exposure_time, f_number, iso_speed, metering_mode, light_source, focal_length, exposure_mode, white_balance, gain_control, contrast, saturation, sharpness, image_compression, exif_version, software_version, hardware_make, hardware_model, hardware_serial_number):
        self._set_id(id)
        self._set_user_id(user_id)
        self._set_flight_id(flight_id)
        self._set_directory_location(directory_location)
        self._set_image_extension(image_extension)
        self._set_datetime(datetime)
        self._set_latitude(latitude)
        self._set_longitude(longitude)
        self._set_altitude(altitude)
        self._set_image_width(image_width)
        self._set_image_height(image_height)
        self._set_exposure_time(exposure_time)
        self._set_f_number(f_number)
        self._set_iso_speed(iso_speed)
        self._set_metering_mode(metering_mode)
        self._set_focal_length(focal_length)
        self._set_light_source(light_source)
        self._set_exposure_mode(exposure_mode)
        self._set_white_balance(white_balance)
        self._set_gain_control(gain_control)
        self._set_contrast(contrast)
        self._set_saturation(saturation)
        self._set_sharpness(sharpness)
        self._set_image_compression(image_compression)
        self._set_exif_version(exif_version)
        self._set_software_version(software_version)
        self._set_hardware_make(hardware_make)
        self._set_hardware_model(hardware_model)
        self._set_hardware_serial_number(hardware_serial_number)

    def _get_id(self):
        return self.id

    def _set_id(self, id):
        self.id = id

    def _get_user_id(self):
        return self.user_id

    def _set_user_id(self, user_id):
        self.user_id = user_id

    def _get_flight_id(self):
        return self.flight_id

    def _set_flight_id(self, flight_id):
        self.flight_id = flight_id

    def _get_directory_location(self):
        return self.directory_location

    def _set_directory_location(self, directory_location):
        self.directory_location = directory_location

    def _get_image_extension(self):
        return self.image_extension

    def _set_image_extension(self, image_extension):
        self.image_extension = image_extension

    def _get_datetime(self):
        return self.datetime

    def _set_datetime(self, datetime):
        self.datetime = datetime

    def _get_latitude(self):
        return self.latitude

    def _set_latitude(self, latitude):
        self.latitude = latitude

    def _get_longitude(self):
        return self.longitude

    def _set_longitude(self, longitude):
        self.longitude = longitude

    def _get_altitude(self):
        return self.altitude

    def _set_altitude(self, altitude):
        self.altitude = altitude

    def _get_image_width(self):
        return self.image_width

    def _set_image_width(self, image_width):
        self.image_width = image_width

    def _get_image_height(self):
        return self.image_height

    def _set_image_height(self, image_height):
        self.image_height = image_height

    def _get_exposure_time(self):
        return self.exposure_time

    def _set_exposure_time(self, exposure_time):
        self.exposure_time = exposure_time

    def _get_f_number(self):
        return self.f_number

    def _set_f_number(self, f_number):
        self.f_number = f_number

    def _get_iso_speed(self):
        return self.iso_speed

    def _set_iso_speed(self, iso_speed):
        self.iso_speed = iso_speed

    def _get_metering_mode(self):
        return self.metering_mode

    def _set_metering_mode(self, metering_mode):
        self.metering_mode = metering_mode

    def _get_focal_length(self):
        return self.focal_length

    def _set_focal_length(self, focal_length):
        self.focal_length = focal_length

    def _get_light_source(self):
        return self.light_source

    def _set_light_source(self, light_source):
        self.light_source = light_source

    def _get_exposure_mode(self):
        return self.exposure_mode

    def _set_exposure_mode(self, exposure_mode):
        self.exposure_mode = exposure_mode

    def _get_white_balance(self):
        return self.white_balance

    def _set_white_balance(self, white_balance):
        self.white_balance = white_balance

    def _get_gain_control(self):
        return self.gain_control

    def _set_gain_control(self, gain_control):
        self.gain_control = gain_control

    def _get_contrast(self):
        return self.contrast

    def _set_contrast(self, contrast):
        self.contrast = contrast

    def _get_saturation(self):
        return self.saturation

    def _set_saturation(self, saturation):
        self.saturation = saturation

    def _get_sharpness(self):
        return self.sharpness

    def _set_sharpness(self, sharpness):
        self.sharpness = sharpness

    def _get_image_compression(self):
        return self.image_compression

    def _set_image_compression(self, image_compression):
        self.image_compression = image_compression

    def _get_exif_version(self):
        return self.exif_version

    def _set_exif_version(self, exif_version):
        self.exif_version = exif_version

    def _get_software_version(self):
        return self.software_version

    def _set_software_version(self, software_version):
        self.software_version = software_version

    def _get_hardware_make(self):
        return self.hardware_make

    def _set_hardware_make(self, hardware_make):
        self.hardware_make = hardware_make

    def _get_hardware_model(self):
        return self.hardware_model

    def _set_hardware_model(self, hardware_model):
        self.hardware_model = hardware_model

    def _get_hardware_serial_number(self):
        return self.hardware_serial_number

    def _set_hardware_serial_number(self, hardware_serial_number):
        self.hardware_serial_number = hardware_serial_number
