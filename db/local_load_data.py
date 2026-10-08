# -*- coding: UTF-8 -*-

import pyodbc
import time
import datetime

d1 = datetime.datetime.now()
# 服务器配置
# connect = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.184;DATABASE=weixin;UID=sa;PWD=123456')
# 本机配置
connect = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.184;DATABASE=weixin;UID=sa;PWD=123456')
cursor = connect.cursor()

print("load data running")
print(datetime.datetime.now())

d1 = datetime.datetime.now()
#
while True:
    d2 = datetime.datetime.now()
    # 5分钟重启一次
    if d2.minute - d1.minute > 4:
        print(datetime.datetime.now())
        break
    cursor.execute("exec load_data")
    row = cursor.fetchone()
    # print row
    print(datetime.datetime.now())
    time.sleep(1)
