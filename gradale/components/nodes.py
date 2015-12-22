import os

import posix

import six

from gradale.components import GradaleList, StartsWithEqual
from gradale.utils.console import pprint_list
from gradale.utils.nodes import deep_scandir
from . import GradaleComponent


class Node(GradaleComponent):
    _type = None
    path = ''

    def __init__(self, path, **kwargs):
        self.path = self._get_path(path)

    @property
    def name(self):
        return os.path.split(self.path)[1]

    @property
    def size(self):
        return os.path.getsize(self.path)

    @property
    def ctime(self):
        return os.path.getctime(self.path)

    @property
    def mtime(self):
        return os.path.getmtime(self.path)

    @property
    def atime(self):
        return os.path.getatime(self.path)

    @classmethod
    def get_cls(cls, path):
        if os.path.isdir(path):
            # return File
            return Dir
        else:
            return File

    @classmethod
    def get_node(cls, path):
        path = cls._get_path(path)
        return cls.get_cls(path)(path)

    @property
    def type(self):
        return StartsWithEqual(self._type)

    def is_dir(self):
        return self.type == 'directory'

    def is_file(self):
        return self.type == 'file'

    @classmethod
    def _get_path(cls, path):
        """Obtener el path de una variable path, que puede ser el propio path, o un DirEntry
        """
        if not isinstance(path, (str, six.string_types)):
            # Es un DirEntry
            path = path.path
        return path


class File(Node):
    __interfaces__ = ['name']
    __clone_params__ = ['path']
    _type = 'file'

    def __repr__(self):
        return self.name


class Dir(Node, GradaleList):
    _pre_filters = None
    __interfaces__ = ['name']
    __clone_params__ = ['path', 'deep']
    _ls = None
    _type = 'directory'

    def __init__(self, path=None, deep=None, **kwargs):
        path = path or os.getcwd()
        super(Dir, self).__init__(path)
        self.deep = deep
        self.root = kwargs.pop('root', None)
        self._pre_filters = kwargs

    def items(self):
        return []

    def _get_iter(self):
        return deep_scandir(self.path, self.deep, cls=Node.get_node, filter=lambda x: False)
        # return iter(os.listdir(self.path))

    def _prepare_next(self, elem):
        return Node.get_node(elem.path)
        # return Node.get_node(os.path.join(self.path, elem))

    def _elem_is_valid(self, elem):
        # TODO: Hay 2 tipos de filtros: aquellos que se aplican DURANTE el listado, y aquellos que se aplican DESPUÉS.
        # if elem.is_dir() and self.deep:
        #     # Aplicar SOLO los filtros previos a los directorios
        #     return elem.check_filters(**self._pre_filters or {})
        return elem.check_filters(**self._filters or {})

    # def __repr__(self):
    #     return pprint_list(list(self._get_iter()))

    def __repr__(self):
        return self.name