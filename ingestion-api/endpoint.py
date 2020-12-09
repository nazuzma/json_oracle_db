import os
import os.path
from flask import render_template, jsonify
from flask_restful import Resource
from app import auth, app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from json_parser import JsonEMDocument
from exceptions import UploadProcessException
from s3_upload import upload_file_to_s3_bucket, common_mime_types


class BaseResource(Resource):

    @staticmethod
    def make_post_response(status_code, message, **kwargs):
        response = jsonify({**{'message': message}, **kwargs})
        response.status_code = status_code
        return response

    def get_and_check_file_in_request(self, allowed_extensions):
        if 'file' not in request.files:
            raise UploadProcessException('No files part in the HTTP request!')
        file = request.files['file']
        if file.filename == '':
            raise UploadProcessException('No files selected for uploading!')
        extension = os.path.splitext(file.filename)[1].lower()
        if not extension in allowed_extensions:
            raise UploadProcessException('Expected file extension to be one of the following: {0}'.format(', '.join(self.allowed_extensions)))
        return file


class UploadResource(BaseResource):
    allowed_extensions = {'.json'}

    @auth.login_required
    def post(self):
        try:
            file = self.get_and_check_file_in_request(self.allowed_extensions)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)
            document = JsonEMDocument(filename)
            # TODO: Generate UVTI from VTI numbers
            file_id, a_id_map, b_id_map, e_id_map = document.save_to_database()
            # TODO: Add sequence id (_id) and UVTI numbers somewhere in the local JSON file before upload to S3.
            upload_file_to_s3_bucket(app.logger, filename, file_id=file_id, parent_id=None)
        except UploadProcessException as e:
            # Delete the file because it could not be processed.
            if filename and os.path.isfile(filename):
                os.remove(filename)
            return self.make_post_response(e.status_code, e.message)
        return self.make_post_response(201, 'Success', a_id_map=a_id_map, b_id_map=b_id_map, e_id_map=e_id_map)


class AttachResource(BaseResource):

    @auth.login_required
    def post(self, id):
        try:
            file = self.get_and_check_file_in_request(set(common_mime_types.keys()))
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)
            upload_file_to_s3_bucket(app.logger, filename, file_id=None, parent_id=id)
        except UploadProcessException as e:
            # Delete the file because it could not be processed.
            if filename and os.path.isfile(filename):
                os.remove(filename)
            return self.make_post_response(e.status_code, e.message)
        return self.make_post_response(201, 'Success')


@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')


class PingResource(BaseResource):

    @auth.login_required
    def get(self):
        return self.make_post_response(200, 'Hello!', target_database=app.config['DB_SCHEMA'])
