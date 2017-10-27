# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from rer.externalnews import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IRerExternalnewsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IExternalNews(Interface):
    """ Interfaccia per il content type: External News"""

    externalUrl = schema.TextLine(
        title=_(u'Link esterno ad una news'),
        description=_(u'Inserire un link valido ad una news esterna.'),
        default=u'https://',
        required=True,
    )

    externalSource = schema.TextLine(
        title=_(u'Da dove viene'),
        description=_(u'Inserire il nome del portale tematico da cui proviene la news.'),
        default=u'',
        required=False,
    )
