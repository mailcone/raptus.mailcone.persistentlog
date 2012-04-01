import logging
import pytz

from logging import handlers
from StringIO import StringIO
from datetime import datetime

from zope import component

from raptus.mailcone.persistentlog.contents import Log





class PersistentLogHandler(handlers.BufferingHandler):
    
    has_errors = False
    firstlog = None
    
    def __init__(self, category, locator):
        super(PersistentLogHandler, self).__init__(1000000000)
        self.category = category
        self.locator = locator
    
    def emit(self, record):
        super(PersistentLogHandler, self).emit(record)
        if record.levelno >= logging.ERROR:
            self.has_errors = True
        if self.firstlog is None:
            self.firstlog = self.now()

    def getLog(self):
        content = StringIO()
        for log in self.buffer:
            content.write('%s\n' % self.format(log))
        return content.getvalue()

    def persist(self):
        container = component.getUtility(self.locator)()
        log = Log()
        if self.firstlog is None:
            self.firstlog = self.now()
        log.log_from = self.firstlog
        log.log_to = self.now()
        log.category = self.category
        log.data = self.getLog()
        log.has_errors = self.has_errors
        container.add_object(log)
        self.flush()

    def flush(self):
        super(PersistentLogHandler, self).flush()
        self.firstlog = None
        self.has_errors = False

    def now(self):
        dt = datetime.now()
        return datetime(dt.year,dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo=pytz.UTC)



