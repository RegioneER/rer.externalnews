# -*- coding: utf-8 -*-
from plone import api

import logging

logger = logging.getLogger(__name__)


default_profile = "profile-rer.externalnews:default"


def to_1100(context):
    """ """
    logger.info("Upgrading rer.externalnews to version 1100")
    context.runImportStepFromProfile(default_profile, "repositorytool")
    context.runImportStepFromProfile(default_profile, "difftool")
    context.runImportStepFromProfile(default_profile, "typeinfo", run_dependencies=True)


def to_1200(context):
    """ """
    logger.info("Upgrading rer.externalnews to version 1200")
    brains = api.content.find(portal_type="ExternalNews")
    tot = len(brains)
    i = 0
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info(f"Progress: {i}/{tot}")

        news = brain.getObject()
        news.reindexObject(idxs=["getRemoteUrl"])


def to_1300(context):
    """
    Convert old-style behavior names, keeping the original order.
    """
    mapping = {
        "plone.app.content.interfaces.INameFromTitle": "plone.namefromtitle",
        "plone.app.dexterity.behaviors.discussion.IAllowDiscussion": "plone.allowdiscussion",
        "plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation": "plone.excludefromnavigation",
        "plone.app.dexterity.behaviors.id.IShortName": "plone.shortname",
        "plone.app.dexterity.behaviors.metadata.IDublinCore": "plone.dublincore",
        "plone.app.relationfield.behavior.IRelatedItems": "plone.relateditems",
        "plone.app.versioningbehavior.behaviors.IVersionable": "plone.versioning",
        "plone.app.lockingbehavior.behaviors.ILocking": "plone.locking",
        "Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes": "plone.constraintypes",
    }

    portal_types = api.portal.get_tool(name="portal_types")
    for type_id in ["ExternalNews"]:
        fti = portal_types.get(type_id)
        if fti is None:
            continue
        old_behaviors = tuple(fti.behaviors)
        behaviors = []
        for behavior in old_behaviors:
            new_behavior = mapping.get(behavior, behavior)
            if new_behavior != behavior:
                logger.info(
                    f"[{type_id}] Replaced behavior {behavior} => {new_behavior}"
                )
            if new_behavior not in behaviors:
                behaviors.append(new_behavior)
        if tuple(behaviors) != old_behaviors:
            # _updateProperty also notifies the FTI modification (schema cache)
            fti._updateProperty("behaviors", tuple(behaviors))
