import glob
import json
import logging
import os
import StringIO
import uuid
import zipfile

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class Lambda(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Lambda({})'.format(self.name)

    def __repr__(self):
        return str(self)

    @staticmethod
    def create(client, role_arn, name, code):
        deployment_package = package(code)
        response = client.create_function(
            FunctionName=name,
            Runtime='python2.7',
            Role=role_arn,
            Handler='handler.handle',
            Description='Description of {}'.format(name),
            Publish=True,
            Code={'ZipFile': deployment_package}
        )
        return Lambda.from_aws_json(response)

    @staticmethod
    def from_aws_json(response):
        return Lambda(response['FunctionName'])

    @staticmethod
    def list(client):
        payload = client.list_functions(MaxItems=500)
        return [
            Lambda.from_aws_json(func)
            for func
            in payload['Functions']
        ]

    def update(self, client, code):
        deployment_package = package(code)
        client.update_function_code(
            FunctionName=self.name,
            Publish=True,
            ZipFile=deployment_package
        )

    def uri(self, region, account_id):
        return 'arn:aws:apigateway:{}:lambda:path/2015-03-31/functions/arn:aws:lambda:{}:{}:function:{}/invocations'.format(
            region, region, account_id, self.name)

    def permissions(self, client, function_name):
        try:
            payload = client.get_policy(FunctionName=self.name)
            policy = json.loads(payload['Policy'])
            return [
                Permission.from_aws_response(statement)
                for statement
                in policy['Statement']
            ]
        except ClientError:
            logger.debug('No permissions for %s', function_name)
            return []

    def allow_invocation(self, client, account_id, rest_api, methods):
        '''
        Ensure that the API Gateway stage is allowed to invoke the lambda
        function.

        This also grants permission for AWS Console to invoke the function.
        '''

        stages = [
            '*',  # testing in AWS Console
            'production'  # production stage
        ]

        permissions = self.permissions(client, self.name)
        existing_source_arns = [p.source_arn for p in permissions]

        for stage in stages:
            for method in methods:
                statement_id = '{}-apigateway-{}-{}-{}'.format(rest_api.name, self.name, method, uuid.uuid4())
                source_arn = 'arn:aws:execute-api:eu-central-1:{}:{}/{}/{}/{}'.format(
                    account_id,
                    rest_api.api_id,
                    stage,
                    method,
                    self.name
                )
                if source_arn not in existing_source_arns:
                    client.add_permission(
                        FunctionName=self.name,
                        StatementId=statement_id,
                        Action='lambda:InvokeFunction',
                        Principal='apigateway.amazonaws.com',
                        SourceArn=source_arn
                    )


class Permission(object):
    def __init__(self, sid, source_arn):
        self.sid = sid
        self.source_arn = source_arn

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.sid == other.sid
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return False

    @staticmethod
    def from_aws_response(statement):
        return Permission(
            sid=statement['Sid'],
            source_arn=statement['Condition']['ArnLike']['AWS:SourceArn']
        )


def package(path):
    '''
        Creates a deployment package based on the contents of the directory
    '''
    buff = StringIO.StringIO()
    zip_archive = zipfile.ZipFile(buff, mode='w')

    # Ensure that the deployment pacakge adheres to our conventions
    files = glob.glob(os.path.join(path, '*.py'))
    handler = os.path.join(path, 'handler.py')
    if handler not in files:
        raise Exception('Missing handler: {}'.format(handler))

    for root, _dirs, files in os.walk(path):
        for filepath in files:

            if filepath.endswith('pyc'):
                pass

            # Set the access of the file in the zip archive.
            # This is required, otherwise AWS Lambda isn't able to import the
            # python modules.
            info = zipfile.ZipInfo(filepath)
            info.external_attr = 0o777 << 16  # give full access to included file

            # Add the file and it's contents.
            contents = _file_get_contents(os.path.join(root, filepath))
            zip_archive.writestr(info, contents)

    zip_archive.close()

    return buff.getvalue()


def _file_get_contents(filename):
    with open(filename) as file_handle:
        return file_handle.read()
