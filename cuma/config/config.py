#!/usr/bin/env python3

"""config.py: Read configuration."""

import os.path
#import ConfigParser as configparser
from cuma.config import Arguments
from cuma.logger import Logger

class Config(object):
    """Global configuration settings."""

    args = {}
    config = {}
    logger = {}

    def __init__(self):
        if not Config.config:
            Config.logger = Logger().get()
            Config.args = Arguments()
            Config.__set_config()

    @classmethod
    def __set_config(cls):
        Config.logger.info('initiating configuration')
        cls.config['path'] = os.path.join(os.environ.get('HOME'), 'devel', 'cuma-db')
        cls.config['file'] = 'cuma.db'

    @classmethod
    def get_storage_location(cls):
        return os.path.join(cls.config['path'], cls.config['file'])

