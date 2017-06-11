# pylint: disable=locally-disabled, C0103

"""
Hatch

hatch is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

Usage:
  hatch api start [options] <path>
  hatch api deploy [options] <path>
  hatch website start [options] <path>
  hatch website deploy [options] <path>
  hatch -h | --help
  hatch --version

Options:
  -h --help      Show this help.
  --version      Show version.
  --config-file  Path to config file.
  --silent       Don't output to stdout.
  --verbose      Output a lot to stdout.
"""

import logging
import os
import sys

import botocore.session
from docopt import docopt

from hatch.services.api import Api
from hatch.services.website import Website
from hatch.ux.server import run_lambda
from hatch.ux.website import serve_path
from hatch.version import VERSION

logger = logging.getLogger(__name__)


def configuration_error(message):
    logger.error('Error %s', message)
    logger.error('Please ensure you\'ve configured AWS correctly')
    logger.error('See https://boto3.readthedocs.io/en/latest/guide/configuration.html')
    sys.exit(1)


def check_credentials():
    try:
        session = botocore.session.get_session()
        credentials = session.get_credentials()
    except botocore.exceptions.ProfileNotFound:
        configuration_error('Unknown profile')

    if credentials is None:
        configuration_error('No AWS credentials')


def website_command(arguments):
    path = arguments.get('<path>', './website')
    config = arguments.get('[--config-file]', '{}/website.yml'.format(path))

    if not os.path.isdir(path):
        logger.error('No such directory: %s', path)
        sys.exit(1)

    website = Website.create(path, config)

    if arguments.get('deploy'):
        website.deploy()
    elif arguments.get('start'):
        serve_path(path, 8000)


def api_command(arguments):
    api_path = arguments.get('<path>', './api')

    if not os.path.isdir(api_path):
        logger.error('No such directory: %s', api_path)
        sys.exit(1)

    config_path = arguments.get(
        '[--config-file]',
        '{}/api.yml'.format(api_path))
    api = Api.create(api_path, config_path)

    if arguments.get('deploy'):
        api.deploy()
    elif arguments.get('start'):
        run_lambda(api, 8888)


def configure_logging(verbose=False):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.CRITICAL,
        format=logging.BASIC_FORMAT if verbose else '%(message)s'
    )
    logging.getLogger('hatch').setLevel(logging.DEBUG)


def run():
    arguments = docopt(__doc__, version='hatch {}'.format(VERSION))
    if not arguments.get('--silent'):
        configure_logging(verbose=arguments.get('--verbose'))

    check_credentials()

    if arguments.get('api'):
        api_command(arguments)
    elif arguments.get('website'):
        website_command(arguments)


if __name__ == '__main__':
    run()
