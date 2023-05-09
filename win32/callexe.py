#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import win32api
import os



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


# 只支持基础类型
def run_runas(name, calls):
    callsstr= json2txt(calls)
    print("run_runas:{},args:{}".format(name, calls))
    res = win32api.ShellExecute(0, 'runas', name, callsstr, '', 0)
    print(res)
    return res 

def call_dll_funcs(data):
    name = data["name"]
    calls=data["calls"]
    msg={"name":name}
    if not name or not calls:
        msg["msg"] = "name or calls不能为空！"
        return False , msg
    if "" == name:
        msg["msg"] = "name or calls不能为空！"
        return False , msg
    try:
        runname = name+".exe"
        res = run_runas(runname, calls)
        msg["msg"] = res
    except BaseException as e:
        msg["msg"]=str(e)
        return False , msg
    return True, msg


def call_exe(mjs):
    if not mjs:
        return False, "空参数"
    print("call={}", mjs)
    msgs = []
    for data in mjs:
        res, msg = call_dll_funcs(data)
        msgs.append(msg)
    print(msgs)
    js = json2txt(msgs)
    print("msg={}".format(js))
    return True, msgs

if __name__ == "__main__":
    args = len(sys.argv)
    if args > 1:
        cmd = sys.argv[1]
    else:
        cmd = '[{"name":"ModVoiIP","calls":"{\'serverAddress\':\'192.168.2.151\',\'netmask\':\'netmask\',\'gateway\':\'gateway\',\'id\':\'1\'}"}]'
        print(cmd)
        os.exit(1)
    mapa = txt2json(cmd)
    call_exe(mapa)
