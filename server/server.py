from flask import Flask, jsonify, request
from flask_cors import CORS
import os, sys
from datetime import datetime

# allows the script to access other python files in the repo
sys.path.append('../')

# external scripts must be imported after the previous line
import managers.image_manager
from daos.image_dao import update_image_ids
import managers.flight_manager

app = Flask(__name__)

# CORS policies need to be modified, this isn't secure
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

# these need to be changed before deployment
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# Flight Upload Endpoint
@app.route('/upload-flight', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        cur_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        directory_name = 'uploaded/12345_' + cur_time
        os.mkdir(directory_name)

        # request.files contains all the files attached to the request
        for file in request.files.getlist('image'):
            path = directory_name + '/' + file.filename
            file.save(path)

        flight_info = managers.flight_manager.build_flight(os.path.abspath(directory_name), 'test1', 'test2', 'test3', 'test4')

        num_updated = update_image_ids(flight_info['image-ids'], flight_info['flight-id'])
        print(num_updated)
        
        return jsonify(success=True)

if __name__ == '__main__':
   app.run()