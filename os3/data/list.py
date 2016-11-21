from os3.core.list import Os3List
from os3.data.tree import DataTree


def items_iterator(items):
    for item in items:
        yield item
        if not isinstance(item, DataTree):
            continue
        for subitem in item:
            yield subitem


class DataItems(Os3List, DataTree):

    def _prepare_next(self, elem):
        return elem

    def _get_iter(self):
        return items_iterator(self.data_list)
