# pylint: disable=locally-disabled, C0103

"""
Easy AWS

awseasy is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

Usage:
  easyaws api start [--config-file] <path>
  easyaws api deploy [--config-file] <path>
  easyaws website deploy [--config-file] <path>
  easyaws -h | --help
  easyaws --version

Options:
  -h --help    Show this help.
  --version    Show version.
  --silent     Don't output to stdout.
"""

import os
import sys

from docopt import docopt

from easyaws.services.api import Api
from easyaws.services.website import Website
from easyaws.ux import server


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

    config_path = arguments.get('[--config-file]', '{}/api.yml'.format(api_path))
    api = Api.create(api_path, config_path)

    if arguments.get('deploy'):
        api.deploy()

    elif arguments.get('start'):
        server.run(api, 8888)


def run():
    arguments = docopt(__doc__, version='awseasy 0.1')

    if arguments.get('api'):
        api_command(arguments)
    elif arguments.get('website'):
        website_command(arguments)
    else:
        print 'Unknown command'


if __name__ == '__main__':
    run()
