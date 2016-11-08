# -*- coding: utf-8 -*-
import os

from colorama import Fore, Style

from os3.components import Os3List, init_tree
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


class Dir(Entry):
    _type = 'directory'

    def ls(self, depth=None, **kwargs):
        return DirList(self.path, depth, **kwargs)

    def print_format(self):
        return '{Fore.BLUE}{name}{Style.RESET_ALL}'.format(name=self.name, Fore=Fore, Style=Style)

    def __repr__(self):
        return self.name


class DirList(Dir, Os3List):
    _pre_filters = None
    __interfaces__ = ['name']
    __clone_params__ = ['path', 'deep']
    _ls = None

    def __init__(self, path=None, deep=None, **kwargs):
        # TODO: renombrar deep a depth
        path = path or os.getcwd()
        super(Dir, self).__init__(path)
        self.deep = deep
        self.root = kwargs.pop('root', None)
        self._pre_filters = kwargs

    def _get_iter(self):
        return deep_scandir(self.path, self.deep, cls=Entry, filter=self._filter, traverse_filter=self._traverse_filter)
        # return iter(os.listdir(self.path))

    def _prepare_next(self, elem):
        return Entry.get_node(elem.path)
        # return Node.get_node(os.path.join(self.path, elem))

    def _filter(self, elem):
        return elem.check_filters(**self._pre_filters or {}) and elem.check_filters(**self._dict_filters or {})

    def _traverse_filter(self, elem):
        return elem.check_filters(**self._pre_filters or {})

    def tree_format(self, roots=None, fn_tree=None, roots_filter_fn=None):
        return super(Dir, self).tree_format([self], init_dir_tree)

    def print_format(self):
        return Os3List.print_format(self)

    def __repr__(self):
        return self.print_format()