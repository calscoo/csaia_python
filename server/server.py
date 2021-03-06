from flask import Flask, json, jsonify, request
from flask.helpers import send_file
from flask_cors import CORS
import os, sys
from datetime import datetime
from shutil import copyfile, make_archive, rmtree

# allows the script to access other python files in the repo
sys.path.append('../')

# external scripts must be imported after the previous line
import managers.image_manager
from daos.image_dao import update_image_ids
import managers.flight_manager
from objects import range as Range

app = Flask(__name__)

time_format = '%Y%m%d-%H%M%S'

# CORS policies need to be modified, this isn't secure
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

# these need to be changed before deployment
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/query')
def query_image():
    # process to remove any old zip files in the zipped folder
    clean_zipped()

    # unpack request parameters
    image_ids = request.args.get('image_ids')
    if (image_ids == 'null'):
        image_ids = None
    else:
        image_ids = str(image_ids).split(',')

        for i in range(0, len(image_ids)): 
            image_ids[i] = int(image_ids[i])

    user_ids = request.args.get('user_ids')
    if (user_ids == 'null'):
        user_ids = None
    else:
        user_ids = str(user_ids).split(',')

        for i in range(0, len(user_ids)): 
            user_ids[i] = int(user_ids[i])

    flight_ids = request.args.get('flight_ids')
    if (flight_ids == 'null'):
        flight_ids = None
    else:
        flight_ids = str(flight_ids).split(',')

        for i in range(0, len(flight_ids)): 
            flight_ids[i] = int(flight_ids[i])

    extensions = request.args.get('extensions')
    if (extensions == 'null'):
        extensions = None
    else:
        extensions = str(extensions).split(',')

    datetime_range = request.args.get('datetime_range')
    if (datetime_range == 'null'):
        datetime_range = None
    else:
        times = str(datetime_range).split(',')
        datetime_range = range(times[0], times[1])

    latitude_range = request.args.get('latitude_range')
    if (latitude_range == 'null'):
        latitude_range = None
    else:
        lats = str(latitude_range).split(',')
        latitude_range = Range(lats[0], lats[1])

    longitude_range = request.args.get('longitude_range')
    if (longitude_range == 'null'):
        longitude_range = None
    else:
        longs = str(longitude_range).split(',')
        longitude_range = Range(longs[0], longs[1])

    altitude_range = request.args.get('altitude_range')
    if (altitude_range == 'null'):
        altitude_range = None
    else:
        alts = str(altitude_range).split(',')
        altitude_range = Range(alts[0], alts[1])

    make = request.args.get('make')
    if (make == 'null'):
        make = None

    model = request.args.get('model')
    if (model == 'null'):
        model = None


    # get file path from database
    results = managers.image_manager.fetch_images(image_ids, user_ids, flight_ids, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model)

    # handle edge cases
    if (len(results) == 0):
        return jsonify(count=0)

    if (len(results) > 50):
        return jsonify(message='Query too broad')

    # make a new temp folder for the zipped file
    cur_time = datetime.now().strftime(time_format)
    directory_name = 'zipped/12345_' + cur_time
    zip_name = directory_name + '.zip'
    os.mkdir(directory_name)

    # add image results to file
    for image in results:
        name = os.path.basename(image.directory_location)
        copyfile(image.directory_location, directory_name + '/' + name)

    # zip file
    make_archive(directory_name, 'zip', directory_name)

    # delete unzipped directory
    rmtree(directory_name)

    # send zip over to user
    return send_file(zip_name, as_attachment=True)

# Flight Upload Endpoint
@app.route('/upload-flight', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        cur_time = datetime.now().strftime(time_format)
        directory_name = 'uploaded/12345_' + cur_time
        os.mkdir(directory_name)

        # get flight-based request args
        flight_name = request.args.get('flight_name')
        notes = request.args.get('notes')
        field_name = request.args.get('field_name')
        crop = request.args.get('crop')

        # request.files contains all the files attached to the request
        for file in request.files.getlist('image'):
            path = directory_name + '/' + file.filename
            file.save(path)

        # build flight
        flight_info = managers.flight_manager.build_flight(os.path.abspath(directory_name), flight_name, notes, field_name, crop)

        # assign flight id to images
        update_image_ids(flight_info['image-ids'], flight_info['flight-id'])
        
        return jsonify(success=True)

def clean_zipped():
    for filename in os.listdir('zipped'):
        # parse out the time this file was created via name
        timestamp = filename.split('_')[1].split('.zip')[0]
        time = datetime.strptime(timestamp, time_format)

        # get age of this file in seconds
        time_difference = (datetime.now() - time).seconds

        # remove file if it's more than 10 seconds old
        if time_difference > 10:
            os.remove('zipped/' + filename)

if __name__ == '__main__':
   app.run()