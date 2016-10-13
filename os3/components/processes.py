import subprocess

from os3.fs.entry import Entry

from os3.components import GradaleList, GradaleComponent


class Processes(GradaleList):
    def _get_iter(self):
        import psutil
        return iter(psutil.pids())

    def _prepare_next(self, process):
        from .process import Process
        return Process(process)


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
