import logging

import yaml
import botocore.session
import boto3

logger = logging.getLogger(__name__)


class APIConfig(object):

    def __init__(self, name, region, account_id):
        self.region = region
        self.account_id = account_id
        self.name = name

    @staticmethod
    def parse(config_path):
        with open(config_path, 'r') as stream:
            cfg = yaml.load(stream)
            return APIConfig(
                cfg['name'],
                get_region(cfg),
                get_account_id()
            )


class WebsiteConfig(object):

    def __init__(self, name=None, region=None, domain=None):
        self.name = name
        self.region = region
        self.domain = domain
        if self.domain and self.name:
            logger.warning('Configuration warning: remove "name" when using "domain"')

    @staticmethod
    def parse(path):
        try:
            with open(path, 'r') as stream:
                cfg = yaml.load(stream)
                return WebsiteConfig(
                    name=cfg.get('name'),
                    region=get_region(cfg),
                    domain=cfg.get('domain')
                )
        except IOError:
            return WebsiteConfig()


def get_region(cfg):
    if 'region' in cfg:
        return cfg['region']
    else:
        session = botocore.session.get_session()
        return session.get_config_variable('region')


def get_account_id():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    return response['Account']
