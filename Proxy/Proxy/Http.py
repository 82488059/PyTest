#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from io import StringIO
import gzip
import requests
import http.client


def http_proxy_post(url, body, header, proxy, timeout=5):
    try:
        sess = requests.session()
        sess.proxies = {'http': proxy, 'https': proxy}
        req = sess.post(url, body, headers=header, timeout=timeout)
        text = req.text
        if req.status_code == 200:
            if req.encoding == 'gzip':
                stream = StringIO(req.text)
                gzipper = gzip.GzipFile(fileobj=stream)
                text = gzipper.read()
            return text
        return text
    except Exception as e:
        return None


def http_proxy_get(url, header, proxy, timeout=5):
    try:
        sess = requests.session()
        sess.proxies = {'http': proxy, 'https': proxy}
        req = sess.get(url, headers=header, timeout=timeout)
        text = req.text
        if req.status_code == 200:
            if req.encoding == 'gzip':
                stream = StringIO(req.text)
                gzipper = gzip.GzipFile(fileobj=stream)
                text = gzipper.read()
            return text
        return text
    except Exception as e:
        return None


def http_post(url, body, header, timeout=5):
    try:
        sess = requests.session()
        req = sess.post(url, data=body, headers=header, timeout=timeout)
        text = req.text
        if req.status_code == 200:
            if req.encoding == 'gzip':
                stream = StringIO(req.text)
                gzipper = gzip.GzipFile(fileobj=stream)
                text = gzipper.read()
            return text
        return text
    except Exception as e:
        return None


def http_get(url, header, timeout=5):
    try:
        sess = requests.session()
        req = sess.get(url, headers=header, timeout=timeout)
        text = req.text
        if req.status_code == 200:
            if req.encoding == 'gzip':
                stream = StringIO(req.text)
                gzipper = gzip.GzipFile(fileobj=stream)
                text = gzipper.read()
            return text
        return text
    except Exception as e:
        return None


def http_get_ex(url, body, header, timeout=5):
    try:
        sess = requests.session()
        req = sess.get(url, data=body, headers=header, timeout=timeout)
        text = req.text
        if req.status_code == 200:
            if req.encoding == 'gzip':
                stream = StringIO(req.text)
                gzipper = gzip.GzipFile(fileobj=stream)
                text = gzipper.read()
            return text
        return text
    except Exception as e:
        return None


def http_get2(host, url, body, header):
    try:
        conn = http.client.HTTPConnection(host, None, None, 20)
        conn.request("GET", url, body, header)
        res = conn.getresponse()
        res_str = res.read()
        encoding = res.getheader('Content-Encoding')
        conn.close()
        if encoding == 'gzip':
            stream = StringIO(res_str)
            gzipper = gzip.GzipFile(fileobj=stream)
            res_str = gzipper.read()
        return res_str
    except Exception:
        return None