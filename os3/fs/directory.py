# -*- coding: utf-8 -*-
import os
import shutil

import six
from colorama import Fore, Style

from os3.core.list import init_tree, Os3List
from os3.fs.entry import Entry
from os3.utils.nodes import deep_scandir


def name_id_parent_fn(item):
    parent = item.parent()
    parent = parent.path if parent is not None else None
    return item.name, item.path, parent


def init_dir_tree(directory, *args):
    directory = directory.clone()
    directory.root = directory.path
    directories = list(sorted(directory, key=lambda x: x.depth()))
    return init_tree([directory] + directories, name_id_parent_fn)


if six.PY3:
    LS_EXCEPTIONS = (PermissionError, OSError)
else:
    LS_EXCEPTIONS = (OSError,)


class Dir(Entry):
    _type = 'directory'

    @classmethod
    def get_dir_list_class(cls):
        return DirList

    def ls(self, depth=None, fail=False, **kwargs):
        return self.get_dir_list_class()(self.path, depth, fail, **kwargs)

    def mkdir(self, name, exist_ok=True):
        subdirectory = self.sub(name)
        if not subdirectory.lexists() or not exist_ok:
            os.mkdir(subdirectory.path)
        return subdirectory

    def remove(self):
        return shutil.rmtree(self.path)

    def print_format(self):
        return '{Fore.BLUE}{name}{Style.RESET_ALL}'.format(name=self.name, Fore=Fore, Style=Style)


class DirList(Dir, Os3List):
    _pre_filters = None
    __interfaces__ = ['name']
    __clone_params__ = ['path', 'depth']
    _ls = None

    def __init__(self, path=None, depth=None, fail=False, **kwargs):
        # TODO: renombrar depth a depth
        path = path or os.getcwd()
        super(DirList, self).__init__(path)
        self.depth = depth
        self.fail = fail
        self.root = kwargs.pop('root', None)
        self.default_format = kwargs.pop('default_format', self.default_format)
        self._pre_filters = kwargs

    def _get_iter(self):
        return deep_scandir(self.path, self.depth, cls=self.get_entry_class(), filter=self._filter,
                            traverse_filter=self._traverse_filter, exceptions=self._get_catched_exceptions())
        # return iter(os.listdir(self.path))

    def _get_catched_exceptions(self):
        return LS_EXCEPTIONS if not self.fail else ()

    def _prepare_next(self, elem):
        return self.get_entry_class().get_node(elem.path)
        # return Node.get_node(os.path.join(self.path, elem))

    def _filter(self, elem):
        return elem.check_filters(**self._pre_filters or {}) and elem.check_filters(**self._dict_filters or {})

    def _traverse_filter(self, elem):
        return elem.check_filters(**self._pre_filters or {})

    def tree_format(self, roots=None, fn_tree=None, roots_filter_fn=None):
        return super(DirList, self).tree_format([self], init_dir_tree)

    def print_format(self):
        return Os3List.print_format(self)

    def remove(self):
        for item in self:
            item.remove()
