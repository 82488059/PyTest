#from adodbapi import connect
import os

try:
    import conf as _conf
except ImportError:
    _conf = None

def _cfg(name, default=''):
    if _conf is not None and hasattr(_conf, name):
        val = getattr(_conf, name)
        if val not in (None, ''):
            return val
    return os.environ.get(name, default)

server = _cfg('DB_SERVER')
user = _cfg('DB_USER')
password = _cfg('DB_PASSWORD')
database = _cfg('DB_DATABASE', 'weixin')
sp = 'LOAD_DATA'
station = 'station'
sn = 'sn'

if not all([server, user, password]):
    raise SystemExit(
        'Missing DB credentials. Set DB_SERVER/DB_USER/DB_PASSWORD '
        '(and optional DB_DATABASE) in the environment or in conf.py '
        '(see conf.py.example).'
    )

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
