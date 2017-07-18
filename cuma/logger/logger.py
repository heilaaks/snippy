#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

import logging

class Logger(object):

    def __init__(self):
        self.logger = logging.getLogger('root')
        #log_format = '%(asctime)s %(process)d%(thread)d@%(filename)-18s:%(lineno)4s %(levelno)s: %(message)s'
        
        # 2017-07-19 00:05:30,026 8895140234446157568@database.py       :  15 10: initiating database into /home/heilaaks/devel/cuma-db/cuma.db
        # 2017-07-19 00:05:30,026 %(host)s %(process)d[%(lineno)4s] <>: %(thread)d@ 8895140234446157568@database.py - initiating database into /home/heilaaks/devel/cuma-db/cuma.db
        
        #Jul 18 23:35:51 localhost.localdomain plasmashell[1650]: QXcbConnection: XCB error: 2 (BadValue),
        
        #log_format = '%(asctime)s %(host)s %(process)d[%(lineno)4s] <%(levelname)d>: %(thread)d@%(filename)-18s: %(message)s'
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-11s : %(message)s'
        logging.basicConfig(level='DEBUG', format=log_format)
        self.logger = logging

        #self.logger = logging.getLogger('root')
        #FORMAT = '%(asctime)s %(process)d%(thread)d@%(filename)-18s:%(lineno)4s %(levelno)s: %(message)s'
        #logging.basicConfig(format=FORMAT)
        #self.logger.setLevel(logging.DEBUG)

    def get(self):
        return self.logger

