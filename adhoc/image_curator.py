import os
import sys
import re
import exifread
from GPSPhoto import gpsphoto

handle_batch_insertion_errors = """
SHOW VARIABLES where Variable_name like '%timeout';
SET GLOBAL connect_timeout=660;
SET GLOBAL wait_timeout=2147483;
SET GLOBAL max_allowed_packet=1073741824;
SELECT @@global.max_allowed_packet;
"""

supported_formats = ('.jpg', '.jpeg', '.tif', '.tiff')

skip_files = [
    '/gpfs1/projects/john.nowatzki/2016/Farmers 2016/Brandon Roller/May/6cm/Roller May 6cm.tif',
    '/gpfs1/projects/john.nowatzki/2016/Farmers 2016/Darrell Nottestad/MAY/6 cm/Nottestad_May_6cm.tif',
    '/gpfs1/projects/john.nowatzki/2017/Joel Ransom/0419 Winter Wheat/Quad Sensor Images/RR_730/RR_730.files/0/0/orthomosaic/tile-3-2.tif',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/4 cm and 6 cm Resolution - Ellingson/May_2016_6cm_Clip1.tif',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/4 cm and 6 cm Resolution - Ellingson/June_2016_4cm_Clip1.tif',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/4 cm and 6 cm Resolution - Ellingson/July_2016_4cm_Clip11.tif',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/1 Meter Resolution - Ellingson/May_2016_1M.jpg',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/1 Meter Resolution - Ellingson/June_2016_1meter.jpg',
    '/gpfs1/projects/john.nowatzki/2017/Bill Ellingson -/1 Meter Resolution - Ellingson/July_2016_1meter.jpg',
    '/gpfs1/projects/john.nowatzki/2017/Dicamba Drift/Rosholt Dicamba Drift/08012017/Rosholt_DicambaDrift_08012017/0004SET/000/IMG_0166_1.tif',
    '/gpfs1/projects/john.nowatzki/2017/Dicamba Drift/Rosholt Dicamba Drift/08012017/Rosholt_DicambaDrift_08012017/0004SET/000/IMG_0166_2.tif',
    '/gpfs1/projects/john.nowatzki/2017/Dicamba Drift/Rosholt Dicamba Drift/08012017/Rosholt_DicambaDrift_08012017/0004SET/000/IMG_0166_3.tif',
    '/gpfs1/projects/john.nowatzki/2017/Dicamba Drift/Rosholt Dicamba Drift/08012017/Rosholt_DicambaDrift_08012017/0004SET/000/IMG_0166_4.tif',
    '/gpfs1/projects/john.nowatzki/2017/Dicamba Drift/Rosholt Dicamba Drift/08012017/Rosholt_DicambaDrift_08012017/0004SET/000/IMG_0166_5.tif',
    '/gpfs1/projects/john.nowatzki/2017/Kathryn/PurpleLoosestrife/07132017/07132017_SlantRange_ValleyCity_PurpleLoosestrife/20170713T180342/GeoTIFF/1499969297.132.tif',
    '/gpfs1/projects/john.nowatzki/2017/Kathryn/PurpleLoosestrife/07132017/07132017_SlantRange_ValleyCity_PurpleLoosestrife/20170713T180342/GeoTIFF/1499969296.132.tif',
    '/gpfs1/projects/john.nowatzki/2019/Sharp-tailed Grouse 2109/1BSE 4-10-19/1BSE.files/0/0/orthomosaic/tile-1-2.tif'
]


def none_check_str(val, w_tick):
    return "NULL" if (val is None) else (("'" + str(val) + "'") if w_tick else (str(val)))


def handle_integer_parse_errors(val):
    if (val is None) or (val == "NULL"):
        return "NULL"
    try:
        int(str(val))
    except ValueError:
        return "NULL"
    return val


def fix_quotes(val):
    return re.sub("'", "''", val)


