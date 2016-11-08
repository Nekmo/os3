# -*- coding: utf-8 -*-
import psutil

from os3.core.item import Os3Item


class Process(psutil.Process, Os3Item):
    pass
