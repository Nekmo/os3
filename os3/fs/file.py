import os
import sys

import six

from os3.fs.entry import Entry


class File(Entry):
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
        if six.PY2 and n is None:
            # PATCH: Python2 requiere que n sea un int siempre
            n = -1
        return self._get_open(mode, buffering, encoding, errors, newline, closefd, opener).read(n)

    def tell(self):
        return self._open.tell()

    @property
    def size(self):
        return os.path.getsize(self.path)

    def readlines(self, n=None, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True,
                  opener=None, breaklines=True):
        if n is not None and not isinstance(n, int):
            mode = n
            n = 0
        if six.PY2 and n is None:
            # PATCH: Python2 requiere que n sea un int siempre
            n = 0
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