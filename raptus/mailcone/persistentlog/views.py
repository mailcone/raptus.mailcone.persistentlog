import grok

from zope.component import getUtility
from zope.interface import alsoProvides
from zope.publisher.interfaces.http import IResult

from z3c.blobfile.browser.file import FileView

from raptus.mailcone.layout.interfaces import ICronjobMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import Page

from raptus.mailcone.core import utils

from raptus.mailcone.persistentlog import _
from raptus.mailcone.persistentlog import interfaces
from raptus.mailcone.persistentlog import contents

grok.templatedir('templates')






class PersistentTable(BaseDataTable):
    grok.context(interfaces.ILogContainer)
    interface_fields = interfaces.ILog
    ignors_fields = ['id', 'has_errors']
    actions = (dict( title = _('delete'),
                     cssclass = 'ui-icon ui-icon-trash ui-modal-minsize ui-datatable-ajaxlink',
                     link = 'deletecustomerform'),
               dict( title = _('download'),
                     cssclass = 'ui-icon ui-icon-arrowthickstop-1-s',
                     link = 'download'),)

    def _metadata(self, objs):
        di = super(PersistentTable, self)._metadata(objs)
        
        css_class = dict()
        for index, obj in enumerate(objs):
            css_class[index] = obj.has_errors and 'table-color-red' or ' '
        di['css_class'] = css_class
        return di



class PersistentLogs(Page):
    grok.name('index')
    grok.context(interfaces.ILogContainer)
    locatormenuitem(ICronjobMenu, interfaces.ILogContainerLocator, _(u'Logs'))
    
    @property
    def logtable(self):
        return PersistentTable(self.context, self.request).html()



class LogView(grok.View, FileView):
    grok.name('index')
    grok.context(interfaces.ILog)

    @property
    def content(self):
        file = self.show()
        del self.request.response._headers['content-type']
        return file.__iter__()



class Download(grok.View, FileView):
    grok.name('download')
    grok.context(interfaces.ILog)
    
    def render(self):
        file = self.show()
        filename = self.context.log_to.strftime('%s-%%d.%%m.%%y.log' % self.context.category)
        self.request.response.setHeader('Content-Type', 'text/csv; charset=utf-8')
        self.request.response.setHeader('Accept-Charset', 'utf-8')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename=%s' % filename)
        alsoProvides(file, IResult)
        return file





