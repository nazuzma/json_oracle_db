from flask import Flask
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from logging.handlers import RotatingFileHandler
import logging
import os
import hashlib
from os.path import join

# Release mode (EM_REPO_RELEASE=1) should only be enable on the production server.
debug = int(os.environ.get('EM_REPO_RELEASE', '0')) != 1
app = Flask(__name__)
api = Api(app, prefix="/api")

# Setup basic HTTP authentication
auth = HTTPBasicAuth()
encrypted_user_data = {
    'lda5148': '6730fd4ac492fbf80fa5607646c56d9dfdc53c46a6ae812067ca416dbfec8c0b'
}


@auth.verify_password
def verify(username, password):
    if debug:
        return True
    if not (username and password):
        return False
    hashed = hashlib.sha256(str.encode(password)).hexdigest()
    return encrypted_user_data.get(username.lower()) == hashed


# Flask environment variables
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # limit file size to 10mb
app.config['DB_SCHEMA'] = 'EM_REPO_DEV' if debug else 'EM_REPO'

# Logging
if not debug:
    log_file_name = join(join(os.getcwd(), 'logs'), 'activity.log')
    file_handler = RotatingFileHandler(log_file_name, maxBytes=1024 * 1024 * 20, backupCount=20)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)  # Add log file handler to Flask
    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.INFO)
    werkzeug_log.addHandler(file_handler)  # Add log file handler to Werkzeug (low level Flask routing engine)

target_db_message = 'Target database schema is {0}'.format(app.config['DB_SCHEMA'])
app.logger.info(target_db_message)
print(target_db_message)

# Registering the endpoints
import endpoint

api.add_resource(endpoint.UploadResource, '/upload')
api.add_resource(endpoint.AttachResource, '/attach/<int:id>')
api.add_resource(endpoint.PingResource, '/ping')
