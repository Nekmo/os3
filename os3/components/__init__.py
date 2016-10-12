# -*- coding: utf-8 -*-
from os3.utils.console import pprint_list


class GradaleComponent(object):
    name = ''
    __clone_params__ = []

    def check_filters(self, **kwargs):
        for name, value in kwargs.items():
            if getattr(self, name) != value:
                return False
        return True

    def values(self, *interfaces, **kwargs):
        return {key: getattr(self, key) for key in interfaces}

    def value(self, interface, this=True):
        return getattr(self, interface)

    def clone(self):
        params = {key: getattr(self, key) for key in self.__clone_params__}
        new_instance = self.__class__(**params)
        return new_instance

    def print_format(self):
        return self.name

    def print(self):
        print(self.print_format())


class GradaleList(GradaleComponent):
    _filters = None # {}
    _sort = None # []
    _iter = None

    def _add_filters(self, filters):
        self._filters = self._filters or {}
        self._filters.update(filters)

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
            # TODO: eliminar luego
            it = [x for x in it]
            # TODO: depurando. Los que son un archivo devuelven el método sin llamar. Directorios vacíos...
            # ¡¿una lista vacía?! Resultado esperado: int.
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
        """Ejecutar _prepare_next solo si no es un GradaleComponent.
        """
        if isinstance(elem, GradaleComponent):
            return elem
        return self._prepare_next(elem)

    def list(self):
        return filter(self._elem_is_valid, [self.__prepare_next(elem) for elem in self._prepare_iter()])

    def _elem_is_valid(self, elem):
        """Comprobar si el elemento se puede devolver por los filtros
        """
        return elem.check_filters(**self._filters or {})

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
                raise StopIteration
            if not self._elem_is_valid(elem):
                continue
            yield elem

    # def next(self):
    #     """Retrocompatibilidad con Python2
    #     """
    #     return self.__next__()

    def print_format(self):
        return pprint_list([x.print_format() for x in self])

    def values(self, *interfaces, **kwargs):
        return super(GradaleList, self).values(*interfaces)

    def values_list(self, *interfaces, **kwargs):
        return [n.values(*interfaces, this=True) for n in self.list()]

    def value(self, interface, **kwargs):
        # TODO: habría que cambiar la lógica en 2 métodos para diferenciar
        # un objeto directorio de cuando se quiere obtener los values de los
        # elementos contenidos
        return super(GradaleList, self).value(interface)

    def value_list(self, interface, **kwargs):
        return [n.value(interface) for n in self.list()]


class StartsWithEqual(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name.startswith(other)

    def __ne__(self, other):
        return not self.__eq__(other)