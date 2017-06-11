# hatch.sh

Hatch.sh makes it easy to build products using [Amazon Web Services (AWS)][aws].

[![Build Status](https://travis-ci.org/mads-hartmann/hatch.svg?branch=master)](https://travis-ci.org/mads-hartmann/hatch)

**NOTICE:** We're still experimenting and trying to find the best developer
experience. The README will not necessarily reflect the current state of the
project as we have not implemented all of the features yet.

## Table of contents

* [Installation](#installation)
* [Background](#background)
* [Getting Started](#getting-started)
* [Services](#services)
  * [Stateless HTTP APIs](#stateless-http-apis)
  * [Static Websites](#static-websites)
* [Develop on hatch](#develop-on-hatch)

## Installation

The Hatch command line interface can be installed using [Homebrew][homebrew] if
you're on macOS

    brew tap mads-hartmann/hatch git@github.com:mads-hartmann/hatch.git
    brew install hatch

Otherwise you can use pip

    pip install hatch-cli

## Background

Amazon Web Services provides an overwhelming number of services and tools that
well help you build your products. These services are highly configurable and
can be shaped to your individual use-cases. This is very powerful but it comes
at a cost. Building simple products using AWS like a small API, a static
website, etc. usually requires the use of several different services and takes
a huge effort when it comes to configuration. We wanted to change that with
Hatch. By focusing on a few simple use-cases we've been able to automate the
entire creation and deployment for you so you can focus on building your
product.

## Getting Started

In order to use Hatch you need to have an [AWS][aws] account.

**TODO**: Finish guide on how to get your credentials and show an example
`~/.aws/config` file.

## Services

You can use Hatch to create various kinds of services on AWS. The following
section describes how to get started with each service.

### Stateless HTTP APIs

If you want to build a simple stateless API that can be reached over HTTP(s)
then this is for you. This is achieved using API Gateway, AWS Lambda, and
Route53.

To get started simply invoke

    hatch api create my-api

Now to play around with the service simply run

    cd api
    hatch api start

Once you're ready to publish your API you simply run

    hatch api deploy

### Static Websites

Hatch doesn't care if you're hand-writing your HTML or if you're using a build
tool like webpack. We just need the static files and we'll put them online. This
is achieved using S3, CloudFront and Route53.

Create your website

    hatch website create

If you want to test it out locally you can run

    hatch website start

When you're ready to publish it run

    hatch website deploy

### Cron jobs

**TODO**: I'm thinking AWS Lambda + something.

### Event handlers

**TODO**: AWS Lambda + something. This is just the generalized version of a cron job. Perhaps we shouldn't have two. 

## Develop on hatch

    git clone git@github.com:mads-hartmann/hatch.git && cd hatch
    make setup
    .venv/bin/hatch api deploy examples/api
    .venv/bin/hatch api start examples/api
    .venv/bin/hatch website deploy examples/website
    .venv/bin/hatch website start examples/website

### Project Overview

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

[aws]: https://aws.amazon.com/
[homebrew]: https://brew.sh
