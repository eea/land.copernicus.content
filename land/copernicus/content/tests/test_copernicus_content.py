""" Test suites for eea.indicators
"""

import unittest
import doctest

from Testing import ZopeTestCase as ztc

from land.copernicus.content.tests import base

OPTION_FLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    contenttypes = ztc.ZopeDocFileSuite(
        'doc/contenttypes.txt', package='land.copernicus.content',
        test_class=base.BaseCopernicusContentTestCase,
        optionflags=OPTION_FLAGS)
    overview = ztc.FunctionalDocFileSuite(
        'doc/overview.txt', package='land.copernicus.content',
        test_class=base.BaseCopernicusContentTestCase,
        optionflags=OPTION_FLAGS)

    return unittest.TestSuite([contenttypes, overview])
