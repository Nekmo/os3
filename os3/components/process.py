# -*- coding: utf-8 -*-
import psutil

from os3.components import Os3Component


class Process(psutil.Process, Os3Component):
    pass