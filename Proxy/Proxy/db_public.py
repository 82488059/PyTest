#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
from . import conf
import queue
from . import Pool
import random



def create_proxy_conn():
    print(('public host {}, public db {}'.format(conf.db_public_host, conf.db_public)))
    cx = pymysql.connect(conf.db_public_host, conf.db_public_user_name, conf.db_public_user_pwd, conf.db_public, charset=conf.db_charset, port=conf.db_port)
    return cx


pool = Pool.Pool(create_proxy_conn, 2)


# execute sql
def execute_sql(sql, args=None):
    global pool
    cx = pool.get()
    cu = cx.cursor()
    ret = cu.execute(sql, args)
    cx.commit()
    pool.put(cx)
    return ret  # >= 0


# execute sql
def execute_fetchall(sql, args=None):
    global pool
    cx = pool.get()
    cu = cx.cursor()
    exp = []
    if cu.execute(sql, args):
        exp = cu.fetchall()
    pool.put(cx)
    return exp


# execute sql
def execute_fetchone(sql, args=None):
    global pool
    cx = pool.get()
    cu = cx.cursor()
    exp = []
    if cu.execute(sql, args):
        exp = cu.fetchone()
    pool.put(cx)
    return exp


def get_random_proxy2(limit=120):
    sql = "select proxy from proxy2 where count > 100 order by avg, loss_rate, count desc limit {}".format(
        limit)
    rec = execute_fetchall(sql)
    if not rec:
        print('not find proxy ')
        return False
    total = len(rec)
    i = random.randint(0, total - 1)
    proxy = rec[i][0]
    return proxy


def get_host_queue():
    hosts = get_hosts()
    q = queue.Queue()
    for host in hosts:
        q.put(host[0])
    return q


def get_host_list():
    hosts = get_hosts()
    q = []
    for host in hosts:
        q.append(host[0])
    return q


# add
# proxy2
def proxy2_select():
    sql = "select proxy, count, lost, total from proxy2 order by lost "
    exp = execute_fetchall(sql)
    return exp


def proxy2_select2(proxy):
    sql = "select proxy, count, lost, total from proxy2 where proxy = '{}' ".format(proxy)
    exp = execute_fetchone(sql)
    return exp


def get_proxy2_ip():
    sql = "select proxy from proxy2 order by lost, loss_rate, count desc"
    exp = execute_fetchall(sql)
    return exp


def get_proxy2_ip_queue():
    q = queue.Queue()
    ips = get_proxy2_ip()
    for ip in ips:
        q.put(ip[0])
    return q


# proxy2
def proxy2_insert_or_update(ip, count, lost, total):
    sql = "insert into proxy2 set proxy='{}', count = {}, lost={}, total = {} on duplicate key update count = {}, lost={}, total = {}, loss_rate={}, avg={}".format(
        ip, count, lost, total, count, lost, total, lost * 1.0 / count, total * 1.0 / count)
    return execute_sql(sql)