def curate(directories, query_output_file):
    file = open(query_output_file, "a")
    file.write("\nINSERT INTO")
    file.write("\ncsaia_database.images(user_id, flight_id, directory_location, image_extension, datetime, latitude, longitude, altitude, image_width, image_height, exposure_time, f_number, iso_speed, metering_mode, focal_length, light_source, exposure_mode, white_balance, gain_control, contrast, saturation, sharpness, image_compression, exif_version, software_version, hardware_make, hardware_model, hardware_serial_number)")
    file.write("\nVALUES")
    file.close()
    for directory in directories:
        for root, subdirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                if path not in skip_files and path.lower().endswith(supported_formats):
                    failed = False
                    try:
                        tags = exifread.process_file(open(path, 'rb'))
                        gps_data = gpsphoto.getGPSData(path)
                    except:
                        error_log = open("error.log", "a")
                        error_log.write("\n\nfailed: " + str(path))
                        error_log.write("\nerror: " + str(sys.exc_info()[0]))
                        error_log.close()
                        failed = True
                        pass

                    if failed is False:
                        trace_log = open("trace.log", "a")
                        trace_log.write("\n" + str(path))
                        trace_log.close()

                        path_to_store = fix_quotes(path)
                        ext = os.path.splitext(file)[1].lower()
                        latitude = none_check_str(gps_data.get('Latitude'), True)
                        longitude = none_check_str(gps_data.get('Longitude'), True)
                        altitude = none_check_str(gps_data.get('Altitude'), True)
                        date_time = none_check_str(tags.get('Image DateTime'), True)
                        exposure_time = none_check_str(tags.get('EXIF ExposureTime'), True)
                        f_number = none_check_str(tags.get('EXIF FNumber'), True)
                        metering_mode = none_check_str(tags.get('EXIF MeteringMode'), True)
                        focal_length = none_check_str(tags.get('EXIF FocalLength'), True)
                        exif_version = none_check_str(tags.get('EXIF ExifVersion'), True)
                        software_version = none_check_str(tags.get('Image Software'), True)
                        hardware_make = none_check_str(tags.get('Image Make'), True)
                        hardware_model = none_check_str(tags.get('Image Model'), True)
                        hardware_serial_number = none_check_str(tags.get('EXIF BodySerialNumber'), True)
                        light_source = none_check_str(tags.get('EXIF LightSource'), True)
                        white_balance = none_check_str(tags.get('EXIF WhiteBalance'), True)
                        gain_control = none_check_str(tags.get('EXIF GainControl'), True)
                        contrast = none_check_str(tags.get('EXIF Contrast'), True)
                        saturation = none_check_str(tags.get('EXIF Saturation'), True)
                        sharpness = none_check_str(tags.get('EXIF Sharpness'), True)
                        image_compression = none_check_str(tags.get('Image Compression'), True)

                        height_1 = none_check_str(tags.get('Image ImageWidth'), False)
                        height_2 = none_check_str(tags.get('EXIF ExifImageWidth'), False)
                        width_1 = none_check_str(tags.get('Image ImageLength'), False)
                        width_2 = none_check_str(tags.get('EXIF ExifImageLength'), False)
                        iso_1 = none_check_str(tags.get('EXIF ISOSpeed'), False)
                        iso_2 = none_check_str(tags.get('EXIF ISOSpeedRatings'), False)
                        exp_1 = none_check_str(tags.get('EXIF ExposureProgram'), True)
                        exp_2 = none_check_str(tags.get('EXIF ExposureMode'), True)
                        image_height = handle_integer_parse_errors(height_1 if height_2 == "NULL" else height_2)
                        image_width = handle_integer_parse_errors(width_1 if width_2 == "NULL" else width_2)
                        iso_speed = handle_integer_parse_errors(iso_1 if iso_2 == "NULL" else iso_2)
                        exposure_mode = exp_1 if exp_2 == "NULL" else exp_2
                        query_file = open(query_output_file, "a")
                        query_file.write("\n(NULL, NULL, '"+str(path_to_store)+"', '"+str(ext)+"', "+date_time+", "+latitude+", "+longitude+", "+altitude+", "+image_width+", "+image_height+", "+exposure_time+", "+f_number+", "+iso_speed+", "+metering_mode+", "+focal_length+", "+light_source+", "+exposure_mode+", "+white_balance+", "+gain_control+", "+contrast+", "+saturation+", "+sharpness+", "+image_compression+", "+exif_version+", "+software_version+", "+hardware_make+", "+hardware_model+", "+hardware_serial_number+"),")
                        query_file.close()

                        del path_to_store
                        del ext
                        del tags
                        del gps_data
                        del latitude
                        del longitude
                        del altitude
                        del date_time
                        del exposure_time
                        del f_number
                        del metering_mode
                        del focal_length
                        del exif_version
                        del software_version
                        del hardware_make
                        del hardware_model
                        del hardware_serial_number
                        del light_source
                        del white_balance
                        del gain_control
                        del contrast
                        del saturation
                        del sharpness
                        del image_compression
                        del image_height
                        del image_width
                        del iso_speed
                        del exposure_mode


curate(['/gpfs1/projects/john.nowatzki/2017'], "bulk_image_insert_query_2017.sql")
