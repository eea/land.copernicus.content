from App.Common import package_home
from cgi import FieldStorage
from cStringIO import StringIO
from land.copernicus.content.config import product_globals
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
import os
from ZPublisher.HTTPRequest import FileUpload


@onsetup
def setup_copernicus_contenttypes():
    """Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import land.copernicus.content
    zcml.load_config('configure.zcml', land.copernicus.content)
    fiveconfigure.debug_mode = False

    ptc.installPackage('land.copernicus.content')


setup_copernicus_contenttypes()
ptc.setupPloneSite(products=['land.copernicus.content'])


class BaseCopernicusContentTestCase(ptc.PloneTestCase):
    """Base class for integration tests.

    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """
    def loadfile(self, rel_filename, ctype='image/png'):
        """ load a file
        """
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = open(filename, 'r').read()

        fp = StringIO(data)
        fp.seek(0)

        env = {'REQUEST_METHOD': 'PUT'}
        headers = {'content-type': ctype,
                   'content-length': len(data),
                   'content-disposition': 'attachment; filename=test.txt'}

        fs = FieldStorage(fp=fp, environ=env, headers=headers)
        ufile = FileUpload(fs)
        ufile.name = None
        return ufile
