# -*- coding: utf-8 -*-
import subprocess

from os3.fs.entry import Entry

from os3.core.list import init_tree, Os3List


def all_childrens(process):
    yield process
    for child in process._children:
        for subchild in all_childrens(child):
            yield subchild


def set_cache_tree(tree):
    tree = list(tree)
    process_by_pid = {process.pid:process for process in tree}
    for process in tree:
        process._parent = None
        process._children = []
    for process in tree:
        parent = process.parent()
        pid = parent.pid if parent else None
        process._parent = process_by_pid.get(pid)
        if not process._parent:
            continue
        process._parent._children.append(process)
    return tree


def name_id_parent_fn(process):
    parent = process._parent
    parent = parent.pid if parent is not None else None
    return process.name(), process.pid, parent


class Processes(Os3List):
    def _get_iter(self):
        import psutil
        return iter(psutil.pids())

    def _prepare_next(self, process):
        from .process import Process
        return Process(process)

    def print_format(self):
        return self.tree_format()

    def tree_format(self, roots=None, fn_tree=None):
        roots = set_cache_tree(self)
        roots = filter(lambda x: not x._parent, roots)
        return super(Processes, self).tree_format(roots, lambda x: init_tree(all_childrens(x), name_id_parent_fn))

    def __repr__(self):
        return self.print_format()


class Run(object):
    def __init__(self, cmd, cwd=None):
        cmd = list(map(lambda x: x.path if isinstance(x, Entry) else x, cmd))
        if isinstance(cwd, Entry):
            cwd = cwd.path
        self.process = subprocess.Popen(cmd, cwd=cwd)
        self.process.wait()

    @property
    def returncode(self):
        return self.process.returncode
