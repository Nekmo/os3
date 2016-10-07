import os
import sys
import stat

import six


class FakeDirEntry(object):
    _stat = None

    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return self.path.split(self.path)[1]

    def is_dir(self):
        return stat.S_ISDIR(self.stat().st_mode)

    def is_symlink(self):
        return stat.S_ISLNK(self.stat().st_mode)

    def is_file(self):
        return stat.S_ISREG(self.stat().st_mode)

    def stat(self):
        if not self._stat:
            self._stat = os.stat(self.path)
        return self._stat

    def inode(self):
        return self.stat().st_ino


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
            for item in deep_scandir(item.path, new_deep, cls):
                yield item
