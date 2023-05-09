import os
import sys 
import time
import pymysql
import queue
import json
import wmi
import win32api
import re
import ctypes


def loadtext(path):
    try:
        f = open(path,"r")
        txt = f.read()
        f.close()
        return txt
    except Exception as e:
        print("load file error! {}".format(path))
        return None
    return None


def writefile(path, text):
    try:
        f = open(path,"w")
        text = f.write(text)
        f.close()
        return True
    except Exception as e:
        print("write file error! {}".format(path))
        return False
    return False

# to json
def txt2json(text):
    try:
        jsondict=json.loads(text)
        return jsondict
    except Exception as e:
        print('json error!')
        return None
    return None

# to txt
def json2txt(jsondict):
    try:
        text=json.dumps(jsondict)
        return text
    except Exception as e:
        print('json error!')
        return None
    return None

def modserverip(mdict):
    intReboot=0
    wmiService = wmi.WMI()
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled=True)
    if len(colNicConfigs)<1:
        print("not find  network adapter")
        return False
    objNicConfig = colNicConfigs[0]
    arrIPAddresses =[mdict['serverAddress']]
    arrSubnetMasks =[mdict['netmask']]
    arrDefaultGateways =[mdict['gateway']]
    arrGatewayCostMetrics =[1]
    #arrDNSServers =['172.16.151.10']
    intReboot =0
    returnValue = objNicConfig.EnableStatic(IPAddress= arrIPAddresses,SubnetMask= arrSubnetMasks)
    if returnValue[0]==0:
        print ('设置IP成功')
    elif returnValue[0]==1:
        print ('设置IP成功')
        intReboot +=1
    else:
        print ('修改IP失败: IP设置发生错误')
        return False
    returnValue = objNicConfig.SetGateways(DefaultIPGateway= arrDefaultGateways,GatewayCostMetric= arrGatewayCostMetrics)
    if returnValue[0]==0:
        print ('设置网关成功')
    elif returnValue[0]==1:
        print ('设置网关成功')
        intReboot +=1
    else:
        print ('修改IP失败: 网关设置发生错误')
        return False
    #returnValue = objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder= arrDNSServers)
    #if returnValue[0]==0:
    #    print ('设置DNS成功')
    #elif returnValue[0]==1:
    #    print ('设置DNS成功')
    #    intReboot +=1
    #else:
    #    print ('修改IP失败: DNS设置发生错误')
    #    return False
    if intReboot >0:
        print ('need reboot computer')
    else:
        print ('修改IP结束')
    return True

# run
def run(cmd, model=0):
    if not is_admin():
        print("runas admin")
        state = runasadmin(cmd)
        print('state {}'.format(state))
        return state  
    jsontext=cmd.replace('\'','\"')
    state=0
    mdict={}
    mdict=txt2json(jsontext)
    if mdict:
        if 0 == model:
            if not modserverip(mdict):
                state = 1
        else: 
            if not modserverip2(mdict):
                state = 1
        setIPevn(mdict['serverAddress'])
    print('state {}'.format(state))
    return state

#设置环境变量
def setIPevn(newIP):
    cmd = "setx {:s} \"{:s}\" /m".format("IDVLOCALIP", newIP)
    os.system(cmd)


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

# 修改IP
def modserverip2(mdict):
    ip = mdict['serverAddress']
    mask = mdict['netmask']
    way = mdict['gateway']
    name = FindFirstNetworkName()
    if not name:
        return False
    cmd = " netsh interface ip set address \"{}\" static {} {} {} 1".format(name, ip , mask, way)
    print(cmd)
    result = os.popen(cmd)
    if not result:
        print(cmd+" -> error!")
        return False
    s = result.read()
    if "" != s:
        print(s)
        return False
    return True

# win10下UAC调到最低，提权时不会弹出UAC框。
def run_runas(name, calls):
    state = 1
    try :
        callsstr= json2txt(calls)
        print("run_runas:{},args:{}".format(name, calls))
        # 参数
        # 父进程句柄  要进行的操作 文件名 参数 文件夹名 显示模式 
        # 具体解释msdn搜索ShellExecute
        # res = win32api.ShellExecute(0, 'runas', name, callsstr, '', 0)
        res = ctypes.windll.shell32.ShellExecuteW(0, "runas", name, callsstr, '', 0)
        print(res)
        if 42 == res:
            state = 0
    except BaseException as e:
        return state, str(e)
    return state 


def runasadmin(jsontext):
    run = sys.argv[0]
    state = run_runas(run, jsontext)
    return state 



def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def test():
    is1 = is_admin()
    return 


if __name__ == "__main__":
    cmd1=""
    model = 0
    args = len(sys.argv)
    if args > 2:
        cmd1 = sys.argv[1]
        model = 1
    elif args > 1:
        cmd1 = sys.argv[1]
        model=0
    else:
        print('this is test code!')
        #cmd1='{"serverAddress":"192.168.2.151","ipEnd":"ipEnd","ipStart":"ipStart","netmask":"netmask","gateway":"gateway","id":"1"}'
        cmd1="{'serverAddress':'192.168.2.151','netmask':'netmask','gateway':'gateway','id':'1'}"
        #os._exit(1)
    print('cmd: {}'.format(cmd1))
    ex = run(cmd1, model)
    os._exit(ex)

