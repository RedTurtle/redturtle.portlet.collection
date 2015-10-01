# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from Products.statusmessages.interfaces import IStatusMessage
from redturtle.portlet.collection import RTCollectionPortletMessageFactory as _
from redturtle.portlet.collection.interfaces import ICollectionTemplatesSettings
from z3c.form import button


class RedturtlePortletCollectionSettingsEditForm(controlpanel.RegistryEditForm):
    """Media settings form.
    """
    schema = ICollectionTemplatesSettings
    id = "RedTurtletPortletCollectionSettingsEditForm"
    label = _(u"Portlet Collection Templates settings")
    description = _(u"help_collection_templates_settings_editform",
                    default=u'Set a list of templates to use in "Collection portlet with custom view"')

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved"),
            "info")
        self.context.REQUEST.RESPONSE.redirect(
            "@@redturtle-portlet-collection-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class RedTurtlePortletCollectionSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Sitesearch settings control panel.
    """
    form = RedturtlePortletCollectionSettingsEditForm
