# coding=UTF-8
# pylint: disable=locally-disabled, C0103

"""
Hatch

Hatch makes it easy to manage your static websites on AWS - Hatch takes cares
of creating S3 buckets and configuring your custom domains in Route53 - All
from the comforts of your command line.

Usage:
  hatch [options]
  hatch [options] website start
  hatch [options] website deploy [--path=<path>] [--domain=<domain>] [--name=<name>]

Options:
  -h --help            Show this help.
  --version            Show version.
  --silent             Don't output to stdout.
  --verbose            Output a lot to stdout.
  --config-file <path> Path to configuration file [default: website.yml]
"""

import logging
import os
import sys

import botocore.session
from docopt import docopt

from hatch.services.website import Website
from hatch.ux.website import serve_path
from hatch.version import VERSION
from hatch.config import WebsiteConfig

logger = logging.getLogger(__name__)

VERBOSE_LOG_FORMAT = '%(asctime)s %(name)-45s %(levelname)-8s %(message)s'


def get_config_path(path, arguments, file_name):
    config_path = arguments.get('--config-file') or path
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

    config_path = arguments.get('--config-file')
    name = arguments.get('--name')
    domain = arguments.get('--domain')
    path = arguments.get('--path')
    region = arguments.get('--region')

    file_config = None
    if config_path is None and os.path.isfile('website.yml'):
        file_config = WebsiteConfig.parse('website.yml')
    elif config_path is not None:
        file_config = WebsiteConfig.parse(config_path)

    arguments_config = WebsiteConfig(path, name, region, domain)
    config = arguments_config.merge(file_config).merge(WebsiteConfig.defaults())

    if not os.path.isdir(config.path):
        logger.error('No such directory: %s', path)
        sys.exit(1)

    website = Website.create(config)

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

    if arguments.get('api') is None and arguments.get('website') is None:
        logger.info('use hatch -h for help')
        sys.exit(0)

    if arguments.get('api'):
        api_command(arguments)
    elif arguments.get('website'):
        logger.info('Hatching...')
        check_credentials()
        website_command(arguments)


if __name__ == '__main__':
    run()
