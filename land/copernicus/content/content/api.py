import os
from hashlib import sha256
from urlparse import urlparse
from urllib import unquote

from land.copernicus.content.config import ENV_DL_SRC_PATH
from land.copernicus.content.content.landfile import PLandFile


def add_landfile(store, **props):
    landfile = PLandFile(**props)
    return store.add(landfile)


def add_landfile_with_filesize(store, **props):
    _fileSize = get_filesize(props['remoteUrl'])
    return add_landfile(store, _fileSize=_fileSize, **props)


def edit_landfile(store, old_title, **props):
    delete_landfile(store, old_title)
    return add_landfile(store, **props)


def edit_landfile_with_filesize(store, old_title, **props):
    # If we delete the landfile first and then call add_landfile_with_filesize
    # (like edit_landfile); in the event of get_filesize raising an error,
    # the entry will still get deleted and nothing will be added.
    # That is why the file size is fetched first.
    props['_fileSize'] = get_filesize(props['remoteUrl'])
    return edit_landfile(store, old_title, **props)


def delete_landfile(store, title):
    try:
        store.delete(title)
    except KeyError:
        raise KeyError('Land file with that title does not exist!')


def get_landfile(store, title):
    return store.get_by_title(title)


def get_landfile_by_shortname(store, shortname):
    return store.get_by_shortname(shortname)


def get_landfile_by_prop(store, name, value):
    for landfile in store.get_by_prop(name, value):
        yield landfile


def nice_sizeof(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def get_filesize(remoteUrl):
    extracted = unquote(urlparse(remoteUrl).path.strip('/'))
    path = os.path.join(ENV_DL_SRC_PATH, extracted)
    if os.path.isfile(path):
        return nice_sizeof(os.path.getsize(path))
    else:
        raise OSError('Provided URL does not resolve to a file!')


class LandFileApi(object):
    """ Exposing basic operations for LandFileStore.
        All edit operations are a combination of delete and add.
    """
    def __init__(self, store):
        self.store = store

    def add(self, **props):
        return add_landfile(self.store, **props)

    def add_with_filesize(self, **props):
        return add_landfile_with_filesize(self.store, **props)

    def edit(self, old_title, **props):
        return edit_landfile(self.store, old_title, **props)

    def edit_with_filesize(self, old_title, **props):
        return edit_landfile_with_filesize(self.store, old_title, **props)

    def delete(self, title):
        return delete_landfile(self.store, title)

    def get(self, title):
        return get_landfile(self.store, title)

    def get_by_shortname(self, shortname):
        return get_landfile_by_shortname(self.store, shortname)

    def get_by_prop(self, name, value):
        for landfile in get_landfile_by_prop(self.store, name, value):
            yield landfile

    @staticmethod
    def get_filesize_from_url(url):
        return get_filesize(url)
