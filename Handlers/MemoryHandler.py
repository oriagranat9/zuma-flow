from ctypes import *
import ctypes
import psutil
import win32api
import win32process


class MemoryReader:
    def __init__(self, process_name):
        self.PROCESS_QUERY_INFORMATION = 0x0400
        self.PROCESS_VM_READ = 0x0010
        self.pid = self._get_client_pid(f"{process_name}.exe")
        self.process, self.read_process, self.read_buffer, self.byte_read = self._get_process()
        self.base_address = self._get_base_address()

    @staticmethod
    def _get_client_pid(process_name):
        pid = None
        for proc in psutil.process_iter():
            try:
                if proc.name() == process_name:
                    pid = int(proc.pid)
                    print("Found, PID = ", pid)
                    break
            except psutil.AccessDenied:
                continue
        return pid

    def _get_process(self):
        process = windll.kernel32.OpenProcess(self.PROCESS_QUERY_INFORMATION | self.PROCESS_VM_READ, False, self.pid)
        read_process = windll.kernel32.ReadProcessMemory
        read_buffer = ctypes.c_uint()
        byte_read = ctypes.c_size_t()
        return process, read_process, read_buffer, byte_read

    def _get_base_address(self):
        process_all_access = 0x1F0FFF
        process_handle = win32api.OpenProcess(process_all_access, False, self.pid)
        modules = win32process.EnumProcessModules(process_handle)
        process_handle.close()
        base_addr = modules[0]
        return base_addr

    def read_address(self, address):
        address_2_read = self.base_address + address
        try:
            if self.read_process(self.process, ctypes.c_void_p(address_2_read), ctypes.byref(self.read_buffer),
                                 ctypes.sizeof(self.read_buffer),
                                 ctypes.byref(self.byte_read)):
                return self.read_buffer.value
        except Exception as e:
            print("Error: ", e)
