import subprocess

from gradale.components.nodes import Node, get_path


class Run(object):
    def __init__(self, cmd, cwd=None):
        cmd = list(map(get_path, cmd))
        if isinstance(cwd, Node):
            cwd = cwd.path
        self.process = subprocess.Popen(cmd, cwd=cwd)
        self.process.wait()

    @property
    def returncode(self):
        return self.process.returncode