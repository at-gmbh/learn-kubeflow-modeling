import os
import boto3
from urllib.parse import urlparse
import numpy as np
from s3fs.core import S3FileSystem


def copy_from_disk_to_s3(source_path, target_uri):
    """
    Copies data from source_path (on local disk) to the target_uri (on s3). If source_path is a folder  (such as for example a folder
    with a TensorFlow SavedModel) then a recursive copy is performed.
    """

    s3 = boto3.Session().resource("s3")

    if os.path.isdir(source_path):
        _recursively_copy_directory(source_path, target_uri)
    else:
        bucket, key = _get_bucket_and_key(target_uri)
        s3.Object(bucket, key).put(Body=open(source_path, "rb"))


def copy_from_s3_to_disk(source_uri, target_path, overwrite=False):
    s3 = boto3.Session().resource("s3")
    target_dir = os.path.split(target_path)[0]

    if not overwrite and os.path.isfile(target_path):
        pass
    else:
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        bucket, key = _get_bucket_and_key(source_uri)

        s3.meta.client.download_file(bucket,
                                     key,
                                     target_path)

def read_array_from_s3(array_uri):
    s3 = S3FileSystem()
    bucket, key =  _get_bucket_and_key(array_uri)
    return np.load(s3.open('{}/{}'.format(bucket, key)))

def write_array_to_s3(array_uri, arr):
    s3 = S3FileSystem()
    bucket, key =  _get_bucket_and_key(array_uri)
    return np.save(s3.open('{}/{}'.format(bucket, key), "wb"), arr)

def _recursively_copy_directory(directory, s3_dir):
    """
    Recursively copy a folder and all its contents to s3

    :param directory:
    :param s3_dir:
    :return:
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            subfolder = root.replace(directory, "").replace("\\", "/")

            copy_from_disk_to_s3(
                source_path=os.path.join(root, file),
                target_uri=s3_dir + subfolder + "/" + file)


def _get_bucket_and_key(s3_uri):
    """parse the bucket and key values from an s3 uri"""
    parsed = urlparse(s3_uri)
    return parsed.netloc, parsed.path[1:]
