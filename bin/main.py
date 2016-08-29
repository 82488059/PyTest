#/bin/env python

#encoding=utf-8
import logging,log,db
import pycurl,sys,time,os
import xml.dom.minidom  

from xml.etree import ElementTree
import iamp
ERRORS = ["NONE-0", "QUEUE","OK","RUNING","COMPLETED","STOP","NONE-6","COMPLETE WITH WRONG"]
HOME="/home/users"

task_completes = iamp.get_task_ids(4)
task_completes_with_wrong = iamp.get_task_ids(7) 
mega_tasks = task_completes.copy()
mega_tasks.update(task_completes_with_wrong)

for tid,task in mega_tasks.items():
    if db.check_task_id(tid) :
     #  logging.info("TASK ID: %s , DO IT BEFORE." % tid)
        continue
    if not task['param_a'] :
        logging.info("TASK ID: %s , No Items Found " % tid )
        continue
    node = [tid,task['created_time'][0:19],task['begin_time'][0:19],task['end_time'][0:19],
          HOME+task['param_a'],task['status']]
    if db.insert_task(tid,node) :
        logging.info("INSERT TASK RECORD ID : %s" % tid )
    
    nodes = iamp.get_task_item(tid)
    logging.info("TASK ID: %s , Find records (%d) " % (tid,len(nodes)) )
    logging.info("Created_time : %s  , begin_time %s , end_time : %s " % ( 
          task['created_time'][0:19],task['begin_time'][0:19],task['end_time'][0:19]))
    logging.info("Source pathname : %s " % task['param_a'])

    for node in nodes :
         pathname = HOME+"/%s/%s" % ( task['param_a'] , node['path'])
         status = int(node['status'])
         
         if os.path.exists(pathname) :
             logging.info("Archived %s %s , LOCAL existed." % ( pathname, ERRORS[status]))
             try:
                 os.remove(pathname)
                 local = 2
                 logging.info("remove local file : %s ok " % pathname)
             except :
                 local= 1
                 logging.error("remove local file : %s fail "%pathname)
         else :
             local = 0
             logging.info("archived %s %s , LOCAL removed." % ( pathname, ERRORS[status]))
         item = tid,pathname,status,local,node['num']
         db.insert_task_item(tid,item)
