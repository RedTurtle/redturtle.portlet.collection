# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

default_profile = 'profile-redturtle.portlet.collection:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('redturtle.portlet.collection', '0.4')
def to_0_4(context):
    """
    """
    context.runImportStepFromProfile(default_profile, 'rolemap')

@upgrade('redturtle.portlet.collection', '0.5')
def to_0_5(context):
    """
    """
    context.runImportStepFromProfile(default_profile, 'portlets')
