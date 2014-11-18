# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from redturtle.portlet.collection.rtcollectionportlet import IAdvancedRTCollectionPortletRenderer
from redturtle.portlet.collection.rtcollectionportlet import IAdvancedRTCollectionSmartRenderer
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapts
from zope.component._api import getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.interface import implements


class getRtpcConfiguration(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, view_name, kwargs={}):
        if not view_name:
            return ''
        try:
            view = getMultiAdapter((self.context, self.request), name=view_name)
            return view(**kwargs)
        except ComponentLookupError:
            return ''


class BaseRenderer(object):
    adapts(IAdvancedRTCollectionSmartRenderer)
    implements(IAdvancedRTCollectionPortletRenderer)

    def __init__(self, base):
        self.request = base.request
        self.context = aq_inner(base.context)
        self.data = base.data
        self.results = base.results
        self.collection_url = base.collection_url
        self.collection = base.collection
        self.base = base
        self._standard_results = base._standard_results

    def render(self, *args, **kwargs):
        return self._template(*args, **kwargs)

    def tag(self, obj, scale='tile', css_class='tileImage'):
        context = aq_inner(obj)
        # test for leadImage and normal image
        for fieldname in ['leadImage', 'image']:
            field = context.getField(fieldname)
            if field is not None:
                if field.get_size(context) != 0:
                    return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def see_more_label(self):
        return _("see_more_label", default="Show more")

    def have_results(self):
        return bool(self.results())


class NewsRenderer(BaseRenderer):
    __name__ = 'Notizie'
    _template = ViewPageTemplateFile('templates/news_renderer.pt')


class DefaultRenderer(BaseRenderer):
    __name__ = 'Template di default'
    _template = ViewPageTemplateFile('templates/default_renderer.pt')
