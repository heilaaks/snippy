#!/usr/bin/env python3

"""arguments.py: Command line arguments"""

#import argparse
from cuma.logger import Logger

class Arguments(object):

    args = {}

    def __init__(self):
        self.logger = Logger().get()

    @classmethod
    def get(self):
        self.logger.info('reading command line arguments')
