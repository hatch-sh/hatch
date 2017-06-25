import fnmatch
import logging
import mimetypes
import os
import sys
import uuid

import boto3

from hatch.aws.s3 import ensure_website_bucket_exists, get_website_endpoint
from hatch.aws.route53 import ensure_route53_s3_setup
from hatch.config import WebsiteConfig

logger = logging.getLogger(__name__)

ignores = ['.DS_Store', 'website.yml']


class Website(object):

    def __init__(self, path, config):
        self.path = path
        self.config = config
        self._random_name = str(uuid.uuid4())[-12:]

    @staticmethod
    def create(path, config_path):
        config = WebsiteConfig.parse(config_path)
        return Website(path, config)

    def _get_hosted_zone_id(self):
        domain = self.config.domain
        if domain:
            client = boto3.client('route53')
            zones = client.list_hosted_zones()['HostedZones']
            for z in zones:
                if z['Name'] == domain + '.':
                    return z['Id']

            logger.warning('"%s" not found in Route53', domain)
            sys.exit(2)
        return None

    def _get_bucket_name(self, zone_id):
        if zone_id:
            return self.config.domain
        return self.config.name or self._random_name

    def _upload_artifacts(self, bucket):
        mimetypes.add_type('application/json', '.map')
        for artifact in recursive_glob(self.path, '*'):
            mime_type = mimetypes.guess_type(artifact)

            if mime_type is None:
                logger.error('Unknown mime type for %s', artifact)
                sys.exit(1)

            [content_type, _] = mime_type

            logger.debug('Uploading %s [%s]', artifact, content_type)
            file_path = artifact.replace('{}/'.format(self.path), '')
            bucket.upload_file(artifact, file_path, ExtraArgs={
                'ACL': 'public-read',
                'ContentType': content_type
            })

    def deploy(self):
        zone_id = self._get_hosted_zone_id()
        bucket_name = self._get_bucket_name(zone_id)

        s3 = boto3.resource('s3', self.config.region)
        bucket = s3.Bucket(bucket_name)

        ensure_website_bucket_exists(bucket=bucket, region=self.config.region)
        self._upload_artifacts(bucket)

        website_endpoint = get_website_endpoint(bucket_name)

        if zone_id:
            ensure_route53_s3_setup(
                zone_id=zone_id,
                bucket_name=bucket_name,
                website_endpoint=website_endpoint
            )
            url = 'http://{}'.format(self.config.domain)
        else:
            url = 'http://{}'.format(website_endpoint)

        logger.info('Website uploaded to %s', url)


def recursive_glob(folder, pattern):
    for root, _, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, pattern):
            if filename in ignores:
                continue
            else:
                yield os.path.join(root, filename)
