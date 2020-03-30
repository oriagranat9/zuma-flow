# knows how to start/end the game from windows
import psutil
import os
from win32 import win32gui, win32process


class ProcessHandler:
    def __init__(self, executable_path):
        self.executable_path = executable_path
        os.path.isfile(executable_path)  # self.process_name = os.path.basename(self.executable_path)
        self.process_name = executable_path
        self.process_dir = os.path.dirname(self.executable_path)
        self._hwnd = None
        self._pid = None

    def is_running(self):
        pass

    def run(self):
        # check if is already running
        os.chdir('c:\\documents and settings\\flow_model')
        os.system('"C:\\Documents and Settings\\flow_model\\flow.exe"')

    def terminate(self):
        pass

    def hwnd(self):
        def callback(hwnd, hwnds):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == self._pid:
                hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0]

    def pid(self):
        for proc in psutil.process_iter():
            try:
                if self.process_name in proc.name():
                    self._pid = int(proc.pid)
                    break
            except:
                continue
        return self._pid
