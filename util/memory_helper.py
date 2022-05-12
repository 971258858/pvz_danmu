from string import printable
import ctypes
import ctypes.wintypes
import struct
import psutil
import win32api

MAX_PATH = 260
MAX_MODULE_NAME32 = 255
TH32CS_SNAPMODULE = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010



# 帮助我们识别内存中游戏的基址。然后我们使用这个基址来构建
class MODULEENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', ctypes.c_ulong),
                ('th32ModuleID', ctypes.c_ulong),
                ('th32ProcessID', ctypes.c_ulong),
                ('GlblcntUsage', ctypes.c_ulong),
                ('ProccntUsage', ctypes.c_ulong),
                ('modBaseAddr', ctypes.c_size_t),
                ('modBaseSize', ctypes.c_ulong),
                ('hModule', ctypes.c_void_p),
                ('szModule', ctypes.c_char * (MAX_MODULE_NAME32+1)),
                ('szExePath', ctypes.c_char * MAX_PATH)]


# CreateToolhelp32Snapshot可以通过获取进程信息为指定的进程、进程使用的堆[HEAP]、模块[MODULE]、线程建立一个快照
CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = ctypes.c_long
CreateToolhelp32Snapshot.argtypes = [ctypes.c_ulong, ctypes.c_ulong]

Module32First = ctypes.windll.kernel32.Module32First
Module32First.argtypes = [ctypes.c_void_p, ctypes.POINTER(MODULEENTRY32) ]
Module32First.rettype = ctypes.c_int

CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = [ctypes.c_void_p]
CloseHandle.rettype = ctypes.c_int

ReadProcessMemory = ctypes.WinDLL('kernel32', use_last_error=True).ReadProcessMemory
ReadProcessMemory.argtypes = [ctypes.wintypes.HANDLE, ctypes.wintypes.LPCVOID,
                              ctypes.wintypes.LPVOID, ctypes.c_size_t,
                              ctypes.POINTER(ctypes.c_size_t)]
ReadProcessMemory.restype = ctypes.wintypes.BOOL


class ReadMemory:
    def __init__(self, exe_name: str):
        self.exe = exe_name
        self.pid = self._get_process_id().pid
        self.patch = self._get_process_id().cwd()
        self.handle = self._get_process_handle()
        self.base_address = self._get_base_address()
        # 游戏基址

    def _get_process_id(self):
        # 正在运行的进程列表psutil.process_iter()
        for proc in psutil.process_iter():
            if self.exe in proc.name():
                return proc
        raise Exception(f"Cannot find executable with name: {self.exe}")

    def _get_process_handle(self):
        try:
            # 打开现有的本地进程对象
            return ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION
                                                      | PROCESS_VM_READ,
                                                      False, self.pid)
        except Exception as e:
            raise Exception(f"Cannot create handle for pid {self.pid}: "
                            f"Error: {str(e)}")

    def _get_base_address(self):
        h_module_snap = ctypes.c_void_p(0)
        me_32 = MODULEENTRY32()

        me_32.dwSize = ctypes.sizeof(MODULEENTRY32)  # pylint: disable=invalid-name, attribute-defined-outside-init)
        h_module_snap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE |
                                                 TH32CS_SNAPMODULE32, self.pid)
        ret = Module32First(h_module_snap, ctypes.byref(me_32))

        if ret == 0:
            print('Error on Thread32First')
            return False

        ret = Module32First(h_module_snap, ctypes.pointer(me_32))
        if ret == 0:
            print('ListProcessModules() Error on Module32First')

        return me_32.modBaseAddr

    def read_bytes(self, address: int, byte: int) -> bytes:
        if not isinstance(address, int):
            raise TypeError('Address must be int: {}'.format(address))
        buff = ctypes.create_string_buffer(byte)
        bytes_read = ctypes.c_size_t()
        ctypes.windll.kernel32.SetLastError(0)
        ReadProcessMemory(self.handle, ctypes.c_void_p(address),
                          ctypes.byref(buff), byte, ctypes.byref(bytes_read))
        error_code = ctypes.windll.kernel32.GetLastError()
        if error_code:
            print("Error")
            ctypes.windll.kernel32.SetLastError(0)
        raw = buff.raw
        return raw

    def read_int(self, address: int):
        read_bytes = self.read_bytes(address, struct.calcsize('i'))
        read_bytes = struct.unpack('<i', read_bytes)[0]
        return read_bytes

    def read_float(self, address: int) -> float:
        read_bytes = self.read_bytes(address, struct.calcsize('f'))
        read_bytes = struct.unpack('<f', read_bytes)[0]
        return read_bytes

    def read_ulong(self, address: int):
        # 4 bytes address
        read_bytes = self.read_bytes(address, struct.calcsize('L'))
        read_bytes = struct.unpack('<L', read_bytes)[0]
        return read_bytes

    def read_ptr(self, address: int) -> int:
        # 8 bytes address
        read_bytes = self.read_bytes(address, struct.calcsize('Q'))
        read_bytes = struct.unpack('<Q', read_bytes)[0]
        return read_bytes

    def read_string(self, address: int, byte: int = 50) -> int:
        buff = self.read_bytes(address, byte)
        # print(type(buff))
        i = buff.find(b'\x00')
        return str("".join(map(chr, buff[:i])))

    def read_name_string(self, address: int, byte: int = 32) -> int:
        buff = self.read_bytes(address, byte)
        i = buff.find(b"\x00\x00\x00")
        joined = str("".join(map(chr, buff[:i])))
        return ''.join(char for char in joined if char in printable)

    def set_int(self, address: int, num: int):
        PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
        # 找窗体

        # 以最高权限打开进程
        p = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        # 加载内核模块
        md = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32")
        data = ctypes.c_long()
        # 读取内存
        md.ReadProcessMemory(int(p), address, ctypes.byref(data), 4, None)
        # 新值
        newData = ctypes.c_long(num)
        # 修改
        md.WriteProcessMemory(int(p), address, ctypes.byref(newData), 4, None)
        win32api.CloseHandle(p)

    def set_bytes(self, address: int, byte: int, change: int) -> bytes:
        PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
        # 找窗体

        # 以最高权限打开进程
        p = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        # 加载内核模块
        md = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\kernel32")
        data = ctypes.c_size_t()
        # 读取内存
        md.ReadProcessMemory(int(p), ctypes.c_void_p(address), ctypes.byref(data), byte, None)
        # 新值
        newData = ctypes.c_size_t(change)
        # 修改
        md.WriteProcessMemory(int(p), ctypes.c_void_p(address), ctypes.byref(newData), byte, None)
        win32api.CloseHandle(p)
