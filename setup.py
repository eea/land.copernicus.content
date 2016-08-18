from land.copernicus.content.config import PACKAGE_AUTHOR
from land.copernicus.content.config import PACKAGE_AUTHOR_EMAIL
from land.copernicus.content.config import PACKAGE_CLASSIFIERS
from land.copernicus.content.config import PACKAGE_DESCRIPTION
from land.copernicus.content.config import PACKAGE_DOCS_FOLDER
from land.copernicus.content.config import PACKAGE_HISTORY_FILE
from land.copernicus.content.config import PACKAGE_KEYWORDS
from land.copernicus.content.config import PACKAGE_NAME
from land.copernicus.content.config import PACKAGE_NAMESPACE_PACKAGES
from land.copernicus.content.config import PACKAGE_README_FILE
from land.copernicus.content.config import PACKAGE_URL
from land.copernicus.content.config import PACKAGE_VERSION_FILE
from setuptools import setup, find_packages
import os

path = PACKAGE_NAME.split('.') + [PACKAGE_VERSION_FILE]
version = open(os.path.join(*path)).read().strip()

setup(
    name=PACKAGE_NAME,
    version=version,
    description=PACKAGE_DESCRIPTION,
    long_description=open(PACKAGE_README_FILE).read() + "\n" +
    open(os.path.join(PACKAGE_DOCS_FOLDER, PACKAGE_HISTORY_FILE)).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=PACKAGE_CLASSIFIERS,
    keywords=PACKAGE_KEYWORDS,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    url=PACKAGE_URL,
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=PACKAGE_NAMESPACE_PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'archetypes.schemaextender',
        'lxml',
        'plone.app.registry',
        'z3c.jbot',
        'Wand',
        'Products.DataGridField',
        'eea.forms',
        'Products.ATVocabularyManager',
        'eea.cache',
    ],
)
