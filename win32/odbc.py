import pyodbc

connect = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.184;DATABASE=weixin;UID=sa;PWD=REDACTED')
cursor = connect.cursor()
cursor.execute("exec alarm")
row = cursor.fetchone()
if row:
    print row
