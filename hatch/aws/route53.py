import logging

import boto3


logger = logging.getLogger(__name__)


# There is no API for these so we have to embed and lookup
# https://forums.aws.amazon.com/thread.jspa?threadID=116724
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
ENDPOINT_HOSTED_ZONE_IDS = {
    's3-website.us-east-2.amazonaws.com': 'Z2O1EMRO9K5GLX',
    's3-website-us-east-1.amazonaws.com': 'Z3AQBSTGFYJSTF',
    's3-website-us-west-1.amazonaws.com': 'Z2F56UZL2M1ACD',
    's3-website-us-west-2.amazonaws.com': 'Z3BJ6K6RIION7M',
    's3-website.ca-central-1.amazonaws.com': 'Z1QDHH18159H29',
    's3-website.ap-south-1.amazonaws.com': 'Z11RGJOFQNVJUP',
    's3-website.ap-northeast-2.amazonaws.com': 'Z3W03O7B5YMIYP',
    's3-website-ap-southeast-1.amazonaws.com': 'Z3O0J2DXBE1FTB',
    's3-website-ap-southeast-2.amazonaws.com': 'Z1WCIGYICN2BYD',
    's3-website-ap-northeast-1.amazonaws.com': 'Z2M4EHUR26P7ZW',
    's3-website.eu-central-1.amazonaws.com': 'Z21DNDUVLTQW6Q',
    's3-website-eu-west-1.amazonaws.com': 'Z1BKCTXD74EZPE',
    's3-website.eu-west-2.amazonaws.com': 'Z3GKZC51ZF0DB4',
    's3-website-sa-east-1.amazonaws.com': 'Z7KQH4QJS55SO',
}


def ensure_route53_s3_setup(zone_id, bucket_name, website_endpoint):
    record_name = bucket_name + '.'
    endpoint = website_endpoint.split(record_name)[1]
    target_hosted_zone_id = ENDPOINT_HOSTED_ZONE_IDS[endpoint]

    client = boto3.client('route53')

    existing_record_sets = client.list_resource_record_sets(
        HostedZoneId=zone_id,
    )['ResourceRecordSets']
    for record in existing_record_sets:
        if record['Type'] == 'A' and record['Name'] == record_name:
            return

    logger.debug('Creating Route53 record set')
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': bucket_name,
                        'Type': 'A',
                        'AliasTarget': {
                            'HostedZoneId': target_hosted_zone_id,
                            'DNSName': endpoint,
                            'EvaluateTargetHealth': False
                        },
                    }
                },
            ]
        }
    )
