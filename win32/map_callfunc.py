import ctypes

mapa={}
mapa["add"]=[1,4]
mapa["sub"]=[5,2]
mapa["add3"]=[2,3,5]

mapb={}
mapb["add"]={"a":1,"b":4}
mapb["sub"]={"a":5,"b":2}
mapb["add3"]={"a":2,"b":3,"c":5}


def test_map_namecall():
    print("test")
    for name in mapa:
        res = eval(name)(*mapa[name])
        print("{} {} {}".format(name,mapa[name],res))

    print("test2")
    for name in mapa:
        res = eval(name)(**mapb[name])
        print("{} {} {}".format(name,mapb[name],res))
    return None

def add(a,b):
    return a+b

def sub(a,b):
    return a+b

def add3(a,b,c):
    return a+b+c

if __name__ == "__main__":
    test_map_namecall()


