import json


class Policy(object):
    AWSLambdaFullAccess = 'arn:aws:iam::aws:policy/AWSLambdaFullAccess'


class Role(object):
    def __init__(self, arn, role_id):
        self.arn = arn
        self.role_id = role_id

    @staticmethod
    def from_aws_json(response):
        return Role(arn=response['Arn'], role_id=response['RoleId'])

    @staticmethod
    def create(client, role_name, policies):
        response = client.create_role(
            RoleName=role_name,
            Description='Created by hatch',
            # This is the policy that describes which services are allowed
            # to assume this role.
            # In this case that's our AWS Lambda functions.
            AssumeRolePolicyDocument=json.dumps({
                'Statement': [
                    {
                        'Principal': {
                            'Service': ['lambda.amazonaws.com']
                        },
                        'Effect': 'Allow',
                        'Action': ['sts:AssumeRole']
                    },
                ]
            })
        )
        for policy in policies:
            client.attach_role_policy(
                PolicyArn=policy,
                RoleName=role_name
            )
        return Role.from_aws_json(response['Role'])

    @staticmethod
    def get(client, role_name):
        try:
            response = client.get_role(RoleName=role_name)
            return Role.from_aws_json(response['Role'])
        except client.exceptions.NoSuchEntityException:
            return None
