import glob
import os
import sys

import boto3

from hatch.aws.awslambda import Lambda
from hatch.aws.apigateway import Resource, RestApi, Deployment, root_resource_id
from hatch.config import APIConfig as Config


class Api(object):

    def __init__(self, name, endpoints, config):
        self.name = name
        self.endpoints = endpoints
        self.config = config

    def __str__(self):
        return 'Api({}, {})'.format(self.name, str(self.endpoints))

    def __repr__(self):
        return str(self)

    @staticmethod
    def create(source_path, config_path):
        config = Config.parse(config_path)
        full_path = '{}/'.format(source_path)
        endpoints = [
            Endpoint.create(
                path.replace(full_path, ''),
                path
            )
            for path
            in glob.glob('{}*'.format(full_path))
            if os.path.isdir(path)
        ]
        return Api(config.name, endpoints, config)

    def deploy(self):
        lambda_client = boto3.client('lambda', self.config.region)
        apigateway_client = boto3.client('apigateway', self.config.region)

        rest_api = RestApi.find_by_name(apigateway_client, self.name)

        if rest_api is None:
            print 'Creating APIGateway API: {}'.format(self.name)
            rest_api = RestApi.create(apigateway_client, self.name)

        lambdas = Lambda.list(lambda_client)
        resources = Resource.list(apigateway_client, rest_api.api_id)

        root_id = root_resource_id(resources)

        for endpoint in self.endpoints:

            aws_lambda = next((l for l in lambdas if l.name == endpoint.route), None)
            resource = next((r for r in resources if endpoint.route == r.path_part), None)

            # Ensure that all the relevant lambdas exist and are up to date.
            if aws_lambda is None:
                print 'Creating lambda {}'.format(endpoint.route)
                aws_lambda = Lambda.create(self.config, lambda_client, endpoint.route, endpoint.code)
            else:
                print 'Updating lambda {}'.format(endpoint.route)
                aws_lambda.update(lambda_client, endpoint.code)

            # Ensure that all the API Gateway resources exist.
            if resource is None:
                print 'Creating resource {}'.format(endpoint.route)
                resource = Resource.create(
                    root_id,
                    endpoint.route,
                    apigateway_client,
                    rest_api.api_id
                )

            print 'Configuring resource {}'.format(endpoint.route)
            resource.configure_integration(
                apigateway_client,
                lambda_client,
                self.config,
                aws_lambda,
                rest_api,
                endpoint.methods
            )

        stage = 'production'

        Deployment.deploy(apigateway_client, rest_api, stage)

        print 'Deployed to https://{}.execute-api.{}.amazonaws.com/{}'.format(
            rest_api.api_id,
            self.config.region,
            stage
        )


class Endpoint(object):
    '''
    An endpoint represents, as the name suggests, an endpoint that we'd
    like to expose in API Gateway
    '''
    def __init__(self, route, methods, code):
        self.route = route
        self.code = code
        self.methods = methods

    def __str__(self):
        return 'Endpoint({}, {})'.format(self.route, ' '.join(self.methods))

    def __repr__(self):
        return str(self)

    @staticmethod
    def create(route, code):
        methods = ['GET']
        return Endpoint(route, methods, code)
