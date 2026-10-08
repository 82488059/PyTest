#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from io import StringIO
import gzip
import re
from Proxy import db_public
from Proxy import Http


MainHeader = {'Host': 'www.66ip.cn',
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


# ip66代理
# http://www.66ip.cn
def get_ip_list_ip66():
    ss = 'http://www.66ip.cn/mo.php?getnum=100&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'
    ss = 'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
    MainHeader['Referer'] = 'http://www.66ip.cn/pt.html'
    ret = Http.http_get(ss, MainHeader)
    # host = 'www.66ip.cn'
    # url = 'mo.php'
    # body = 'getnum=10&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'
    # ret = http.http_get2(host, url, body, MainHeader)
    if ret:
        pattern = '(\d*\.\d*\.\d*\.\d*:[1-9]\d*)'
        string = ret
        ips = re.findall(pattern, string, flags=0)
        # for x in ips:
        #    DebugPrint(x)
        return ips
    return []


# 西祠代理
# https://www.xicidaili.com/wt/1
# https://www.xicidaili.com/nt/
# 0http 1普通 2高匿 3https
def get_ip_list_xc(t=0, page=1):
    url = 'https://www.xicidaili.com/wt/{}'.format(page)
    if 1 == t:
        url = 'https://www.xicidaili.com/nt/{}'.format(page)
    elif 2 == t:
        url = 'https://www.xicidaili.com/nn/{}'.format(page)
    elif 3 == t:
        url = 'https://www.xicidaili.com/wn/{}'.format(page)

    ret = Http.http_get(url, MainHeader)
    if ret:
        # <td>113.121.22.211</td>
        # <td>9999</td>
        pattern = '<td>(\d*\.\d*\.\d*\.\d*)</td>\s*<td>(\d*)</td>'
        string = ret
        ipst = re.findall(pattern, string, flags=0)
        ips = []
        for x in ipst:
            ips.append(x[0]+':'+x[1])
            # print(x)
        return ips
    return []


# 89ip代理
# http://www.89ip.cn/
# http://www.89ip.cn/tqdl.html?num=30&address=&kill_address=&port=&kill_port=&isp=
def get_ip_list_89ip(num=100):
    ss = 'http://www.89ip.cn/tqdl.html?num={}&address=&kill_address=&port=&kill_port=&isp='.format(num)
    ss = 'http://www.89ip.cn/tqdl.html?api=1&num={}&port=&address=&isp='.format(num)
    MainHeader['Host'] = 'www.89ip.cn'
    ret = Http.http_get(ss, MainHeader)
    # host = 'www.66ip.cn'
    # url = 'mo.php'
    # body = 'getnum=10&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'
    # ret = http.http_get2(host, url, body, MainHeader)
    if ret:
        pattern = '(\d*\.\d*\.\d*\.\d*:[1-9]\d*)'
        string = ret
        ips = re.findall(pattern, string, flags=0)
        # for x in ips:
        #    DebugPrint(x)
        return ips
    return []


def test_post(proxy_ip, url, body, header, TIMEOUT=5):
    text = Http.http_proxy_post(url, body, header, proxy_ip, TIMEOUT)
    return text


def test_get(proxy_ip, url, header, TIMEOUT=5):
    text = Http.http_proxy_get(url, header, proxy_ip, TIMEOUT)
    return text


def test_post_times(ip, host, url, body, header, times):
    if times <= 0:
        times = 5
    bt = time.time()
    for x in (0, times):
        url = 'http://' + host + url
        if not test_post(ip, url, body, header):
            print('test {} time {}'.format(x, time.time()-times))
            return 99
    avg = (time.time() - bt) / times
    return avg

