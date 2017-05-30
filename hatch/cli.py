# pylint: disable=locally-disabled, C0103

"""
Hatch

hatch is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

Usage:
  hatch api start [--config-file] <path>
  hatch api deploy [--config-file] <path>
  hatch website deploy [--config-file] <path>
  hatch -h | --help
  hatch --version

Options:
  -h --help    Show this help.
  --version    Show version.
  --silent     Don't output to stdout.
"""

import os
import sys

import botocore.session
from docopt import docopt

from hatch.services.api import Api
from hatch.services.website import Website
from hatch.ux import server


def check_credentials():
    session = botocore.session.get_session()
    if session.get_credentials() is None:
        print 'You need to configure an AWS profile.'
        print 'See https://boto3.readthedocs.io/en/latest/guide/configuration.html'
        sys.exit(1)


def website_command(arguments):
    path = arguments.get('<path>', './website')
    config = arguments.get('[--config-file]', '{}/website.yml'.format(path))

    if not os.path.isdir(path):
        print 'No such directory: {}'.format(path)
        sys.exit(1)

    website = Website.create(path, config)

    if arguments.get('deploy'):
        website.deploy()
    else:
        print 'Meh.'


def api_command(arguments):
    api_path = arguments.get('<path>', './api')

    if not os.path.isdir(api_path):
        print '{} doesn\'t exist'.format(api_path)
        sys.exit(1)

    config_path = arguments.get(
        '[--config-file]',
        '{}/api.yml'.format(api_path))
    api = Api.create(api_path, config_path)

    if arguments.get('deploy'):
        api.deploy()

    elif arguments.get('start'):
        server.run(api, 8888)


def run():
    arguments = docopt(__doc__, version='hatch 0.1')
    check_credentials()

    if arguments.get('api'):
        api_command(arguments)
    elif arguments.get('website'):
        website_command(arguments)
    else:
        print 'Unknown command'


if __name__ == '__main__':
    run()
