# -*- coding: UTF-8 -*-

import pyodbc
import time
import datetime
print(datetime.datetime.now())

d1 = datetime.datetime.now()
# 服务器配置
# connect = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.184;DATABASE=weixin;UID=sa;PWD=123456')
# 本机配置
connect = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.184;DATABASE=weixin;UID=sa;PWD=123456')
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

    

