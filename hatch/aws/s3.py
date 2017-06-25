from boto import connect_s3
from boto.s3.connection import OrdinaryCallingFormat
from botocore.client import ClientError


def bucket_exists(bucket):
    try:
        bucket.creation_date
        return True
    except ClientError:
        return False


def get_website_endpoint(bucket_name):
    # bucket names with .'s in them need to use the calling_format option,
    # otherwise the connection will fail.
    # See https://github.com/boto/boto/issues/2836
    bucket = connect_s3(
        calling_format=OrdinaryCallingFormat()
    ).get_bucket(bucket_name, validate=False)
    return bucket.get_website_endpoint()


def ensure_website_bucket_exists(bucket, region=None):
    bucket_website = bucket.Website()

    if not bucket_exists(bucket):
        kwargs = {'ACL': 'public-read'}
        if region and region != 'us-east-1':
            # See https://github.com/boto/boto3/issues/125
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
