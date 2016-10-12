import os
import shutil

import six

from os3.components import GradaleComponent, StartsWithEqual


class Entry(GradaleComponent):
    _type = None
    path = ''

    def __new__(cls, *args, **kwargs):
        from os3.fs.directory import Dir
        from os3.fs.file import File

        if cls != Entry or not args:
            return GradaleComponent.__new__(cls)
        if args and isinstance(args[0], Entry):
            path = args[0].path
        else:
            path = os.path.realpath(os.path.expanduser(args[0])) if args else None
        if path and os.path.isdir(path):
            return Dir.__new__(Dir, *args, **kwargs)
        elif path and os.path.isfile(path):
            return File.__new__(File, *args, **kwargs)
        return File.__new__(File, *args, **kwargs)
        # return GradaleComponent.__new__(cls)

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
        from os3.fs.directory import Dir
        from os3.fs.file import File

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
        return Entry(os.path.join(self.path, get_path(subpath)))

    @classmethod
    def _get_path(cls, path):
        """Obtener el path de una variable path, que puede ser el propio path, o un DirEntry
        """
        if not isinstance(path, (str, six.string_types)):
            # Es un DirEntry
            path = path.path
        return os.path.abspath(os.path.expanduser(path))


def get_path(node):
    if isinstance(node, Entry):
        return node.path
    return os.path.expanduser(node)
