# coding=UTF-8
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
  -h --help         Show this help.
  --version         Show version.
  --config=<config> Path to config file.
  --silent          Don't output to stdout.
  --verbose         Output a lot to stdout.
"""

import logging
import os
import sys

import botocore.session
from docopt import docopt

from hatch.services.website import Website
from hatch.ux.website import serve_path
from hatch.version import VERSION

logger = logging.getLogger(__name__)

VERBOSE_LOG_FORMAT = '%(asctime)s %(name)-45s %(levelname)-8s %(message)s'


def get_config_path(path, arguments, file_name):
    config_path = arguments.get('--config') or path
    if os.path.isfile(config_path):
        return config_path
    return os.path.join(config_path, file_name)


def configuration_error(message):
    logger.error('Error %s', message)
    logger.error('Please ensure you\'ve configured AWS correctly')
    logger.error('See https://boto3.readthedocs.io/en/latest/guide/configuration.html')
    sys.exit(1)


def check_credentials():
    logger.debug('Checking credentials')
    try:
        session = botocore.session.get_session()
        credentials = session.get_credentials()
    except botocore.exceptions.ProfileNotFound:
        configuration_error('Unknown profile')

    if credentials is None:
        configuration_error('No AWS credentials')


def website_command(arguments):
    logger.debug('Running website command')
    path = arguments.get('<path>', './website')

    if not os.path.isdir(path):
        logger.error('No such directory: %s', path)
        sys.exit(1)

    config_path = get_config_path(path, arguments, 'website.yml')
    website = Website.create(path, config_path)

    if arguments.get('deploy'):
        website.deploy()
    elif arguments.get('start'):
        serve_path(path, 8000)


def api_command(arguments):
    logger.debug('Running API command')
    logger.info("👷‍♀️ Support for serverless APIs coming soon 🚧")


def configure_logging(verbose=False):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.CRITICAL,
        format=VERBOSE_LOG_FORMAT if verbose else '%(message)s'
    )
    logging.getLogger('hatch').setLevel(logging.INFO)


def run():
    arguments = docopt(__doc__, version='hatch {}'.format(VERSION))
    if not arguments.get('--silent'):
        configure_logging(verbose=arguments.get('--verbose'))

    logger.info('Hatching...')
    check_credentials()

    if arguments.get('api'):
        api_command(arguments)
    elif arguments.get('website'):
        website_command(arguments)


if __name__ == '__main__':
    run()
