from zope import interface
from zope import interface, schema

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator

from raptus.mailcone.persistentlog import _





class ILogContainer(IContainer):
    """ A container for persistentlog
    """


class ILogContainerLocator(IContainerLocator):
    """ interface for locate the persistentlog folder.
    """


class ILog(interface.Interface):
    """ A customer
    """
    id = schema.TextLine(title=_(u'Id'), required=True)
    category = schema.TextLine(title=_(u'Category'), required=True)
    log_from = schema.Datetime(title=_(u'Log from'), required=True)
    log_to = schema.Datetime(title=_(u'Log to'), required=True)
