import os

import posix

import shutil
import six
import sys

from gradale.components import GradaleList, StartsWithEqual
from gradale.utils.console import pprint_list
from gradale.utils.nodes import deep_scandir
from . import GradaleComponent


class Node(GradaleComponent):
    _type = None
    path = ''

    def __new__(cls, *args, **kwargs):
        if cls != Node or not args:
            return GradaleComponent.__new__(cls)
        path = os.path.realpath(os.path.expanduser(args[0])) if args else None
        if path and os.path.isdir(path):
            return Dir.__new__(Dir, *args, **kwargs)
        elif path and os.path.isfile(path):
            return File.__new__(File, *args, **kwargs)
        return GradaleComponent.__new__(cls)

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

    def exists(self):
        return os.path.exists(self.path)

    def lexists(self):
        return os.path.lexists(self.path)

    def is_dir(self):
        return self.type == 'directory'

    def is_file(self):
        return self.type == 'file'

    def bak(self):
        if not self.lexists():
            return self
        i = -1
        bak_name = self.path + '.bak'
        while True:
            new_bak_name = bak_name
            if i > -1:
                new_bak_name += str(i)
            if not os.path.lexists(new_bak_name):
                shutil.move(self.path, new_bak_name)
                break
            i += 1
        return self

    def symlink(self, link_name):
        os.symlink(self.path, get_path(link_name))

    def copy(self, dst, symlinks=False, ignore=None):
        shutil.copytree(self.path, os.path.expanduser(dst), symlinks, ignore)

    def sub(self, subpath):
        return Node(os.path.join(self.path, get_path(subpath)))

    @classmethod
    def _get_path(cls, path):
        """Obtener el path de una variable path, que puede ser el propio path, o un DirEntry
        """
        if not isinstance(path, (str, six.string_types)):
            # Es un DirEntry
            path = path.path
        return os.path.abspath(os.path.expanduser(path))


class File(Node):
    __interfaces__ = ['name']
    __clone_params__ = ['path']
    _type = 'file'
    _open = None

    def _get_open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if self._open is None:
            return self.open(mode, buffering, encoding, errors, newline, closefd, opener)
        else:
            return self._open

    def open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if sys.version_info >= (3, 0):
            self._open = open(self.path, mode, buffering, encoding, errors, newline, closefd, opener)
        else:
            self._open = open(self.path, mode)
        return self

    def read(self, n=None, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if n is not None and not isinstance(n, int):
            mode = n
            n = None
        return self._get_open(mode, buffering, encoding, errors, newline, closefd, opener).read(n)

    def tell(self):
        return self._open.tell()

    def size(self):
        return os.path.getsize(self.path)

    def readlines(self, n=None, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True,
                  opener=None, breaklines=True):
        if n is not None and not isinstance(n, int):
            mode = n
            n = None
        lines = self._get_open(mode, buffering, encoding, errors, newline, closefd, opener).readlines(n)

        def remove_breakline(line):
            if line.endswith('\r\n'):
                return line[:-2]
            if line.endswith('\n'):
                return line[:-1]
            return line
        if not breaklines:
            lines = list(map(remove_breakline, lines))
        return lines

    def readline(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None,
                 breakline=True):
        return self.readlines(1, mode, buffering, encoding, errors, newline, closefd, opener, breakline)

    def seek(self, i):
        return self._open.seek(i)

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
        return deep_scandir(self.path, self.deep, cls=Node.get_node, filter=lambda x: True)
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


def bak_target_decorator(fn):
    def decorator(src, dst=None, **kwargs):
        src, dst = Node(src), Node(dst) if dst else dst
        if dst and os.path.islink(dst.path) and os.path.realpath(dst.path) == os.path.realpath(src.path):
            return
        if not dst and src.exists():
            return
        elif dst and dst.lexists():
            dst.bak()
        return fn(src, dst, **kwargs) if dst is not None else fn(src, **kwargs)
    return decorator


def get_path(node):
    if isinstance(node, Node):
        return node.path
    return os.path.abspath(os.path.expanduser(node))


def get_node(path):
    if not isinstance(path, Node):
        return Node(path)
    return path


def symlink(source, link_name):
    return get_node(source).symlink(link_name)


def mkdir(path, mode=511, exists_ok=False):
    if sys.version_info >= (3,0):
        return os.makedirs(get_path(path), mode, exists_ok)
    return os.makedirs(get_path(path), mode)


def cp(src, dst, symlinks=False, ignore=None):
    return get_node(src).copy(dst, symlinks, ignore)
