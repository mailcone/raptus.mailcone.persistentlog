import grok

from zope import schema
from zope import component
from zope.annotation.interfaces import IAnnotations

from z3c.blobfile.file import File

from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone, ISearchable

from raptus.mailcone.persistentlog import interfaces



class Log(bases.Container):
    grok.implements(interfaces.ILog)



class LogContainer(bases.Container):
    grok.implements(interfaces.ILogContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_logs_container(obj, event):
    obj['cronjob_logs'] = LogContainer()

class LogContainerLocator(bases.BaseLocator):
    splitedpath = ['cronjob_logs']
grok.global_utility(LogContainerLocator, provides=interfaces.ILogContainerLocator)