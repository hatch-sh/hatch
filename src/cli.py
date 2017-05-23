# pylint: disable=locally-disabled, C0103

"""
Easy AWS

awseasy is a tool that makes it easy to build products using AWS. It uses
conventions to automate the creation of things like static website,
HTTP API's etc. quick and easy.

Usage:
  easyaws api start [--config-file] <path>
  easyaws api deploy [--config-file] <path>
  easyaws website deploy <path>
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

from services.api import Api
from ux import server

if __name__ == '__main__':
    arguments = docopt(__doc__, version='awseasy 0.1')

    if arguments.get('api'):
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

    elif arguments['website']:
        pass
