import psutil
import os, signal
import subprocess
from win32 import win32gui, win32process

# knows how to start/end the game from windows
class ProcessHandler:
    def __init__(self, executable_path):
        if not os.path.isfile(executable_path):
            raise Exception(f"{executable_path} is not a valid path.")
        self.executable_path = executable_path
        self.work_dir = os.path.dirname(self.executable_path)
        self.process_name = os.path.basename(self.executable_path)
        self._hwnd = None
        self._pid = None

    def is_running(self):
        return self.pid() is not None

    def run(self):
        if self.is_running() is not True:
            subprocess.Popen(self.executable_path, cwd=self.work_dir)

    def terminate(self):
        if self.is_running():
            os.kill(self._pid, signal.SIGTERM) 

    def hwnd(self):
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == self._pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        if len(hwnds) > 0:
            return hwnds[0]
        return None

    def pid(self):
        self._pid = None        
        for proc in psutil.process_iter():
            try:
                if self.process_name in proc.name():
                    self._pid = int(proc.pid)
                    break
            except:
                continue
        return self._pid
