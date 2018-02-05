import os
import random
import string
from functools import partial

from land.copernicus.content.config import ENV_DL_SRC_PATH


def _make_temp_dir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def make_random_string(size):
    """ Will be slow for large sizes!
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))


def _add_testfile(path, name, size):
    path_testfile = os.path.join(path, name)
    with open(path_testfile, 'w') as testfile:
        testfile.write(make_random_string(size))


def _rm_testfile(path, name):
    os.remove(os.path.join(path, name))


add_testfile = partial(_add_testfile, ENV_DL_SRC_PATH)
rm_testfile = partial(_rm_testfile, ENV_DL_SRC_PATH)
make_temp_dir = partial(_make_temp_dir, ENV_DL_SRC_PATH)
