# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from redturtle.portlet.collection.rtcollectionportlet import (IRTCollectionPortletRenderer,
                                                              IRTCollectionPortletTemplate)
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapts
from zope.interface import implements


class BaseRenderer(object):
    adapts(IRTCollectionPortletRenderer)
    implements(IRTCollectionPortletTemplate)

    def __init__(self, base):
        self.request = base.request
        self.context = aq_inner(base.context)
        self.data = base.data
        self.results = base.results
        self.collection_url = base.collection_url
        self.collection = base.collection
        self.base = base

    def render(self, *args, **kwargs):
        return self._template(*args, **kwargs)


class DefaultRenderer(BaseRenderer):

    _human_readable_name = 'Default Renderer' 
    _template = ViewPageTemplateFile('templates/default_renderer.pt')
