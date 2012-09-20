# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize.instance import memoize
from plone.portlet.collection.collection import \
    Assignment as BaseCollectionPortletAssignment, ICollectionPortlet, \
    Renderer as BaseCollectionPortletRenderer
from redturtle.portlet.collection import RTCollectionPortletMessageFactory as _
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter


class IRTCollectionPortlet(ICollectionPortlet):
    """The collection portlet that handle in a better way results view
    """

    link_text = schema.TextLine(title=_("custom_more_label",
                                        default=u'Custom "more..." label'),
                                description=_("custom_more_label_help",
                                              default=u'Fill this to show a different label for the "more..." link'),
                                required=False)

    target_more = schema.Choice(title=_("custom_more_target_label",
                                        default=u'Custom "more..." target'),
                                  description=_("custom_more_target_help",
                                                default=u'Select an object in the site, for the "more..." link. If empty, the link will be the collection.'),
                                  required=False,
                                  source=SearchableTextSourceBinder({'sort_on': 'getObjPositionInParent'}, default_query='path:'))

    no_elements_text = schema.TextLine(title=_("no_elements_text_label",
                                               default=u'Text on "no elements found"'),
                                               description=_("no_elements_text_label_help",
                                                             default=u'Render template can use this to show a custom text when no collection shows no elements.'),
                                               required=False)

    check_rss = schema.Bool(title=_("check_rss_label",
                                    default=u'Show RSS link'),
                            description=_("check_rss_label_help",
                                          default=u'Check this box to show the RSS link for the portlet. If you check this and the "more..." url isn\'t a collection, the RSS link will be broken.'),
                            required=False)

    css_class = schema.TextLine(title=_("css_class_label",
                                        default=u'Portlet\'s CSS class'),
                                  description=_("css_class_label_help",
                                                default=u'Fill this to  assign a CSS class to the portlet (for style purpose)'),
                                  required=False)

    div_id = schema.TextLine(title=_("div_id_label",
                                     default=u'Portlet\'s HTML id'),
                                description=_("div_id_label_help",
                                              default=u'Fill this to  assign an id to the portlet (for style purpose)'),
                                required=False)

    template_id = schema.TextLine(title=_("template_id_label",
                                          default=u'Template Id'),
                                  description=_("template_id_label_help",
                                                default=u"Id of a template to use, to render this collection\nAll other parameters here can or can't be used by the target template choosen"),
                                  default=u"base_collection_portlet_view",
                                  required=True)


class Assignment(BaseCollectionPortletAssignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IRTCollectionPortlet)

    link_text = u''
    check_rss = False
    link_value = u""
    div_id = ""
    template_id = 'base_collection_portlet_view'
    no_elements_text = ''
    css_class = ""
    target_more = None

    def __init__(self, header=u"", target_collection=None, limit=None, random=False, show_more=True, div_id="",
                 link_text=u'', link_value='', check_rss=False, show_dates=False,
                 template_id='base_collection_portlet_view', no_elements_text='', css_class="", target_more=None):
        BaseCollectionPortletAssignment.__init__(self, header=header, target_collection=target_collection, limit=limit, random=random, show_more=show_more, show_dates=show_dates)
        self.link_text = link_text
        self.check_rss = check_rss
        self.link_value = link_value
        self.div_id = div_id
        self.template_id = template_id
        self.no_elements_text = no_elements_text
        self.css_class = css_class
        self.target_more = target_more


class Renderer(BaseCollectionPortletRenderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    _template = ViewPageTemplateFile('rtcollectionportlet.pt')

    def __init__(self, *args):
        BaseCollectionPortletRenderer.__init__(self, *args)

    render = _template

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header

    @property
    def available(self):
        return len(self.results()) or self.data.no_elements_text

    def collection_url(self):
        if self.data.target_more:
            target = self.moreTarget()
            if target:
                return target.absolute_url()
        else:
            collection = self.collection()
            if collection:
                return collection.absolute_url()
        return None

    def rss_url(self):
        """
        Return the rss feed url from the collection
        """
        collection = self.collection()
        if collection:
            return "%s/RSS" % collection.absolute_url()
        return None

    @memoize
    def moreTarget(self):
        """ get the target custom for more... link"""

        target_path = self.data.target_more
        if not target_path:
            return None

        if target_path.startswith('/'):
            target_path = target_path[1:]

        if not target_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(target_path, default=None)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRTCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_more'].custom_widget = UberSelectionWidget

    label = _(u"Add Collection portlet with custom view")
    description = _(u"This portlet display a listing of items from a Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRTCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    form_fields['target_more'].custom_widget = UberSelectionWidget
    label = _(u"Edit Collection portlet with custom view")
    description = _(u"This portlet display a listing of items from a Collection.")
