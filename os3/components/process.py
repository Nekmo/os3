# -*- coding: utf-8 -*-
import psutil

from os3.components import Os3Item


class Process(psutil.Process, Os3Item):
    pass