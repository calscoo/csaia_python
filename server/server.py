from shutil import copyfile, make_archive, rmtree
from flask import Flask, json, jsonify, request
from flask.helpers import send_file
from datetime import datetime
from flask_cors import CORS
import os, sys


sys.path.append('../')

# external scripts must be imported after the previous line
from enums.privacy import privacy as privacy_enum
from enums.role import roles
import managers.image_manager
import managers.flight_manager
import managers.users_manager
from objects import range as Range

app = Flask(__name__)

# time format for use in file naming
time_format = '%Y%m%d-%H%M%S'

# CORS policies need to be modified, this isn't secure
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

# these need to be changed before deployment
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


def float_or_none(val):
    return None if val is None else float(val)


'''
GET
Sends the client a list of objects that match
multiple query parameters obtained through the request parameters
'''
@app.route('/query')
def query_image():
    # unpack request parameters
    # TODO: This should never be null. Once user creation is implemented, remove this null check
    calling_user_id_str = request.args.get('calling_user_id')
    if (calling_user_id_str == 'null'):
        calling_user_id = None
    else:
        calling_user_id = int(str(calling_user_id_str).split(','))

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
    results = managers.image_manager.fetch_images(calling_user_id, image_ids, user_ids, flight_ids, None, extensions, datetime_range, latitude_range, longitude_range, altitude_range, make, model, None)

    return_object = {
        'objects' : []
    }

    for image in results:
        return_object['objects'].append({
            'id': image.id,
            'user_id': image.user_id,
            'flight_id': image.flight_id,
            'image_extension': image.image_extension,
            'datetime' : image.datetime,
            'latitude': float_or_none(image.latitude),
            'longitude': float_or_none(image.longitude),
            'altitude': float_or_none(image.altitude)
        })

    return jsonify(return_object)


'''
GET
Sends the client a list of user objects
multiple query parameters obtained through the request parameters
'''
@app.route('/fetch-all-users')
def fetch_all_users():

    results = managers.users_manager.fetch_all_users()

    return_object = {
        'objects': []
    }

    for user in results:
        return_object['objects'].append({
            'id': user.id,
            'email': user.email,
            'role': user.role.value,
        })

    return jsonify(return_object)


'''
GET
Sends the client an email value to check if it exists in the system
'''
@app.route('/does-user-exist')
def does_user_exist():

    email = request.args.get('email')

    result = managers.users_manager.does_user_exist(email)

    return_object = {
        'exists': result
    }

    return jsonify(return_object)


'''
GET
Sends the client and email and password to attempt a login
'''
@app.route('/login')
def login():

    email = request.args.get('email')
    password = request.args.get('password')

    login_result = managers.users_manager.validate_login_credentials(email, password)

    return_object = {
        'login_result': login_result
    }

    return jsonify(return_object)


'''
GET
Returns the user's role
'''
@app.route('/get-user-role')
def get_user_role():

    user_id = request.args.get('user_id')

    user_role = managers.users_manager.fetch_user_role(user_id)

    return_object = {
        'user_role': user_role
    }

    return jsonify(return_object)

'''
GET
Returns the user's API key
'''
@app.route('/get-user-api-key')
def get_user_api_key():

    user_id = request.args.get('user_id')
    password = request.args.get('password')

    api_key = managers.users_manager.fetch_user_api_key(user_id, password)

    if api_key is not None:
        return jsonify({'api_key' : api_key})
    
    return jsonify(success=False)

'''
GET
Generates a new API key for a user and returns it
'''
@app.route('/generate-user-api-key')
def generate_user_api_key():

    user_id = request.args.get('user_id')
    password = request.args.get('password')

    api_key = managers.users_manager.generate_user_api_key(user_id, password)

    if api_key is not None:
        return jsonify({'api_key' : api_key})

    return jsonify(success=False)


'''
POST
Allows the client to upload flights
'''
@app.route('/update-user-role', methods=['GET', 'POST'])
def update_user_role():
    if request.method == 'POST':

        # get update request args
        user_id = request.form['user_id']
        role = request.form['role']

        # update user
        managers.users_manager.update_user_role(user_id, roles(int(str(role))))
        return jsonify(success=True)


'''
POST
Allows the client to upload flights
'''
@app.route('/create-user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':

        # get create request args
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # create user
        managers.users_manager.create_user(email, password, roles(int(str(role))))
        return jsonify(success=True)


'''
GET
Sends the client a zipped file of images
Images are fetched via "image_ids" request argument
'''
@app.route('/prepare-zip')
def prepare_zip():
    # process to remove any old zip files in the zipped folder
    clean_zipped()

    image_ids = request.args.get('image_ids')
    calling_user_id = request.args.get('calling_user_id')
    if (image_ids == 'null'):
        image_ids = None
    else:
        image_ids = str(image_ids).split(',')

        for i in range(0, len(image_ids)): 
            image_ids[i] = int(image_ids[i])

    results = managers.image_manager.fetch_images(calling_user_id, image_ids, None, None, None, None, None, None, None, None, None)

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
    # return send_file(zip_name, as_attachment=True)
    return jsonify(zip_name=os.path.basename(zip_name))


@app.route('/download-zip/<name>')
def download_zip(name):
    return send_file('zipped\\' + name, as_attachment=True)


'''
POST
Allows the client to upload flights
'''
@app.route('/upload-flight', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        cur_time = datetime.now().strftime(time_format)
        directory_name = 'uploaded/12345_' + cur_time
        os.makedirs(directory_name)

        # get flight-based request args
        flight_name = request.form['flight_name']
        notes = request.form['notes']
        field_name = request.form['field_name']
        crop = request.form['crop']
        privacy_value = request.form['privacy_value']
        shared_users = request.form['shared_users']

        # request.files contains all the files attached to the request
        for file in request.files.getlist('image'):
            path = directory_name + '/' + file.filename
            file.save(path)

        # build flight
        managers.flight_manager.build_flight(os.path.abspath(directory_name), flight_name, notes, field_name, crop, privacy_enum(int(privacy_value)), shared_users)
        
        return jsonify(success=True)

'''
Method to keep server files to a miniumum

Deletes all files in the zipped folder that
were made more than 10 seconds ago
'''
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