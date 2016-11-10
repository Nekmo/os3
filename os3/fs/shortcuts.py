import os
import sys

from os3.fs.directory import DirList
from os3.fs.entry import get_path
from os3.fs.utils import get_node
from os3.utils.decorators import withrepr


@withrepr(lambda x: DirList().print_format())
def ls(path='', depth=None, **kwargs):
    return DirList(path).ls(depth, **kwargs)
ls.filter = DirList().filter


def symlink(source, link_name):
    return get_node(source).symlink(link_name)


def mkdir(path, mode=511, exists_ok=False):
    if sys.version_info >= (3,0):
        return os.makedirs(get_path(path), mode, exists_ok)
    return os.makedirs(get_path(path), mode)


def cp(src, dst, symlinks=False, ignore=None):
    return get_node(src).copy(dst, symlinks, ignore)
