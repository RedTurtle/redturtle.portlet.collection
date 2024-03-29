# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlet.collection.collection import \
    Assignment as BaseCollectionPortletAssignment, ICollectionPortlet, \
    Renderer as BaseCollectionPortletRenderer
from redturtle.portlet.collection import RTCollectionPortletMessageFactory as _
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implementer

from plone import api

class IRTCollectionPortlet(ICollectionPortlet):
    """The collection portlet that handle in a better way results view
    """
    image_ref = schema.Choice(
        title=_(u"Background image"),
        description=_(
            u"Insert an image that will be shown as background"
            u"under the header"),
        required=False,
        source=CatalogSource(portal_type='Image')
    )

    link_text = schema.TextLine(
        title=_("custom_more_label", default=u'Custom "more..." label'),
        description=_(
            "custom_more_label_help",
            default=u'Fill this to show a different"\
                    " label for the "more..." link'),
        required=False
    )

    target_more = schema.Choice(
        title=_(
            "custom_more_target_label",
            default=u'Custom "more..." target'),
        description=_(
            "custom_more_target_help",
            default=u'Select an object in the site, for the "more..." link.'
                    u' If empty, the link will be the collection.'),
        required=False,
        source=CatalogSource()
    )

    start_from = schema.Int(
        title=_("start_from_label", default=u'Number of element to skip'),
        default=0,
        required=False
    )

    no_elements_text = schema.TextLine(
        title=_(
            "no_elements_text_label",
            default=u'Text on "no elements found"'),
        description=_(
            "no_elements_text_label_help",
            default=u'Render template can use this to show a custom text when'
                    u' no collection shows no elements.'),
        required=False
    )

    check_rss = schema.Bool(
        title=_("check_rss_label", default=u'Show RSS link'),
        description=_(
            "check_rss_label_help",
            default=u'Check this box to show the RSS link for the portlet.'
                    u' If you check this and the "more..." url isn\'t a'
                    u' collection, the RSS link will be broken.'),
            required=False
        )

    css_class = schema.TextLine(
        title=_("css_class_label", default=u'Portlet\'s CSS class'),
        description=_(
            "css_class_label_help",
            default=u'Fill this to  assign a CSS class to the portlet'
                    u' (for style purpose)'),
        required=False)

    div_id = schema.TextLine(
        title=_("div_id_label", default=u'Portlet\'s HTML id'),
        description=_(
            "div_id_label_help",
            default=u'Fill this to assign an id to the portlet'
                    u' (for style purpose)'),
        required=False)

    template_id = schema.TextLine(
        title=_("template_id_label", default=u'Template Id'),
        description=_(
            "template_id_label_help",
            default=u"Id of a template to use, to render this collection\n"
                    u"All other parameters here can or can't be used by the"
                    u" target template choosen"),
        default=u"base_collection_portlet_view",
        required=True)


@implementer(IRTCollectionPortlet)
class Assignment(BaseCollectionPortletAssignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    image_ref = None
    link_text = u''
    check_rss = False
    link_value = u""
    div_id = ""
    template_id = 'base_collection_portlet_view'
    no_elements_text = ''
    css_class = ""
    target_more = None
    start_from = 0

    def __init__(self, header=u"", uid=None, limit=None,
                 random=False, show_more=True, show_dates=False,
                 no_icons=False, no_thumbs=False,
                 thumb_scale=None, div_id="", image_ref=None, link_text=u'',
                 link_value='', check_rss=False,
                 template_id='base_collection_portlet_view',
                 no_elements_text='', css_class="", target_more=None,
                 start_from=0, exclude_context=True):

        try:
            BaseCollectionPortletAssignment.__init__(
                self,
                header=header,
                uid=uid,
                limit=limit, random=random,
                show_more=show_more,
                show_dates=show_dates,
                exclude_context=exclude_context,
                no_icons=no_icons,
                no_thumbs=no_thumbs,
                thumb_scale=thumb_scale)
        except TypeError:
            # Lord of Immortals, forgive me for that ugliness but
            # plone.portlet.collection 2.1.6 forced me to do this
            BaseCollectionPortletAssignment.__init__(
                self,
                header=header,
                uid=uid,
                limit=limit, random=random,
                show_more=show_more,
                show_dates=show_dates)

        self.image_ref = image_ref
        self.link_text = link_text
        self.check_rss = check_rss
        self.link_value = link_value
        self.div_id = div_id
        self.template_id = template_id
        self.no_elements_text = no_elements_text
        self.css_class = css_class
        self.target_more = target_more
        self.start_from = start_from


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

    def results(self):
        start_from = getattr(self.data, 'start_from', 0)
        return super(Renderer, self).results()[start_from:]

    def get_image_src(self):
        #target = self.get_image_path()
        target = api.content.get(UID=self.data.image_ref)
        # this approach is better if you need to use diazo and replace
        # 'image_preview' with some other scale
        if target:
            # https://docs.plone.org/develop/plone/images/content.html
            return target.absolute_url() + '/@@images/image/mini'
        else:
            return ''
        # If you want use images view....
        # scales = getMultiAdapter((target, self.request), name="images")
        # return scales.tag('image', scale='preview')

    def get_image_path(self):
        # redundant/obsolete code!
        #target_path = self.data.image_ref
        img = api.content.get(UID=self.data.image_ref)
        if img:
            target_path = img.absolute_url(1)
        else:
            target_path = ''

        if not target_path:
            return None

        if target_path.startswith('/'):
            target_path = target_path[1:]

        if not target_path:
            return None

        portal = api.portal.get()
        return portal.restrictedTraverse(target_path, default=None)

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

        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(target_path, default=None)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    schema = IRTCollectionPortlet

    label = _(u"Add Collection portlet with custom view")
    description = _(
        u"This portlet display a listing of items from a Collection."
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    schema = IRTCollectionPortlet

    label = _(u"Edit Collection portlet with custom view")
    description = _(
        u"This portlet display a listing of items from a Collection."
    )
