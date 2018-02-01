from time import time
import os
import pytest
import string
import random

from land.copernicus.content.content.landfile import LandFileStore
from land.copernicus.content.content.api import LandFileApi

from land.copernicus.content.config import ENV_DL_SRC_PATH

try:
    os.makedirs(ENV_DL_SRC_PATH)
except OSError:
    pass


def make_random_string(size):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))


def add_testfile(name, size):
    path_testfile = os.path.join(ENV_DL_SRC_PATH, name)
    with open(path_testfile, 'w') as testfile:
        testfile.write(make_random_string(size))


def test_api_add():
    store = LandFileStore()
    api = LandFileApi(store)

    landfile = api.add(
        title=u'A title',
        shortname='a-title',
        description='desc'
    )

    assert landfile.title == u'A title'
    assert landfile.shortname == 'a-title'

    by_title = api.get('A title')
    by_shortname = api.get_by_shortname('a-title')
    by_prop = next(api.get_by_prop('description', 'desc'))

    assert by_title is not None
    assert by_shortname is not None
    assert by_prop is not None

    assert by_title is by_shortname is by_prop

    assert len([x for x in store.tree.keys()]) == 1
    assert len([x for x in store.ids.keys()]) == 1

    with pytest.raises(KeyError):
        api.add(title='A title', shortname='a-title')

    with pytest.raises(KeyError):
        api.add(title='Another title', shortname='a-title')


def test_api_edit():
    store = LandFileStore()
    api = LandFileApi(store)

    api.add(title=u'A title', shortname='a-title')
    api.edit('A title', title='A changed title', shortname='a-changed-title')

    assert api.get('A title') is None

    assert api.get('A changed title') is not None
    assert api.get_by_shortname('a-changed-title') is not None

    assert len([x for x in store.tree.keys()]) == 1
    assert len([x for x in store.ids.keys()]) == 1

    with pytest.raises(KeyError):
        api.edit('A title', title='Something else', shortname='a-title')


def test_api_delete():
    store = LandFileStore()
    api = LandFileApi(store)

    api.add(title=u'A title', shortname='a-title')
    assert api.get('A title') is not None

    api.delete('A title')
    assert api.get('A title') is None

    assert len([x for x in store.tree.keys()]) == 0
    assert len([x for x in store.ids.keys()]) == 0


def test_api_add_edit_with_filesize():
    store = LandFileStore()
    api = LandFileApi(store)

    add_testfile('testfile0', 1000)
    add_testfile('testfile1', 2000)

    landfile0 = api.add_with_filesize(
        title=u'A title',
        shortname='a-title',
        remoteUrl='http://localhost/testfile0'
    )

    landfile0_filesize = landfile0.fileSize
    assert landfile0_filesize and landfile0_filesize != 'N/A'

    landfile1 = api.edit_with_filesize(
        'A title',
        title='A title',
        shortname='a-title',
        remoteUrl='http://localhost/testfile1'
    )

    landfile1_filesize = landfile1.fileSize
    assert landfile1_filesize and landfile1_filesize != 'N/A'

    assert landfile0_filesize != landfile1_filesize

    with pytest.raises(OSError):
        api.add_with_filesize(
            title=u'A missing landfile',
            shortname='a-missing-landfile',
            remoteUrl='http://localhost/testfile_missing'
        )


def test_performance():
    store = LandFileStore()
    api = LandFileApi(store)

    t0 = time()
    for num in range(1, 100001):
        title = str(num)
        api.add(title=title, shortname=title)

    tf0 = time() - t0
    assert tf0 < 3

    t00 = time()
    for num in range(1, 100001):
        title = str(num)
        api.delete(title=title)

    tf1 = time() - t00
    assert tf1 < 1
