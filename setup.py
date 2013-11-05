from setuptools import setup, find_packages
import os

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()

name = 'land.copernicus.content'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()

setup(name=name,
      version=version,
      description="Custom Content-Types for Land Copernicus",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='land copernicus eea content-types plone zope',
      author='European Environment Agency',
      author_email="webadmin@eea.europa.eu",
      url='http://github.com/eea/land.copernicus.content',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['land', 'land.copernicus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
