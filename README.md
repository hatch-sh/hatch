# easyaws

awseasy is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website, HTTP API's
etc. quick and easy.

## Services

### HTTP(S) APIs

This uses API Gateway, AWS Lambda, and Route53 to build HTTP APIs.

    easywas api create # scaffolding
    easyaws api start # local development
    easyaws api deploy # 0 config deployment to AWS

### Static Websites

This uses S3, CloudFront, and Route53.

    easyaws website create # scaffolding
    easyaws website deploy
    easyaws website start

### Cron jobs

TODO

### Event handlers

TODO

## Develop on easyaws

    git clone git@github.com:mads-hartmann/easyaws.git && cd easyaws
    make setup
    .venv/bin/easyaws api deploy examples/api
    .venv/bin/easyaws website deploy examples/website

## Project Overview

The general approach is that each kind of service has it's own file in
`./easyaws/services` where we have a model of the service. E.g. for the HTTP
API we have `./easyaws/services/api.py` which contains an `Api` class that
represents our model of a HTTP API.

This modal can then be used for two things. Firstly it is used to figure out
what to deploy to AWS, and secondly it's used to emulate the service for local
development. Again, taking the HTTP API as an example, we use the `Api` class
to create a Tornado server we can run locally that emulate the configuration of
running your code on AWS Labmda/API Gateway.

The services are in `./easyaws/services`. The mapping to AWS are in
`./easyaws/aws` and the local development setup things can be found in
`./easyaws/ux`.
