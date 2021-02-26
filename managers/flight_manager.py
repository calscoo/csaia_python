from daos import flight_dao
from managers import image_manager

def build_flight(path, flight, notes, field, crop):
    flight_records = []
    image_manager.upload_images(path)
    user_id = None
    flight_name = flight #input("File name: ")
    manual_notes = notes #input("Notes: ")
    address = 'Test' # Using google maps for this field
    field_name = field #input("Field: ")
    crop_name = crop #input("Crop: ")
    latitude = image_manager.get_Latitude()
    longitude = image_manager.get_Longitude()
    altitude = image_manager.get_Altitude()
    start = image_manager.get_start_Time()
    end = image_manager.get_end_Time()
    make = image_manager.get_Make()
    model = image_manager.get_Model() 
    average_latitude =  latitude
    average_longitude = longitude
    average_altitude = altitude
    flight_start_time = start   
    flight_end_time = end
    hardware_make = make
    hardware_model = model
    '''
    print(type(user_id), type(flight_name), type(manual_notes), type(address), type(field_name), type(crop_name),
          type(average_latitude), type(average_longitude), type(average_altitude), type(flight_start_time), type(flight_end_time),
          type(hardware_make), type(hardware_model))
    '''
    flight_records.insert(0, (user_id, flight_name, manual_notes, address, field_name,
                            crop_name, average_latitude, average_longitude, average_altitude, flight_start_time,
                            flight_end_time, hardware_make, hardware_model))

    flight_dao.insert_flights(flight_records)

#print(build_flight('Test', 'Test', 'Test', 'Test'))