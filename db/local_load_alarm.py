# -*- coding: UTF-8 -*-

import os
import pyodbc
import time
import datetime

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
driver = _cfg('DB_DRIVER', '{SQL Server}')

if not all([server, user, password]):
    raise SystemExit(
        'Missing DB credentials. Set DB_SERVER/DB_USER/DB_PASSWORD '
        '(and optional DB_DATABASE/DB_DRIVER) in the environment or in conf.py '
        '(see conf.py.example).'
    )

print(datetime.datetime.now())

d1 = datetime.datetime.now()
connect = pyodbc.connect(
    'DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (driver, server, database, user, password)
)
cursor = connect.cursor()

while True:
    d2 = datetime.datetime.now()
    # 一小时重启一次
    if d2.hour - d1.hour > 0:
        print(datetime.datetime.now())
        break

    cursor.execute("exec alarm")
    row = cursor.fetchone()
    # print row
    print(datetime.datetime.now())

    time.sleep(1)
