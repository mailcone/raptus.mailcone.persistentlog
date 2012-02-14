import os
import grok
import json
import copy

from grokcore.view.interfaces import ITemplateFileFactory

from megrok import navigation

from zope.component import getUtility
from zope.formlib import form

from raptus.mailcone.layout.interfaces import ICronjobMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.datatable import BaseDataTable
from raptus.mailcone.layout.views import Page

from raptus.mailcone.core import utils

from raptus.mailcone.rules.interfaces import IRuleset, IRuleItem
from raptus.mailcone.rules.wireit import IdentifierMixing

from raptus.mailcone.persistentlog import _
from raptus.mailcone.persistentlog import interfaces
from raptus.mailcone.persistentlog import contents

grok.templatedir('templates')






class PersistentTable(BaseDataTable):
    grok.context(interfaces.ILogContainer)
    interface_fields = interfaces.ILog
    ignors_fields = ['id']
    actions = (dict( title = _('delete'),
                     cssclass = 'ui-icon ui-icon-trash ui-modal-minsize ui-datatable-ajaxlink',
                     link = 'deletecustomerform'),
               dict( title = _('download'),
                     cssclass = 'ui-icon ui-icon-pencil ui-datatable-ajaxlink',
                     link = 'download'),)



class PersistentLogs(Page):
    grok.name('index')
    grok.context(interfaces.ILogContainer)
    locatormenuitem(ICronjobMenu, interfaces.ILogContainerLocator, _(u'Logs'))
    
    @property
    def logtable(self):
        return PersistentTable(self.context, self.request).html()
    





