#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Deploys the web application to S3 in a bucket.
"""

import sys
import mimetypes
import fnmatch
import os

import boto3
from botocore.client import ClientError


AWS_REGION = 'eu-central-1'
AWS_ACCOUNT_ID = '790804032123'
S3_BUCKET = 'conferencevideohygge.com'

ignores = ['.DS_Store']

def recursive_glob(folder, pattern):
    for root, _, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, pattern):
            print 'filename is ' + filename
            if filename in ignores:
                print 'Ignoring {}'.format(filename)
            else:
                yield os.path.join(root, filename)


def bucket_exists(bucket):
    try:
        bucket.creation_date
        return True
    except ClientError:
        return False


def deploy():
    mimetypes.add_type('application/json', '.map')

    s3 = boto3.resource('s3', AWS_REGION)
    bucket = s3.Bucket(S3_BUCKET)
    website = bucket.Website()

    if not bucket_exists(bucket):
        bucket.create(
            ACL='public-read',
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            }
        )
        website.put(
            WebsiteConfiguration={
                'IndexDocument': {
                    'Suffix': 'index.html'
                },
                'ErrorDocument': {
                    'Key': '404.html'
                }
            }
        )

    for artifact in recursive_glob('web/dist', '*'):
        mime_type = mimetypes.guess_type(artifact)

        if mime_type is None:
            print 'Unknown mime type for {}'.format(artifact)
            sys.exit(1)

        [conten_type, _] = mime_type

        print 'Uploading {} as {}'.format(artifact, conten_type)
        bucket.upload_file(artifact, artifact.replace('web/dist/', ''), ExtraArgs={
            'ACL': 'public-read',
            'ContentType': conten_type
        })

    print 'Website uploaded'


if __name__ == "__main__":
    deploy()
