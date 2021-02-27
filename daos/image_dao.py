from daos.tools import dao_tools
from pypika import Query, Table

insert_images_query = """
INSERT INTO images(
user_id, flight_id, directory_location, image_extension, datetime, latitude, 
longitude, altitude, image_width, image_height, exposure_time, 
f_number, iso_speed, metering_mode, focal_length, light_source, 
exposure_mode, white_balance, gain_control, contrast, saturation, 
sharpness, image_compression, exif_version, software_version, 
hardware_make, hardware_model, hardware_serial_number)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def insert_images(image_records):
    result = dao_tools.execute(insert_images_query, image_records)


def select_images(select_columns, image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model):
    """
    General purpose image selection method built to cover a broad demand of queries.
    Every parameter can be None and list values can accept any number of elements including 0.
    This was built to flesh out image selections in the manager without having to write complex queries.

    Parameters
    ----------
    select_columns : string or None
        The optional comma delimited string of columns to select on
        NOTE: if this value is None, all (*) columns will be selected
    image_ids : list[int]
        The optional list of image ids
    user_ids : list[int]
        The optional list of user ids
    flight_ids : list[int]
        The optional list of flight ids
    extensions : list[str]
        The optional list of image format extensions
    datetime_range : objects.range
        The optional range of datetimes
    latitude_range : objects.range
        The optional range of latitudes
    longitude_range : objects.range
        The optional range of longitudes
    altitude_range : objects.range
        The optional range of altitudes
    make : str
        The optional hardware make
        NOTE: Uses a LIKE comparision, full hardware make is not necessary, case IN-sensitive
    model : str
        The optional hardware model
        NOTE: Uses a LIKE comparision, full hardware model is not necessary, case IN-sensitive

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    images = Table('images')
    select_image_query = Query.from_(images).select('*' if select_columns is None else select_columns)
    if image_ids is not None and len(image_ids) > 0:
        select_image_query = select_image_query.where(images.id.isin(image_ids))
    if user_ids is not None and len(user_ids) > 0:
        select_image_query = select_image_query.where(images.user_id.isin(user_ids))
    if flight_ids is not None and len(flight_ids) > 0:
        select_image_query = select_image_query.where(images.flight_id.isin(flight_ids))
    if extensions is not None and len(extensions) > 0:
        select_image_query = select_image_query.where(images.image_extension.isin(extensions))
    if datetime_range is not None:
        select_image_query = select_image_query.where(images.datetime >= datetime_range.begin).where(images.datetime <= datetime_range.end)
    if latitude_range is not None:
        select_image_query = select_image_query.where(images.latitude >= latitude_range.begin).where(images.latitude <= latitude_range.end)
    if longitude_range is not None:
        select_image_query = select_image_query.where(images.longitude >= longitude_range.begin).where(images.longitude <= longitude_range.end)
    if altitude_range is not None:
        select_image_query = select_image_query.where(images.altitude >= altitude_range.begin).where(images.altitude <= altitude_range.end)
    if make is not None:
        select_image_query = select_image_query.where(images.hardware_make.like('%' + make + '%'))
    if model is not None:
        select_image_query = select_image_query.where(images.hardware_model.like('%' + model + '%'))
    return dao_tools.execute(select_image_query.get_sql(quote_char=None))


def select_all_images(select_columns):
    """
    Delegates to image_dao.select_images
    Used for selecting on all images without restrictions

    Parameters
    ----------
    select_columns : string or None
        The optional comma delimited string of columns to select on
        NOTE: if this value is None, all (*) columns will be selected

    Returns
    -------
    list[tuple]
        Query results based on incoming parameters.
        NOTE: This will return None for queries that return no results.
    """
    return select_images(select_columns, None, None, None, None, None, None, None, None, None, None)