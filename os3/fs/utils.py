# -*- coding: utf-8 -*-
import os
from .entry import Entry


def bak_target_decorator(fn):
    def decorator(src, dst=None, **kwargs):
        src, dst = Entry(src), Entry(dst) if dst else dst
        if dst and os.path.islink(dst.path) and os.path.realpath(dst.path) == os.path.realpath(src.path):
            return
        if not dst and src.exists():
            return
        elif dst and dst.lexists():
            dst.bak()
        return fn(src, dst, **kwargs) if dst is not None else fn(src, **kwargs)
    return decorator


def get_abspath(node):
    if isinstance(node, Entry):
        return node.path
    return os.path.abspath(os.path.expanduser(node))


def get_node(path):
    if not isinstance(path, Entry):
        return Entry(path)
    return path
