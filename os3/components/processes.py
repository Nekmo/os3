import subprocess

from os3.fs.entry import Entry

from os3.components import GradaleList, GradaleComponent


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
        if parent is None:
            continue
        process._parent = process_by_pid[parent.pid]
        process._parent._children.append(process)
    return tree


def init_tree(process):
    from treelib import Node, Tree
    tree = Tree()
    # tree.create_node(process.name(), process.pid)
    for children in all_childrens(process):
        parent = children._parent
        parent = parent.pid if parent is not None else None
        tree.create_node(children.name(), children.pid, parent)
    return tree


class Processes(GradaleList):

    def _get_iter(self):
        import psutil
        return iter(psutil.pids())

    def _prepare_next(self, process):
        from .process import Process
        return Process(process)

    def print_format(self):
        cached_tree = set_cache_tree(self)
        forest = [init_tree(x) for x in filter(lambda x: not x._parent, cached_tree)]
        output = ''
        for tree in forest:
            output += str(tree)
        return output

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
