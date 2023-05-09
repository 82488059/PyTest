import ctypes
import win32com.client
import win32gui, win32api, pywintypes
import os
import win32process  
import re

WMI = win32com.client.GetObject('winmgmts:')
kernel32 = ctypes.windll.kernel32

TH32CS_SNAPTHREAD = 0x00000004

class THREADENTRY32(ctypes.Structure): 
    _fields_ = [
              ("dwSize", ctypes.c_ulong), 
              ("cntUsage", ctypes.c_ulong), 
              ("th32ThreadID", ctypes.c_ulong), 
              ("th32OwnerProcessID", ctypes.c_ulong), 
              ("tpBasePri", ctypes.c_long), 
              ("tpDeltaPri", ctypes.c_long), 
              ("dwFlags", ctypes.c_ulong)] 
    

def EnumerateThreads(processId):
    threadEntry = THREADENTRY32()
    
    threadList = []
    threadSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, processId)
    if threadSnap is not None:
        threadEntry.dwSize = ctypes.sizeof(threadEntry)
        success = kernel32.Thread32First(threadSnap, ctypes.byref(threadEntry))
        if not success:
            print ('Failed getting first process.')
        
        while success:
            if threadEntry.th32OwnerProcessID == processId:
                threadList.append(threadEntry.th32ThreadID)
            success = kernel32.Thread32Next(threadSnap, ctypes.byref(threadEntry))
        
        kernel32.CloseHandle(threadSnap)
    return threadList

def EnumerateProcesses(processName):
    processList = WMI.ExecQuery("SELECT * FROM Win32_Process where name = '%s'"%processName)
    return processList


def SearchWindowHandleIdIdByCaption(processName ,caption):
    processList = EnumerateProcesses(processName)
    for process in processList:
        for thread in EnumerateThreads(long(process.Handle)):
            windows = []
            win32gui.EnumThreadWindows(thread, lambda hwnd, resultList: resultList.append(hwnd), windows)
            for windowIdi in windows:
                text = win32gui.GetWindowText(windowIdi) 
                text = text.__str__()
                caption = caption.__str__()
                if caption in text:
                    return [windowIdi, process.Handle]
    return [None, None]
                    
import wmi
c = wmi.WMI ()
def print_process():
    for process in c.Win32_Process ():
        print(process.ProcessId, process.Name, process.derivation)
        
def cmd():
    #v = os.system("cmd.exe") 
    #print (v )
    win32api.ShellExecute(0, 'open', 'cmd.exe', '', '', 1) 
    #win32process.CreateProcess('C:\\Windows\\cmd.exe', '', None, None, 0, win32process.CREATE_NO_WINDOW,  None, None, win32process.STARTUPINFO())  

# 匹配中文网卡名，取第一块网卡名
def FindFirstNetworkName():
    result = os.popen("ipconfig")
    if not result:
        print("cmd ipconfig error!")
        return ""
    s = result.read()
    if not s:
        print("ipconfig result error!")
        return ""
    # print(s)
    pattern = re.compile("以太网适配器 (.*):")   # 查找数字
    finds = re.findall(pattern, s)
    resname = ""
    for name in finds: 
        # 路过虚拟网卡
        if -1 != name.find("VMnet"):
            continue
        resname = name 
        break
    return resname


if __name__ == "__main__":
    FindFirstNetworkName()
    print("xxx")
    cmd()
    print_process()