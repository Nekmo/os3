from os3.core.item import Os3Item


class DataItem(dict, Os3Item):
    def value(self, interface):
        return self[interface]
