# -*- coding: utf-8 -*-
from redturtle.portlet.collection import RTCollectionPortletMessageFactory as _
from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from plone.registry.field import PersistentField
from z3c.form.object import registerFactoryAdapter
from plone.formwidget.contenttree import UUIDSourceBinder
from plone.supermodel import model
from plone.directives import form
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree.widget import ContentTreeWidget
from plone.app.textfield.value import RichTextValue


class IRedTurtlePortletCollectionLayer(Interface):
    """
    Marker interface for browserlayer
    """


class ICollectionTemplatePersistentObject(Interface):
    pass


@implementer(ICollectionTemplatePersistentObject)
class CollectionTemplateEntryPersistentObject(PersistentField, schema.Object):
    pass


class ICollectionTemplateEntrySubitem(Interface):
    """Single entry for the collection templates configuration
    """

    template_id = schema.TextLine(
        title=_("template_id_label", u"Template id"),
        description=_('template_id_help',
                      default=u"Insert the id of the template."),
        default=u"",
        missing_value=u"",
        required=True,
    )
    template_title = schema.TextLine(
        title=_("template_title_label", u"Template title"),
        description=_('template_title_help',
                      default=u"Insert the title of the template that will be shown in the portlet configuration."),
        default=u"",
        missing_value=u"",
        required=True,
    )


@implementer(ICollectionTemplateEntrySubitem)
class CollectionTemplateEntrySubitem(object):
    """ """

registerFactoryAdapter(
    ICollectionTemplateEntrySubitem,
    CollectionTemplateEntrySubitem)


class ICollectionTemplatesSettings(Interface):
    """Settings used in the control panel
    """
    template = schema.Tuple(
        title=_('template_label', u'Collection template'),
        description=_(
            'template_collection_help',
            default=u"For collection template, provide a name and an id"),
        value_type=CollectionTemplateEntryPersistentObject(
            ICollectionTemplateEntrySubitem,
            title=_(u"Infos")),
        required=True,
        default=(),
        missing_value=(),
    )
