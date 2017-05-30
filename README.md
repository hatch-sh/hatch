# hatch

hatch is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website, HTTP API's
etc. quick and easy.

## Services

### HTTP(S) APIs

This uses API Gateway, AWS Lambda, and Route53 to build HTTP APIs.

    easywas api create # scaffolding
    hatch api start # local development
    hatch api deploy # 0 config deployment to AWS

### Static Websites

This uses S3, CloudFront, and Route53.

    hatch website create # scaffolding
    hatch website deploy
    hatch website start

### Cron jobs

TODO

### Event handlers

TODO

## Develop on hatch

    git clone git@github.com:mads-hartmann/hatch.git && cd hatch
    make setup
    .venv/bin/hatch api deploy examples/api
    .venv/bin/hatch website deploy examples/website

## Project Overview

The general approach is that each kind of service has it's own file in
`./hatch/services` where we have a model of the service. E.g. for the HTTP
API we have `./hatch/services/api.py` which contains an `Api` class that
represents our model of a HTTP API.

This modal can then be used for two things. Firstly it is used to figure out
what to deploy to AWS, and secondly it's used to emulate the service for local
development. Again, taking the HTTP API as an example, we use the `Api` class
to create a Tornado server we can run locally that emulate the configuration of
running your code on AWS Labmda/API Gateway.

The services are in `./hatch/services`. The mapping to AWS are in
`./hatch/aws` and the local development setup things can be found in
`./hatch/ux`.
