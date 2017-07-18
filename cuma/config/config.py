#!/usr/bin/env python3

"""config.py: Read configuration."""

import os.path
#import ConfigParser as configparser
from cuma.config import arguments

class Config(object):
    """Global configuration settings."""

    config = {}

    def __init__(self):
        print("init")
        Config.set_config()

    @classmethod
    def set_config(cls):
        print("set config")
        cls.config['path'] = os.path.join(os.environ.get('HOME'), 'devel', 'cuma-db')
        cls.config['file'] = 'cuma.db'

    @classmethod
    def get_storage_location(cls):
        return os.path.join(cls.config['path'], cls.config['file'])

