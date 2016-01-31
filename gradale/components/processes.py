import subprocess

from gradale.components.nodes import Node


class Run(object):
    def __init__(self, cmd, cwd=None):
        cmd = list(map(lambda x: x.path if isinstance(x, Node) else x, cmd))
        if isinstance(cwd, Node):
            cwd = cwd.path
        self.process = subprocess.Popen(cmd, cwd=cwd)
        self.process.wait()

    @property
    def returncode(self):
        return self.process.returncode