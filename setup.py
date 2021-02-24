import os

from setuptools import find_packages, setup

name = 'land.copernicus.content'
path = name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(
    name=name,
    version=version,
    description="Custom Content-Types for Land Copernicus",
    long_description=open("README.txt").read() + "\n" +
    open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=["Programming Language :: Python", ],
    keywords='land copernicus eea content-types plone zope',
    author='European Environment Agency',
    author_email="webadmin@eea.europa.eu",
    url='http://github.com/eea/land.copernicus.content',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages=['land', 'land.copernicus'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.app.dexterity',
        'setuptools',
        'archetypes.schemaextender',
        'lxml',
        'plone.app.registry',
        'z3c.jbot',
        'Wand',
        'Products.DataGridField',
        'collective.z3cform.datagridfield==1.2.0',
        'eea.forms',
        'Products.ATVocabularyManager',
        'eea.cache',
        'eea.geotags',
        'plone.app.async',
        'five.pt',
        'plone.stringinterp==1.0.14',  # needed for IContextWrapper in async
        'eea.rdfmarshaller>=10.5',
        'eea.meeting',
        'eea.sentry',
        'pycountry',
        'plone.namedfile [blobs]'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    users_stats = land.copernicus.content.browser.scripts:users_stats
    subscrib_reset = land.copernicus.content.browser.scripts:subscrib_reset
    send_emails = land.copernicus.content.browser.scripts:send_emails
    """,
)
