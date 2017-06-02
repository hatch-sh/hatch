import sys
import mimetypes
import fnmatch
import os

import boto3

from hatch.aws.s3 import bucket_exists
from hatch.config import WebsiteConfig


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
            bucket.create(
                ACL='public-read',
                CreateBucketConfiguration={
                    'LocationConstraint': self.config.region
                }
            )
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
                print 'Unknown mime type for {}'.format(artifact)
                sys.exit(1)

            [content_type, _] = mime_type

            print 'Uploading {} [{}]'.format(artifact, content_type)
            bucket.upload_file(artifact, artifact.replace('{}/'.format(self.path), ''), ExtraArgs={
                'ACL': 'public-read',
                'ContentType': content_type
            })

        url = 'http://{}.s3-website.{}.amazonaws.com'.format(self.name, self.config.region)
        print 'Website uploaded to {}'.format(url)


def recursive_glob(folder, pattern):
    for root, _, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, pattern):
            if filename in ignores:
                continue
            else:
                yield os.path.join(root, filename)
