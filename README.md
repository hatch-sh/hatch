# easyaws

awseasy is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

## Services

### HTTP(S) APIs

This uses API Gateway, AWS Lambda, and Route53 to build HTTP APIs.

    easywas api create # scaffolding
    easyaws api deploy # 0 config deployment to AWS
    easyaws api start # local development

### Static Websites

This uses S3, CloudFront, and Route53.

    easyaws website create # scaffolding
    easyaws website deploy
    easyaws website start

### Cron jobs

TODO

### Event handlers

TODO

## Project Overview

The general approach is that each kind of service has it's own file in `./src/services` 
where we have a model of the serivce. E.g. for the HTTP API we have `./src/api.py` which
contains an `Api` class that represents our model of a HTTP API.

This modal can then be used for two things. Firstly it is used to figure out what to deploy
to AWS, and secondly it's used to emulate the service for local development. Again, taking
the HTTP API as an example, we use the `Api` class to create a Tornado server we can run locally
that emulate the configuration of running your code on AWS Labmda/API Gateway.

The services are in `./src/services`. The mapping to AWS  are in `./src/aws` and the local development
setup things can be found in `./src/ux`.
