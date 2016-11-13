# -*- coding: utf-8 -*-
from future.builtins import open
import os
import sys

import six

from os3.fs.entry import Entry


class File(Entry):
    __interfaces__ = ['name']
    __clone_params__ = ['path']
    _type = 'file'
    _open = None
    _mode = None
    _ext = None

    def _get_open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if self._open is None or self._mode != mode:
            self._mode = mode
            return self.open(mode, buffering, encoding, errors, newline, closefd, opener)
        else:
            return self._open

    def open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        if sys.version_info >= (3, 0):
            self._open = open(self.path, mode, buffering, encoding, errors, newline, closefd, opener)
        else:
            self._open = open(self.path, mode)
        return self

    def read(self, n=None, mode=None, buffering=-1, encoding=None, errors=None, newline=None, closefd=True,
             opener=None):
        mode = mode or self._mode or 'r'
        if n is not None and not isinstance(n, int):
            mode = n
            n = None
        if six.PY2 and n is None:
            # PATCH: Python2 requiere que n sea un int siempre
            n = -1
        data = self._get_open(mode, buffering, encoding, errors, newline, closefd, opener).read(n)
        if n is None or n is -1:
            self.seek(0)
        return data

    def write(self, data, mode=None, buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        mode = mode or self._mode or 'w'
        if six.PY2 and 'b' not in mode and isinstance(data, bytes):
            data = data.decode('utf-8')
        self._get_open(mode, buffering, encoding, errors, newline, closefd, opener).write(data)

    def touch(self):
        if not self.lexists():
            self.write('')
        return self

    def tell(self):
        return self._open.tell()

    @property
    def size(self):
        return os.path.getsize(self.path)

    @property
    def ext(self):
        if self._ext is None:
            parts = self.name.split('.')
            self._ext = parts[-1] if len(parts) > 1 else ''
        return self._ext

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
        line = self.readlines(1, mode, buffering, encoding, errors, newline, closefd, opener, breakline)
        if not line:
            return None
        return line[0]

    def seek(self, i):
        return self._open.seek(i)

    def remove(self):
        return os.remove(self.path)

    def __repr__(self):
        return self.name