#from adodbapi import connect

server = '172.16.10.230'
user = 'sa'
password = 'sqlserverweixin'
database = 'weixin'
sp = 'LOAD_DATA'
station = 'station'
sn = 'sn'

try:
    db = connect('Provider=SQLOLEDB.1;Data Source=%s;Initial Catalog=%s;\
                        User ID=%s;Password=%s;'%(server, database, user, password))
except Exception as e:
    print(e)
else:
    cur = db.cursor()
    msg = cur.callproc(sp, ()) 
    if len(msg) > 1:
        if msg[-1] is None:
            print('sn is ok. Can be test at this station')
        else:
            print(msg[-1])
finally:
    try: db.close()
    except: pass
