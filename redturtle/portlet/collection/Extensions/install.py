# -*- coding: utf-8 -*-

def uninstall(portal, reinstall=False):
    setup_tool = portal.portal_setup
    setup_tool.runAllImportStepsFromProfile('profile-redturtle.portlet.collection:uninstall')
