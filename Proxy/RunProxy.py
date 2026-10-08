#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from Proxy import db_public
from Proxy import Proxy
import MultiTaskRun
from multiprocessing import cpu_count
import queue


BaiduHeader = {'Host': 'www.baidu.com',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
              'Connection': 'Keep-Alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'Referer': 'app:/assets/CardMain.swf',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Cookie': '__jsluid_h=28606fb439ea32758dbacb7cc70dbf91; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1564452517; __jsl_clearance=1564477327.868|0|aoBBpqEmuDsVxzPLEozWdRCXJ6U%3D; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1564477529'
              , 'Accept-Encoding': 'gzip, deflate'
              , 'Accept-Language': 'zh-CN,zh;q=0.9'
              }


def find_new_proxy(tn=0):
    ips = []
    if tn == 0:
        ips = Proxy.get_ip_list_ip66()
    if tn == 1:
        ips = Proxy.get_ip_list_xc(0, 1)
    if tn == 2:
        ips = Proxy.get_ip_list_xc(1, 1)
    if tn == 3:
        ips = Proxy.get_ip_list_xc(2, 1)
    if tn == 4:
        ips = Proxy.get_ip_list_xc(3, 1)
    if tn == 5:
        ips = Proxy.get_ip_list_89ip(100)
    if not ips:
        return True

    url = 'http://www.baidu.com'
    # 测试有没有网
    if Proxy.Http.http_get('http://www.baidu.com', BaiduHeader) is None:
        return True

    test_times = 5
    for proxy in ips:
        info = db_public.proxy2_select2(proxy)
        if info:
            continue
        lost = 0
        count = 0
        total = 0.0
        if Proxy.test_get(proxy, url, BaiduHeader) is None:
            continue
        # 测试proxy
        bt = time.time()
        for x in range(0, test_times):
            if Proxy.test_get(proxy, url, BaiduHeader) is None:
                lost += 1
        et = time.time()
        total += et - bt
        count += test_times
        print('proxy={}, loss rate={}, avg={}, count={} lost={} '.format(proxy, lost * 1.0 / test_times, (et - bt) / test_times, test_times, lost))
        # 丢包了
        if lost >= 1:
            continue
        # 时间长
        if total > 3:
            continue
        db_public.proxy2_insert_or_update(proxy, count, lost, total)
    return True


def test_proxy(proxy):
    test_times = 5
    v = db_public.proxy2_select2(proxy)
    if not v:
        return True
    proxy = v[0]
    count = v[1]
    lost = v[2]
    total = v[3]
    url = 'http://www.baidu.com'
    # 测试有没有网
    if Proxy.Http.http_get('http://www.baidu.com', BaiduHeader) is None:
        return False
    # 测试proxy
    nlost = 0
    bt = time.time()
    for x in range(0, test_times):
        if Proxy.test_get(proxy, url, BaiduHeader) is None:
            nlost += 1
    et = time.time()
    total += et-bt
    count += test_times
    lost += nlost
    db_public.proxy2_insert_or_update(proxy, count, lost, total)
    print('proxy={}, loss rate={}, avg={}, count={} lost={} '.format(proxy, nlost*1.0/test_times, (et-bt)/test_times, test_times, nlost))
    # print('proxy={}, loss rate={}, avg={}, count={} lost={} '.format(proxy, lost*1.0/count, total/count, count, lost))
    return True


def test_proxy_get(proxy=''):
    proxys = db_public.proxy2_select()
    for v in proxys:
        proxy = v[0]
        count = v[1]
        lost = v[2]
        total = v[3]
        url = 'http://www.baidu.com'
        # 测试有没有网
        if Proxy.Http.http_get('http://www.baidu.com', BaiduHeader) is None:
            return 0
        # 测试proxy
        bt = time.time()
        for x in range(0, 5):
            if Proxy.test_get(proxy, url, BaiduHeader) is None:
                lost += 1
        et = time.time()
        total += et-bt
        count += 5
        db_public.proxy2_insert_or_update(proxy, count, lost, total)
    return


def test_proxy_post(proxy=''):
    proxys = db_public.proxy2_select()
    for v in proxys:
        proxy = v[0]
        count = v[1]
        lost = v[2]
        total = v[3]
        url = 'http://www.baidu.com'
        # 测试有没有网
        if Proxy.Http.http_get('http://www.baidu.com', BaiduHeader) is None:
            return 0
        # 测试proxy
        bt = time.time()
        for x in range(0, 5):
            if Proxy.test_post(proxy, url, {}, BaiduHeader) is None:
                lost += 1
        et = time.time()
        total += et-bt
        count += 5
        db_public.proxy2_insert_or_update(proxy, count, lost, total)
    return


if __name__ == "__main__":
    # 对已有的IP进行测试
    q = db_public.get_proxy2_ip_queue()
    MultiTaskRun.multi_thread_run_base_task(q, test_proxy, 4 * cpu_count())

    # 找新的IP并入库
    q = queue.Queue()
    tn = 6  # type
    for x in range(0, tn):
        q.put(x)
    MultiTaskRun.multi_thread_run_base_task(q, find_new_proxy, tn)
