# -*- coding: utf-8 -*-


class StartsWithEqual(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name.startswith(other)

    def __ne__(self, other):
        return not self.__eq__(other)
