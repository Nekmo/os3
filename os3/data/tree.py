from os3.data.item import DataItem


class DataTree(DataItem):
    def __init__(self, data_list, **kwargs):
        super(DataItem, self).__init__(**kwargs)
        self.data_list = data_list

    def ls(self, depth=None):
        from os3.data.list import DataItems
        return DataItems(self.data_list, depth=depth)
