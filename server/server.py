from flask import Flask, jsonify, request
from flask_cors import CORS
from objects.flight import flight
import os

app = Flask(__name__)

# CORS policies need to be modified, this isn't secure
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

# these need to be changed before deployment
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

# Flight Upload Endpoint
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        flight_ = flight()

        # request.files contains all the files attached to the request
        for file in request.files.getlist('image'):
            file.save(os.path.join('uploaded', file.filename))

        
        return jsonify(success=True)

if __name__ == '__main__':
   app.run()