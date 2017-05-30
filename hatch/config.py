import yaml
import botocore.session


class APIConfig(object):

    def __init__(self, name, region, account_id, role_id):
        self.region = region
        self.account_id = account_id
        self.role_id = role_id
        self.name = name

    @staticmethod
    def parse(config_path):
        with open(config_path, 'r') as stream:
            try:
                cfg = yaml.load(stream)
                return APIConfig(
                    cfg['name'],
                    cfg['region'],
                    cfg['account_id'],
                    cfg['role_id']
                )
            except yaml.YAMLError as exc:
                print exc


class WebsiteConfig(object):

    def __init__(self, name, region):
        self.name = name
        self.region = region

    @staticmethod
    def parse(path):
        session = botocore.session.get_session()
        with open(path, 'r') as stream:
            try:
                cfg = yaml.load(stream)
                region = cfg['region'] if 'region' in cfg else session.get_config_variable('region')
                return WebsiteConfig(
                    cfg['name'],
                    region
                )
            except yaml.YAMLError as exc:
                print exc
