
import sys
import psutil
import ctypes
from ctypes import *
import win32api
import time
PAGE_EXECUTE_READWRITE = 0x00000040
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

kernel32 = windll.kernel32
pName = 'plantsvszombies.exe'
shellcode = b"\x60\x9c\xb9\x38\x9f\x6a\x00\x8b\x09\x81\xc1\x68\x07\x00\x00\x8b\x09\x81\xc1\x60\x01\x00\x00\x8b\x09\xb8\x02\x00\x00\x00\x6a\x08\x6a\x00\xbe\xf0\xa0\x42\x00\xff\xd6\x6a\x02\x6a\x04\x6a\x50\x68\x00\x04\x00\x00\xb9\x38\x9f\x6a\x00\x8b\x09\x81\xc1\x68\x07\x00\x00\x8b\x09\xbe\x10\xcb\x40\x00\xff\xd6\x9d\x61\xc3"
# 生成僵尸和阳光
code_size = len(shellcode)  # 默认数据

TH32CS_SNAPPROCESS = 0x00000002

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_ulong),
                ("cntUsage", ctypes.c_ulong),
                ("th32ProcessID", ctypes.c_ulong),
                ("th32DefaultHeapID", ctypes.c_ulong),
                ("th32ModuleID", ctypes.c_ulong),
                ("cntThreads", ctypes.c_ulong),
                ("th32ParentProcessID", ctypes.c_ulong),
                ("pcPriClassBase", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("szExeFile", ctypes.c_char * 260)]

class ZombieCall:
    def __init__(self, x, y, mytype):
        # 类型不能为3、7、8、9、11、12、13、14、15、17
        self.created_zombie(x, y, mytype)
        procPid = int(self.getProcName(pName))
        print("pid", procPid)

        # Get a handle to the process we are injecting into.

        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, procPid)
        print("句柄", h_process)
        if not h_process:
            print
            "[*] Couldn't acquire a handle to PID"
            sys.exit(0)

        # Allocate some space for the shellcode

        arg_address = kernel32.VirtualAllocEx(h_process, 0, code_size, VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
        # Write out the shellcode
        written = c_int(0)

        print("修改内存", kernel32.WriteProcessMemory(h_process, arg_address, shellcode, code_size, byref(written)))
        # Now we create the remote thread and point it's entry routine

        # to be head of our shellcode
        thread_id = c_ulong(0)
        print("arg_address", hex(arg_address), h_process)
        hThread = kernel32.CreateRemoteThread(h_process, None, code_size, arg_address, None, 0, byref(thread_id))
        win32api.CloseHandle(hThread)
        # print(kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x4000))
        win32api.CloseHandle(h_process)

    def created_zombie(self, x, y, mytype):
        zombie_x = self.int_to_hex(x)
        zombie_y = self.int_to_hex(y)
        zombie_type = self.int_to_hex(mytype)
        global shellcode, code_size
        shellcode = b"\x60\x9c\xb9\x38\x9f\x6a\x00\x8b\x09\x81\xc1\x68\x07\x00\x00\x8b\x09\x81\xc1\x60\x01\x00\x00\x8b\x09\xb8"+zombie_x+b"\x00\x00\x00\x6a"+zombie_y+b"\x6a"+zombie_type+b"\xbe\xf0\xa0\x42\x00\xff\xd6\x6a\x02\x6a\x04\x6a\x50\x68\x00\x04\x00\x00\xb9\x38\x9f\x6a\x00\x8b\x09\x81\xc1\x68\x07\x00\x00\x8b\x09\xbe\x10\xcb\x40\x00\xff\xd6\x9d\x61\xc3"
        code_size = len(shellcode)

    def int_to_hex(self, num):
        # 目前支持0~39
        bytesList = [b"\x00", b"\x01", b"\x02", b"\x03", b"\x04", b"\x05", b"\x06", b"\x07", b"\x08", b"\x09",
                     b"\x0a", b"\x0b", b"\x0c", b"\x0d", b"\x0e", b"\x0f", b"\x10", b"\x11", b"\x12", b"\x13",
                     b"\x14", b"\x15", b"\x16", b"\x17", b"\x18", b"\x19", b"\x1a", b"\x1b", b"\x1c", b"\x1d",
                     b"\x1e", b"\x1f", b"\x20", b"\x21", b"\x22", b"\x23", b"\x24", b"\x25", b"\x26", b"\x27"]
        return bytesList[num]

    def getProcName(self, pname):
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == pname:
                    return str(proc).split('=')[1].split(',')[0]  # return if found one
            except psutil.AccessDenied:
                pass
            except psutil.NoSuchProcess:
                pass
        return None
