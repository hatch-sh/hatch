import fnmatch
import logging
import mimetypes
import os
import sys

import boto
import boto3

from hatch.aws.s3 import bucket_exists
from hatch.config import WebsiteConfig

logger = logging.getLogger(__name__)

ignores = ['.DS_Store', 'website.yml']


class Website(object):

    def __init__(self, name, path, config):
        self.name = name
        self.path = path
        self.config = config

    @staticmethod
    def create(path, config_path):
        config = WebsiteConfig.parse(config_path)
        return Website(config.name, path, config)

    def deploy(self):
        mimetypes.add_type('application/json', '.map')

        s3 = boto3.resource('s3', self.config.region)
        bucket = s3.Bucket(self.name)
        bucket_website = bucket.Website()

        if not bucket_exists(bucket):
            region = self.config.region
            kwargs = {'ACL': 'public-read'}
            if region != 'us-east-1':
                # https://github.com/boto/boto3/issues/125
                kwargs['CreateBucketConfiguration'] = {'LocationConstraint': region}

            bucket.create(**kwargs)
            bucket_website.put(
                WebsiteConfiguration={
                    'IndexDocument': {
                        'Suffix': 'index.html'
                    },
                    'ErrorDocument': {
                        'Key': '404.html'
                    }
                }
            )

        for artifact in recursive_glob(self.path, '*'):
            mime_type = mimetypes.guess_type(artifact)

            if mime_type is None:
                logger.error('Unknown mime type for %s', artifact)
                sys.exit(1)

            [content_type, _] = mime_type

            logger.debug('Uploading %s [%s]', artifact, content_type)
            bucket.upload_file(artifact, artifact.replace('{}/'.format(self.path), ''), ExtraArgs={
                'ACL': 'public-read',
                'ContentType': content_type
            })

        bucket = boto.connect_s3().get_bucket(self.name)
        url = 'http://{}'.format(bucket.get_website_endpoint())
        logger.info('Website uploaded to %s', url)


def recursive_glob(folder, pattern):
    for root, _, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, pattern):
            if filename in ignores:
                continue
            else:
                yield os.path.join(root, filename)
