from os3.core.list import Os3List
from os3.data.tree import DataTree


def items_iterator(items, depth=None):
    for item in items:
        yield item
        if not isinstance(item, DataTree) or not depth:
            continue
        depth = depth - 1 if not isinstance(depth, bool) and isinstance(depth, int) else depth
        for subitem in item.ls(depth=depth):
            yield subitem


class DataItems(Os3List, DataTree):

    def __init__(self, data_list, interfaces=None, depth=None):
        super(DataItems, self).__init__(data_list)
        self.depth = depth
        self.update(interfaces or {})

    def _prepare_next(self, elem):
        return elem

    def _get_iter(self):
        return items_iterator(self.data_list, self.depth)
