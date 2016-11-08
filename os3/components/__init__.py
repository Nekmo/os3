# -*- coding: utf-8 -*-
from __future__ import print_function
from os3.utils.console import pprint_list


def name_id_parent_function(elem):
    return elem[0], elem[1], elem[2]


def init_tree(process, name_id_parent_fn=None):
    name_id_parent_fn = name_id_parent_fn or name_id_parent_function
    from treelib import Tree
    tree = Tree()
    for children in process:
        tree.create_node(*name_id_parent_fn(children))
    return tree


class Os3Item(object):
    name = ''
    __clone_params__ = []

    def check_filters(self, **kwargs):
        for name, value in kwargs.items():
            if self.value(name) != value:
                return False
        return True

    def values(self, *interfaces, **kwargs):
        return {key: getattr(self, key) for key in interfaces}

    def value(self, interface):
        value = getattr(self, interface)
        if hasattr(value, '__call__'):
            value = value()
        return value

    def clone(self):
        params = {key: getattr(self, key) for key in self.__clone_params__}
        new_instance = self.__class__(**params)
        return new_instance

    def print_format(self):
        return self.name.encode('utf8').decode('utf-8', 'replace')

    def print(self):
        print(self.print_format())


class Os3List(Os3Item):
    _tuple_filters = None
    _dict_filters = None
    _sort = None # []
    _iter = None

    def _add_filters(self, filters):
        self._dict_filters = self._dict_filters or {}
        self._dict_filters.update(filters)

    def _set_sort(self, *interfaces):
        self._sort = interfaces

    def filter(self, **kwargs):
        instance = self.clone()
        instance._add_filters(kwargs)
        return instance

    def sort(self, *interfaces):
        instance = self.clone()
        instance._set_sort(*interfaces)
        return instance

    def group_by(self, interface):
        pass

    def _get_iter(self):
        raise NotImplementedError

    def _prepare_iter(self):
        it = self._get_iter()
        if self._sort:
            it = map(self._prepare_next, it)
            it = sorted(it, key=lambda x: [x.value(interface) for interface in self._sort])
        return it

    def _next(self, reset=False):
        """Obtener el siguiente elemento de la iteración sin filtros
        """
        if not self._iter and not reset:
            self._iter = self._prepare_iter()
        return next(self._iter)

    def _prepare_next(self, elem):
        """Devolver el siguiente elemento de la iteración preparado
        """
        raise NotImplementedError

    def __prepare_next(self, elem):
        """Ejecutar _prepare_next solo si no es un Os3Item.
        """
        if isinstance(elem, Os3Item):
            return elem
        return self._prepare_next(elem)

    def list(self):
        return filter(self._elem_is_valid, [self.__prepare_next(elem) for elem in self._prepare_iter()])

    def _elem_is_valid(self, elem):
        """Comprobar si el elemento se puede devolver por los filtros
        """
        return elem.check_filters(**self._dict_filters or {})

    # def __next__(self):
    #     elem = None
    #     while True:
    #         elem = self.__prepare_next(self._next())
    #         if self._elem_is_valid(elem):
    #             break
    #     return elem
    #
    # def __iter__(self):
    #     # Probar a cambiar __next__ por __iter__ y el return del primero por yield
    #     # http://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators
    # http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
    #     return self

    # TODO: Pruebas. Código de arriba funcional
    def __iter__(self):
        while True:
            try:
                elem = self.__prepare_next(self._next())
            except StopIteration:
                self._iter = None
                return
            if not self._elem_is_valid(elem):
                continue
            yield elem

    # def next(self):
    #     """Retrocompatibilidad con Python2
    #     """
    #     return self.__next__()

    def print_format(self):
        return self.list_format()

    def tree_format(self, roots=None, fn_tree=None):
        roots = roots if roots is not None else self
        fn_tree = fn_tree or init_tree
        forest = [fn_tree(x) for x in roots]
        output = ''
        for tree in forest:
            output += str(tree)
        return output

    def list_format(self):
        return pprint_list([x.print_format() for x in self])

    def values(self, *interfaces, **kwargs):
        return super(Os3List, self).values(*interfaces)

    def values_list(self, *interfaces, **kwargs):
        return [n.values(*interfaces, this=True) for n in self.list()]

    def value_list(self, interface, **kwargs):
        return [n.value(interface) for n in self.list()]


class StartsWithEqual(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name.startswith(other)

    def __ne__(self, other):
        return not self.__eq__(other)
