# knows how to start/end the game from windows
import psutil
import os
from win32 import win32gui, win32process


class ProcessHandler:
	def __init__(self, executable_path):

		self.executable_path = executable_path
		os.path.isfile(executable_path)
		#self.process_name = os.path.basename(self.executable_path)
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
		if self._hwnd is None:
			self._hwnd = win32gui.FindWindow(None, self.process_name)
		return self._hwnd


	def pid(self):
		if self._pid is None:
			# for proc in psutil.process_iter():
			# 	if self.process_name in proc.name:
			# 		self.pid = int(proc.pid)
			# 		break
			_, self._pid = win32process.GetWindowThreadProcessId(self.hwnd())
		return self._pid

	def _enum_cb(self, hwnd, result):
		self.all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
