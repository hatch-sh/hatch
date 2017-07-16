# coding=UTF-8
import logging
import boto3
from botocore.client import ClientError

from hatch.aws.utils import get_error_code


logger = logging.getLogger(__name__)
client = boto3.client('cloudfront')


def ensure_cloudfront_s3_setup(bucket_name, domain_name):
    origin_id = 'S3-{}'.format(bucket_name)
    origin_domain_name = '{}.s3.amazonaws.com'.format(bucket_name)

    try:
        client.create_distribution(
            DistributionConfig={
                'CallerReference': origin_id,
                'Aliases': {
                    'Quantity': 1,
                    'Items': [domain_name],
                },
                'DefaultRootObject': 'index.html',
                'Origins': {
                    'Quantity': 1,
                    'Items': [
                        {
                            'Id': origin_id,
                            'OriginPath': '/index.html',
                            'DomainName': origin_domain_name,
                            'S3OriginConfig': {u'OriginAccessIdentity': ''},
                        },
                    ]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_id,
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {
                            'Forward': 'none',
                        },
                    },
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0,
                    },
                    'ViewerProtocolPolicy': 'allow-all',
                    'MinTTL': 0,
                    'AllowedMethods': {
                        'Quantity': 2,
                        'Items': [
                            'GET',
                            'HEAD'
                        ],
                        'CachedMethods': {
                            'Quantity': 2,
                            'Items': [
                                'GET',
                                'HEAD'
                            ]
                        }
                    },
                    'SmoothStreaming': False,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000,
                    'Compress': True,
                },
                'Comment': 'Created by Hatch.sh',
                'PriceClass': 'PriceClass_All',
                'Enabled': True,
                'IsIPV6Enabled': True,
            }
        )
    except ClientError as ex:
        error_code = get_error_code(ex)
        if error_code == 'DistributionAlreadyExists':
            logger.warning('Warning: A CloudFront distribution named %s was already configured... 🤞', origin_id)
