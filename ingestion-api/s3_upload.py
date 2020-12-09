import os
import os.path
import boto3
import crypto as cr
from chunk_bytes import ChunkBytesIO, MB
from exceptions import UploadProcessException
import oracle_db
import threading
from app import debug

common_mime_types = {
    '.json': 'application/json',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.txt': 'text/plain',
    '.pdf': 'application/pdf',
    '.csv': 'text/csv',
    '.gif': 'image/gif',
}


def upload_file_to_s3_bucket(logger, file_name, file_id, parent_id):
    logger.info('Starting upload of {0} attached to #{1}...'.format(file_name, parent_id))
    name, ext = os.path.splitext(os.path.basename(file_name))
    object_name = '{0}/{1}{2}'.format(parent_id, name, ext) if parent_id else 'json/{0}{1}'.format(name, ext)
    try:
        # Insert a tracking record in our database to track the async cloud upload process.
        with oracle_db.get_connection() as connection:
            if not file_id:
                file_id = oracle_db.get_unique_id(connection)
            oracle_db.upsert_cloud_upload_status(connection, file_id, parent_id or 0, os.path.basename(file_name), object_name, 'Pending')
        # Start the actual upload process asynchronously in a separate thread.
        thread_upload = threading.Thread(target=_async_upload_function, args=(logger, file_name, file_id, parent_id or 0, object_name))
        thread_upload.start()
    except Exception as e:
        raise UploadProcessException('Cannot upload file to S3: {0}'.format(e)) from e


def _async_upload_function(logger, file_name, file_id, parent_id, object_name):
    bucket_name = 'emea-em-ctl-repo'
    chunk_size = 50 * MB
    try:
        s3 = boto3.client('s3', aws_access_key_id=cr.decrypt(cr.lda5148_aws_aki), aws_secret_access_key=cr.decrypt(cr.lda5148_aws_sak))
        mime_type = common_mime_types.get('ext', 'application/octet-stream')
        if not debug:  # Skip the actually upload if not in production
            with open(file_name, 'rb') as f:
                mpu = s3.create_multipart_upload(Bucket=bucket_name, Key=object_name, ContentType=mime_type, StorageClass='STANDARD_IA')
                mpu_id = mpu['UploadId']
                index = 1
                parts = list()
                chunk = f.read(chunk_size)
                while chunk:
                    part = s3.upload_part(Bucket=bucket_name, Key=object_name, PartNumber=index, UploadId=mpu_id, Body=chunk)
                    parts.append({'PartNumber': index, 'ETag': part['ETag']})
                    index += 1
                    chunk = f.read(chunk_size)
            if parts:
                s3.complete_multipart_upload(Bucket=bucket_name, Key=object_name, UploadId=mpu_id, MultipartUpload={'Parts': parts})
        with oracle_db.get_connection() as connection:
            oracle_db.upsert_cloud_upload_status(connection, file_id, parent_id, os.path.basename(file_name), object_name, 'Complete')
    except Exception as e:
        logger.exception(e)
        with oracle_db.get_connection() as connection:
            oracle_db.upsert_cloud_upload_status(connection, file_id, parent_id, os.path.basename(file_name), object_name, 'Failed')


