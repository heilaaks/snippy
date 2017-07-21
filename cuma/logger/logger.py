#!/usr/bin/env python3

"""logger.py: Common logger for the tool."""

import logging


class Logger(object):
    """Logger wrapper."""

    def __init__(self):
        self.logger = logging.getLogger('root')
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(filename)-12s : %(message)s'
        logging.basicConfig(level='DEBUG', format=log_format)
        self.logger = logging

    def get(self):
        return self.logger


class LoggerWrapper(logging.Logger):
    """TODO: Logger wrapper experimental to try to get LoggerWrapper.debug("to work")."""

    def __init__(self, name="custom_logger", level=logging.DEBUG):
    #def __init__(self, name="custom_logger", *args, **kwargs  ):
        #super(Logger, self).__init__(__name__)
        #super(Logger, self).__init__()
        #logging.Logger.__init__(self, __name__, level)
        #super(Logger, self).__init__(logger, {})
        #super(Logger, self).__init__(name, level)
        #super(LoggerWrapper, self).__init__(name, level)
        #super(LoggerWrapper, self)
        #logging.setLoggerClass(Logger)
        
        #super(LoggerWrapper, self).__init__(name, level)
        #super(LoggerWrapper, self).__init__(name, level)
        self.filename = __name__
        self.logger = logging.getLogger(name)
        log_format = '%(asctime)s %(process)d[%(lineno)04d] <%(levelno)s>: %(threadName)s@%(self.filename)-12s : %(message)s'
        logging.basicConfig(level='DEBUG', format=log_format)
        self.logger = logging

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        return super(LoggerWrapper, cls).debug(cls, msg)

    #@classmethod
    def warn(self, msg, *args, **kwargs):
        print("warning (%s)" % msg)
        import inspect
        frm = inspect.stack()[1]
        print(frm)
        print(frm.filename)
        self.filename = frm.filename
        self.logger.warn(msg)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    #def debug(self, msg, extra=None):
    #    import inspect
    #    frm = inspect.stack()[1]
    #    print(frm)
    #    self.logger.debug(msg, extra=extra)

    #def warn(self, msg, extra=None):
    #    self.logger.warn(msg, extra=extra)