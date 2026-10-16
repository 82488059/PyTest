import os
import pyodbc

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

connect = pyodbc.connect(
    'DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (driver, server, database, user, password)
)
cursor = connect.cursor()
cursor.execute("exec alarm")
row = cursor.fetchone()
if row:
    print(row)
