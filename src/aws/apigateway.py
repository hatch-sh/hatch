
def root_resource_id(resources):
    # TODO: This is somewhat hacky. There must be a better way to get
    # the root id.
    root = [x.resource_id for x in resources if x.path == '/']
    return root[0]


class Deployment(object):

    @staticmethod
    def deploy(client, api, stage):
        return client.create_deployment(
            restApiId=api.api_id,
            stageName=stage,
            description='Deployed by automation'  # TODO: git sha?
        )


class RestApi(object):
    def __init__(self, api_id):
        self.api_id = api_id


class Resource(object):

    def __init__(self, resource_id, parent_id, path_part, path, methods):
        self.resource_id = resource_id
        self.parent_id = parent_id
        self.path_part = path_part
        self.path = path
        self.methods = methods

    def __str__(self):
        return 'Resource({},{},{}, {})'.format(
            self.resource_id,
            self.parent_id,
            self.path_part,
            self.path
        )

    def __repr__(self):
        return str(self)

    def configure_integration(self, config, client, lambda_client, lambda_function, methods):
        '''
        Configures the integration between the API Gateway resource and the
        Lambda function for each HTTP verb that the resource supports.

        Also takes care of the relevant permissions that are required in order
        to allow the Resource to invoke the Lambda.
        '''

        lambda_function.allow_invocation(config, lambda_client, methods)

        for method in methods:

            if method in self.methods:
                continue

            # Register the HTTP method for the resource.
            client.put_method(
                restApiId=config.rest_api_id,
                resourceId=self.resource_id,
                httpMethod=method,
                authorizationType='NONE'
            )

            # Define the integration for the method on the resource.
            # We're going with an AWS_PROXY integration.
            client.put_integration(
                restApiId=config.rest_api_id,
                resourceId=self.resource_id,
                httpMethod=method,
                # We're using AWS_PROXY integration as it defines a clear interface
                # between between the Lambda and API Gateway that makes it possible to
                # return proper http status codes and errors from the Lambdas.
                type='AWS_PROXY',
                # The Lambda to invoke.
                uri=lambda_function.uri(config.region, config.account_id),
                # From the docs: You must use the POST method for the integration
                # request when calling a Lambda function
                integrationHttpMethod='POST',
                # If the Content-Type doesn't match any of the ones defined in
                # requestTemplates (that is, application/json, for now) then reject the
                # request.
                passthroughBehavior='NEVER',
                # TODO: Figure out if this is needed.
                contentHandling='CONVERT_TO_TEXT'
            )

            # Define how to transform the response from the lambda into HTTP.
            client.put_integration_response(
                restApiId=config.rest_api_id,
                resourceId=self.resource_id,
                httpMethod=method,
                statusCode='200',
                contentHandling='CONVERT_TO_TEXT',
                responseTemplates={
                    'application/json': '$input.json("$.body")'
                }
            )

            # Define how to result from the lambda is mapped into the response that
            # the client receives.
            client.put_method_response(
                restApiId=config.rest_api_id,
                resourceId=self.resource_id,
                httpMethod=method,
                statusCode='200',
                # The docs claim that the value should be a string that specifies a
                # contant value for the headers OR a json expression. However, it seems
                # that for Lambda integrations it should be a boolean specifying if the
                # headers should be accepted.
                responseParameters={
                    'method.response.header.Access-Control-Allow-Headers': True,
                    'method.response.header.Access-Control-Allow-Methods': True,
                    'method.response.header.Access-Control-Allow-Origin': True
                },
                responseModels={
                    # if the content type is json then don't do anything?
                    'application/json': 'Empty'
                }
            )

    def delete(self, config, client):
        client.delete_resource(
            restApiId=config.rest_api_id,
            resourceId=self.resource_id
        )

    @staticmethod
    def create(parent_id, path_part, client, rest_api_id):
        response = client.create_resource(
            restApiId=rest_api_id,
            parentId=parent_id,
            pathPart=path_part
        )
        return Resource.from_aws_json(response)

    @staticmethod
    def list(client, rest_api_id):
        response = client.get_resources(restApiId=rest_api_id, limit=500)
        return [
            Resource.from_aws_json(item)
            for item in response['items']
        ]

    @staticmethod
    def from_aws_json(response):
        return Resource(
            resource_id=response['id'],
            parent_id=response['parentId'] if 'parentId' in response else None,
            path_part=response['pathPart'] if 'pathPart' in response else None,
            path=response['path'],
            methods=response['resourceMethods'].keys() if 'resourceMethods' in response else []
        )
