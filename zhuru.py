
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


shellcode = b"\xb9\x38\x9f\x6a\x00\x8b\x09\x81\xc1\x68\x07\x00\x00\x8b\x09\x81\xc1\x60\x01\x00\x00\x8b\x09\xb8\x02\x00\x00\x00\x6a\x08\x6a\x00\xbf\xf0\xa0\x42\x00\xff\xd7\xc3"


code_size = len(shellcode)

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


def getProcName(pname):
    """ get process by name

    return the first process if there are more than one
    """
    for proc in psutil.process_iter():

        try:

            if proc.name().lower() == pname:
                return str(proc).split('=')[1].split(',')[0]  # return if found one
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return None


procPid = int(getProcName(pName))
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
print("arg_address", arg_address, h_process)
hThread = kernel32.CreateRemoteThread(h_process, None, code_size, arg_address, None, 0, byref(thread_id))
# win32api.CloseHandle(hThread)
# kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
# win32api.CloseHandle(h_process)
