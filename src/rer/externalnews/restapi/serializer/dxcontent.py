from rer.externalnews.interfaces import IExternalNews
from plone.restapi.interfaces import IObjectPrimaryFieldTarget
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(IExternalNews, Interface)
@implementer(IObjectPrimaryFieldTarget)
class ExternalNewsObjectPrimaryFieldTarget:
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.permission_cache = {}

    def __call__(self):
        """
        If user can edit Link object, do not return remoteUrl
        """
        pm = getToolByName(self.context, "portal_membership")
        if bool(pm.isAnonymousUser()):
            return getattr(self.context, "externalUrl", "")
