
#encoding=utf-8

import pycurl,sys,time
import xml.dom.minidom
from xml.etree import ElementTree

def get_node(task):
    data = {}
    for child in task.getchildren():
        data[child.tag] = child.text
    return data

class writeback :
    def __init__(self):
        self.contents = ''
    def body_callback(self, buf):
        self.contents  = self.contents + buf

def get_server_query(url) :
    try:
        temp = writeback()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, temp.body_callback)
        c.perform()
#       end_time = time.time()
#       duration = end_time - start_time
        c.close()
    except Exception as e:
        print "ERROR %s" % e
        return -1
#   print temp.contents
#    return xml.dom.minidom.parseString(temp.contents)
    return ElementTree.fromstring(temp.contents)


def get_task_ids(status=4) :
    url = "http://11.11.11.71:8080/iamp/enum_Task.websvc?task_status=%d&page_number=1&rows=120" % status
    root = get_server_query(url)
    tasks = root.getiterator('task')
    task_ids = {}
    for task in tasks :
        task_info = get_node(task)
        task_ids[task.attrib['id']] = task_info
    return task_ids

def get_task_item(task_id) :
    url = "http://11.11.11.71:8080/iamp/enum_task_item.websvc?task_id=%s&page_number=1&rows=120" % task_id
    root = get_server_query(url)
    items = root.getiterator('item')
    data = []
    for item in items :
        node = {}
        node['num' ]    = int(item.attrib['num'])
        node['status' ] = int(item.attrib['status'])
        node['errno']   = int(item.attrib['errno'])
        node['path']    = item.text
        data.append(node)
    return data
#   return infos

def get_task_info(task_id) :
    url = "http://11.11.11.71:8080/iamp/query_task_info.websvc?task_id=%s" % task_id
    root = get_server_query(url)
    infos = root.getiterator('task')
    return infos 
