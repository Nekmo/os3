# -*- coding: utf-8 -*-

from __future__ import print_function


class Os3Item(object):
    name = ''
    __clone_params__ = []

    def check_filters(self, *args, **kwargs):
        for fn_filter in args:
            if not fn_filter(self):
                return False
        for name, value in kwargs.items():
            if self.value(name) != value:
                return False
        return True

    def values(self, *interfaces, **kwargs):
        return {key: getattr(self, key) for key in interfaces}

    def values_list(self, *interfaces):
        return [self.value(key) for key in interfaces]

    def value(self, interface):
        value = getattr(self, interface)
        if hasattr(value, '__call__'):
            value = value()
        return value

    def clone(self, **extra):
        params = {key: getattr(self, key) for key in self.__clone_params__}
        params.update(extra)
        new_instance = self.__class__(**params)
        return new_instance

    def print_format(self):
        return self.name.encode('utf8').decode('utf-8', 'replace')

    def print(self):
        print(self.print_format())

    def __repr__(self):
        return self.print_format()
