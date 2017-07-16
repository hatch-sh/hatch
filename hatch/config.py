import logging

import yaml
import botocore.session
import boto3
import uuid
import sys

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

    def __init__(self, path=None, name=None, region=None, domain=None):
        self.path = path
        self.name = name
        self.region = region
        self.domain = domain
        if self.domain and self.name:
            logger.warning('Configuration warning: remove "name" when using "domain"')

    @staticmethod
    def defaults():
        return WebsiteConfig(
            path=".",
            name=str(uuid.uuid4())[-12:],
            region=get_region({}),
            domain=None
        )

    @staticmethod
    def parse(path):
        try:
            with open(path, 'r') as stream:
                cfg = yaml.load(stream)
                return WebsiteConfig(
                    path=cfg.get('path'),
                    name=cfg.get('name'),
                    region=get_region(cfg),
                    domain=cfg.get('domain')
                )
        except IOError:
            logger.error('Configuration file does not exist: {}'.format(path))
            sys.exit(1)

    def merge(self, other):
        """Merges this configuration with `other`. The values in `self` takes precedence."""

        if other is None:
            return self

        # Don't override name if domain is already set
        name = other.name if self.domain is None and self.name is None else self.name

        return WebsiteConfig(
            path=self.path if self.path else other.path,
            name=name,
            region=self.region if self.region else other.region,
            domain=self.domain if self.domain else other.domain
        )


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
