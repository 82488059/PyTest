import ctypes
import json

from ctypes import *

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

mapa={}
mapa["add"]=[1,4]
mapa["sub"]=[5,2]
mapa["add3"]=[2,3,5]

mapb={}
mapb["add"]={"a":1,"b":4}
mapb["sub"]={"a":5,"b":2}
mapb["add3"]={"a":2,"b":3,"c":5}


def call_func(obj, name, params, types, restype=None):
    try:
        funcname="obj."+name
        strtypes=""        
        args=[]
        for i in range(len(params)):
            args.append(params[i])
            if strtypes=="":
                strtypes=types[i]
            else:
                strtypes=strtypes+","+types[i]
        if "" != strtypes:
            strtypes="["+strtypes+"]"
            sss = funcname+".argtypes="+strtypes
            # 设置参数类型
            exec(sss)
        if restype:
            sss = funcname+".restype="+restype
            # 设置返回类型
            exec(sss)
        # 调用函数
        res = eval(funcname)(*args)
        print("{} {} {} ".format(funcname,params,res))
    except BaseException as e:
        print(e)
        return False, str(e)
    return True , res

def call_dll_funcs(data):
    path = data["path"]
    dll = data["dll"]
    calls=data["calls"]
    msg={"dll":dll}
    if not dll or not path:
        msg["msg"] = "dll or path不能为空！"
        return False , msg
    if "" == dll or "" ==  path:
        msg["msg"] = "dll or path不能为空！"
        return False , msg
    msg ={}
    try:
        obj = ctypes.cdll.LoadLibrary(path)
        for name in calls:
            params = calls[name].get("params")
            types = calls[name].get("types")
            restype = calls[name].get("restype")
            if not params or not types:
                msg["msg"] = "params or types不能为空！"
                return False , msg
            if len(params) != len(types):
                msg["msg"] = "params and types数量不等！"
                return False , msg

            flg, res = call_func(obj, name, params, types, restype)
            # print("{} {} {} {}".format(name,params, types,res))
            msg[name]={}
            if flg:
                msg[name]["res"] = res
            else:
                msg[name]["msg"] = res
    except  BaseException as e:
        msg["msg"]=str(e)
        return False , msg
    return True, msg


def test_loaddll2(mjs):
    if not mjs:
        return
    print("call={}", mjs)
    msgs = {}
    for index in mjs:
        data = mjs[index]
        res, msg = call_dll_funcs(data)
        # print(msg)
        msgs[index]=msg
    print(msgs)
    js = json2txt(msgs)
    print("msg={}".format(js))
    return msgs

if __name__ == "__main__":
    js = '{"d1":{"dll":"dynamic.dll","path":"./dynamic.dll","calls":{"addf":{"params":[1.1,2.2],"types":["c_float","c_float"],"restype":"c_float"},"add":{"params":[1,2],"types":["c_int","c_int"],"restype":"c_int"},"sub":{"params":[1,2],"types":["c_int","c_int"]},"add3":{"params":[1,2,3],"types":["c_int","c_int","c_int"]} } } }'

    mapa = txt2json(js)
    test_loaddll2(mapa)

    # test_loaddll()
