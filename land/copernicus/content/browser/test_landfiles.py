from Products.Five.browser import BrowserView
from land.copernicus.content.content.api import LandFileApi
import logging
import plone.api as api

logger = logging.getLogger('land.copernicus.content')


class TestAllLandFilesView(BrowserView):
    """ Administration view for testing land files
    """

    def items(self):
        landitems = api.content.find(portal_type='LandItem')

        msgs = []

        for item in landitems:
            landitem = item.getObject()
            landfiles = [x for x in landitem.landfiles.get_all()]
            for landfile in landfiles:
                lfa = LandFileApi(landitem.landfiles)
                orig = lfa.get_by_shortname(landfile.shortname)

                props = dict(
                    title=orig.title,
                    description=orig.description,
                    remoteUrl=orig.remoteUrl,
                    fileCategories=orig.fileCategories
                )

                try:
                    landfile = lfa.edit_with_filesize(orig.title, **props)

                    msgs.append([
                        landitem.absolute_url(),
                        landfile.shortname,
                        u'OK'
                        ])
                except (KeyError, OSError) as err:
                    msgs.append([
                        landitem.absolute_url(),
                        landfile.shortname,
                        err
                        ])
                    logger.info(
                        "ERROR landfile: {0}: {1} - {2}".format(
                            landitem.absolute_url(),
                            landfile.shortname,
                            err))

        return msgs
