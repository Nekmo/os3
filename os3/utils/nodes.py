# -*- coding: utf-8 -*-
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


def scandir(path='.', errors=None):
    if sys.version_info >= (3, 5):
        fn = os.scandir
    else:
        try:
            import scandir as fn
        except ImportError:
            fn = lambda x: map(FakeDirEntry, os.listdir(x))
    return fn(path)


def get_path(path):
    if not isinstance(path, (str, six.string_types)):
        path = path.path
    return path


def deep_scandir(path, deep=False, cls=None, filter=None, traverse_filter=None, errors=None):
    filter = filter or (lambda x: True)
    traverse_filter = traverse_filter or (lambda x: True)

    for item in scandir(path, errors):
        item = os.path.join(get_path(path), get_path(item))
        item = item if cls is None else cls(item)
        traverse_result = item.is_dir() and traverse_filter(item)
        if deep and traverse_result:
            new_deep = deep
            if not isinstance(deep, bool) and isinstance(deep, int):
                new_deep = deep - 1
            # yield from deep_scandir(item.path, new_deep)
            # for subitem in deep_scandir(item.path, new_deep, cls):
            for subitem in deep_scandir(item.path, new_deep, cls, filter, traverse_filter, errors):
                yield subitem
        if item.is_dir() and not traverse_result:
            # Si es un directorio y no cumple el traverse_result, no merece probar filter
            continue
        if filter(item):
            yield item
