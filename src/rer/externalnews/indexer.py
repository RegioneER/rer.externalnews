# -*- coding: utf-8 -*-
from rer.externalnews.interfaces import IExternalNews
from plone.indexer.decorator import indexer


@indexer(IExternalNews)
def getRemoteUrl(obj):
    return getattr(obj, "externalUrl", "")
