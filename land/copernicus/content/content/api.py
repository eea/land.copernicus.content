import os
from urlparse import urlparse
from urllib import unquote

from land.copernicus.content.config import ENV_DL_SRC_PATH
from land.copernicus.content.content.landfile import PLandFile


def add_landfile(tree, **props):
    landfile = PLandFile(**props)
    title = landfile.title
    if tree.has_key(title): # NOQA 'in' is slower for BTree
        raise KeyError('Land file with same title exists!')
    else:
        tree[title] = landfile
    return landfile


def edit_landfile(tree, **props):
    delete_landfile(tree, props['title'])
    return add_landfile(tree, **props)


def delete_landfile(tree, title):
    try:
        del tree[title]
    except KeyError:
        raise KeyError('Land file with that title does not exist!')


def get_landfile(tree, title):
    return tree.get(title)


def get_landfile_by_prop(tree, name, value):
    for landfile in tree.values():
        if getattr(landfile, name) == value:
            yield landfile


def nice_sizeof(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def get_filesize(remoteUrl):
    try:
        extracted = unquote(urlparse(remoteUrl).path.strip('/'))
        path = os.path.join(ENV_DL_SRC_PATH, extracted)
        return nice_sizeof(os.path.getsize(path))
    except OSError:
        raise OSError('{} does not exist!'.format(extracted))


class LandFileApi(object):
    def __init__(self, tree):
        self.tree = tree

    def add(self, **props):
        return add_landfile(self.tree, **props)

    def edit(self, **props):
        return edit_landfile(self.tree, **props)

    def delete(self, title):
        return delete_landfile(self.tree, title)

    def get(self, title):
        return get_landfile(self.tree, title)

    def get_by_prop(self, name, value):
        for landfile in get_landfile_by_prop(self.tree, name, value):
            yield landfile

    @staticmethod
    def get_filesize_from_url(url):
        return get_filesize(url)
