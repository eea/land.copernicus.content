from land.copernicus.content.content.landfile import LandFileStore, PLandFile
from land.copernicus.content.content.api import LandFileApi


def test_api_add():
    store = LandFileStore()
    api = LandFileApi(store)

    landfile = api.add(title=u'A title', shortname='a-title')

    assert landfile.title == u'A title'
    assert landfile.shortname == 'a-title'

    assert api.get('A title') is not None
    assert api.get_by_shortname('a-title') is not None

    assert len([x for x in store.tree.keys()]) == 1
    assert len([x for x in store.ids.keys()]) == 1
