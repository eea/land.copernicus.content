import json
from StringIO import StringIO

import pytest

from plone.i18n.normalizer.tests import base as i18n_base

from land.copernicus.content.browser.views import AdminLandFilesView
from land.copernicus.content.content.landfile import LandFileStore
from land.copernicus.content.content.api import LandFileApi

from utils import make_temp_dir
from utils import add_testfile
from utils import rm_testfile


make_temp_dir()


class Context(object):
    landfiles = None

    def __init__(self):
        self.landfiles = LandFileStore()
        self.fileCategories = ['Type', 'Country']


class Request(object):
    form = None

    def __init__(self, form):
        self.form = form


class MockAdmin(AdminLandFilesView):

    def render(self):
        return json.loads(self.output_json)

    def show_error(self, *a, **kw):
        print(a, kw)

    show_info = show_error


TPL_POST = """
Title {nr}
Description {nr}
http://localhost/testfile{nr}
(Type, Vector), (Country, Romania)
""".strip()

TPL_PUT = """
Title {nr}
Description modified {nr}
http://localhost/testfile{nr}
(Type, Vector), (Country, Romania)
""".strip()


FILE_ALL = 'all'
FILE_POST = '\n'.join(TPL_POST.format(nr=nr) for nr in range(10))
FILE_PUT = '\n'.join(TPL_PUT.format(nr=nr) for nr in range(10))
FILE_GET_DEL_135 = '\n'.join('Title {}'.format(nr) for nr in [1, 3, 5])


NAMES_TESTFILES = ['testfile{}'.format(nr) for nr in range(10)]


@pytest.fixture(scope='module')
def testfiles():
    for idx, filename in enumerate(NAMES_TESTFILES, start=1):
        add_testfile(filename, idx)

    yield None

    for filename in NAMES_TESTFILES:
        rm_testfile(filename)


@pytest.fixture(scope='module')
def context():
    return Context()


@pytest.fixture(scope='session')
def normalizer():
    i18n_base.setUp()
    yield None
    i18n_base.tearDown()


def file_from_template(contents, filename):
    _file = StringIO(contents)
    _file.filename = filename
    return _file


def test_admin_POST(context, testfiles, normalizer):
    _file = file_from_template(FILE_POST, 'import')

    form = dict(
        file=_file,
        inlineRadioOptions='post',
        submit='submit'
    )

    request = Request(form=form)
    admin = MockAdmin(context, request)
    result = admin()

    expect = [
        dict(status='success', title='Title {}'.format(nr))
        for nr in range(10)
    ]

    landfiles = [x for x in context.landfiles.get_all()]

    assert result == expect
    assert len(landfiles) == 10
    assert all(lf.fileSize != 'N/A' for lf in landfiles)

    # files should exist and errors should be raised
    _file.seek(0)
    result_err = admin()
    expect_err = [
        dict(status='error', title='Title {}'.format(nr))
        for nr in range(10)
    ]

    assert result_err == expect_err
    assert len(landfiles) == 10
    assert all(lf.fileSize != 'N/A' for lf in landfiles)


def test_admin_PUT(context, testfiles, normalizer):
    _file = file_from_template(FILE_PUT, 'import')

    form = dict(
        file=_file,
        inlineRadioOptions='put',
        submit='submit'
    )

    request = Request(form=form)
    result = MockAdmin(context, request)()

    expect = [
        dict(status='success', title='Title {}'.format(nr))
        for nr in range(10)
    ]

    landfiles = [x for x in context.landfiles.get_all()]

    assert result == expect
    assert len(landfiles) == 10
    assert all(lf.fileSize != 'N/A' for lf in landfiles)


def test_admin_GET_135(context, testfiles, normalizer):
    _file = file_from_template(FILE_GET_DEL_135, 'import')

    form = dict(
        file=_file,
        inlineRadioOptions='get',
        submit='submit'
    )

    request = Request(form=form)
    result = MockAdmin(context, request)()

    def _dict(nr, landfile):
        return dict(
            status='success',
            title='Title {}'.format(nr),
            id='title-{}'.format(nr),
            description='Description modified {}'.format(nr),
            download_url='http://localhost/testfile{}'.format(nr),
            categorization_tags=[
                ['Type', 'Vector'],
                ['Country', 'Romania']
            ],
            size=landfile.fileSize,
        )

    api = LandFileApi(context.landfiles)

    expect = [
        _dict(nr, api.get('Title {}'.format(nr)))
        for nr in [1, 3, 5]
    ]

    assert result == expect


def test_admin_DEL_135(context, testfiles, normalizer):
    _file = file_from_template(FILE_GET_DEL_135, 'import')

    form = dict(
        file=_file,
        inlineRadioOptions='delete',
        submit='submit'
    )

    request = Request(form=form)
    result = MockAdmin(context, request)()

    expect = [
        dict(status='success', title='Title {}'.format(nr))
        for nr in [1, 3, 5]
    ]

    assert result == expect
