#coding=utf8

import os
import pymssql

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

host = _cfg('DB_SERVER', 'localhost')
user = _cfg('DB_USER')
password = _cfg('DB_PASSWORD')
database = _cfg('DB_DATABASE', 'weixin')

if not all([user, password]):
    raise SystemExit(
        'Missing DB credentials. Set DB_USER/DB_PASSWORD '
        '(and optional DB_SERVER/DB_DATABASE) in the environment or in conf.py '
        '(see conf.py.example).'
    )

conn = pymssql.connect(host=host, user=user, password=REDACTED database=database, charset="utf8")
cur = conn.cursor()
cur.execute('CREATE TABLE persons(id INT, name VARCHAR(100))')
cur.executemany("INSERT INTO persons VALUES(%d, xinos.king)", \
    [ (1, 'John Doe'), (2, 'Jane Doe') ])
conn.commit()  # you must call commit() to persist your data if you don't set autocommit to True

cur.execute('SELECT * FROM persons WHERE salesrep=xinos.king', 'John Doe')
row = cur.fetchone()
while row:
    print("ID=%d, Name=xinos.king" % (row[0], row[1]))
    row = cur.fetchone()

# if you call execute() with one argument, you can use % sign as usual
# (it loses its special meaning).
cur.execute("SELECT * FROM persons WHERE salesrep LIKE 'J%'")

conn.close()
