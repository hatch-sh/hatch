from botocore.client import ClientError


def bucket_exists(bucket):
    try:
        bucket.creation_date
        return True
    except ClientError:
        return False
