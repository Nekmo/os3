# -*- coding: utf-8 -*-
import random

from os3.core.item import Os3Item
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


class Os3List(Os3Item):
    default_format = 'list'
    _tuple_filters = None
    _dict_filters = None
    _sort = None # []
    _iter = None
    _format_interfaces = None  # Uses in table

    def _add_filters(self, tuple_filters, dict_filters):
        self._tuple_filters = self._tuple_filters or ()
        self._dict_filters = self._dict_filters or {}
        self._tuple_filters += tuple_filters
        self._dict_filters.update(dict_filters)

    def _set_sort(self, *interfaces):
        self._sort = interfaces

    def filter(self, *args, **kwargs):
        instance = self.clone()
        instance._add_filters(args, kwargs)
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
            it = iter(it)
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
        return elem.check_filters(*self._tuple_filters or (), **self._dict_filters or {})

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

    def _table_class(self):
        from terminaltables import SingleTable
        return SingleTable

    def print_format(self):
        return getattr(self, '{}_format'.format(self.default_format))()

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

    def table_format(self, *interfaces):
        interfaces = interfaces or self._format_interfaces
        table_class = self._table_class()
        data = self.values_list(*interfaces)
        data = [interfaces] + data
        table = table_class(data)
        return table.table

    def values(self, *interfaces, **kwargs):
        return [n.values(*interfaces, this=True) for n in self.list()]

    def values_list(self, *interfaces):
        return [n.values_list(*interfaces) for n in self.list()]

    def value(self, interface, **kwargs):
        return [n.value(interface) for n in self.list()]

    def random(self):
        return random.choice(list(self))

    def tree(self):
        return self.clone(default_format='tree')

    def table(self, *interfaces):
        ls = self.clone(default_format='table')
        ls._format_interfaces = interfaces
        return ls

    def count(self):
        return len(list(self))
