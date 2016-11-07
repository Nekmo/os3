# -*- coding: utf-8 -*-
import os
import sys

from os3.fs import __init__, Entry, get_path


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


def symlink(source, link_name):
    return get_node(source).symlink(link_name)


def mkdir(path, mode=511, exists_ok=False):
    if sys.version_info >= (3,0):
        return os.makedirs(get_path(path), mode, exists_ok)
    return os.makedirs(get_path(path), mode)


def cp(src, dst, symlinks=False, ignore=None):
    return get_node(src).copy(dst, symlinks, ignore)