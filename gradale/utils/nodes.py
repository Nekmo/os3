import os
import sys

import six


class FakeDirEntry(object):
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return self.path.split(self.path)[1]

    @property
    def is_dir(self):
        return os.path.isdir(self.path)

    @property
    def is_symlink(self):
        import pathlib
        return pathlib.Path.is_symlink(self.path)

    def stat(self, follow_symlinks=True):
        return os.stat(self.path, follow_symlinks=follow_symlinks)

    def inode(self):
        return os.stat(self.path).st_ino


def scandir(path='.'):
    if sys.version_info >= (3, 5):
        return os.scandir(path)
    try:
        import scandir
    except ImportError:
        return map(FakeDirEntry, os.listdir(path))
    else:
        return scandir(path)


def deep_scandir(path, deep=False, cls=None, filter=None):
    def get_path(path):
        if not isinstance(path, (str, six.string_types)):
            path = path.path
        return path
    for item in scandir(path):
        item = os.path.join(get_path(path), get_path(item))
        item = item if cls is None else cls(item)
        if filter is not None and not filter(item):
            continue
        yield item
        if deep and item.is_dir():
            new_deep = deep
            if not isinstance(deep, bool) and isinstance(deep, int):
                new_deep = deep - 1
            # yield from deep_scandir(item.path, new_deep)
            for item in  deep_scandir(item.path, new_deep):
                yield item
