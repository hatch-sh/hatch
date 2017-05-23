import yaml

class Config(object):

    def __init__(self, name, region, account_id, role_id, rest_api_id):
        self.region = region
        self.account_id = account_id
        self.role_id = role_id
        self.rest_api_id = rest_api_id
        self.name = name


    def __str__(self):
        return 'Config({}, {}, {})'.format(
            self.name,
            self.region,
            self.role_id
        )

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse(config_path):
        with open(config_path, 'r') as stream:
            try:
                cfg = yaml.load(stream)
                return Config(
                    cfg['name'],
                    cfg['region'],
                    cfg['account_id'],
                    cfg['role_id'],
                    cfg['rest_api_id']
                )
            except yaml.YAMLError as exc:
                print exc
