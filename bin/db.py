
import logging,sqlite3

try:
    conn = sqlite3.connect('tasks.db')
    cur  = conn.cursor()
except Exception,e :
    print e
    exit(1)

def init_db() :
    global conn,cur
    cur.execute("create table tasks ("+
            "task_id varchar(64) UNIQUE,"+
            "created_time varchar(32),"+
            "start_time varchar(32),"+
            "end_time varchar(32),"+
            "realpath varchar(256),"+
            "status integer )")

    cur.execute("create table task_items(" +
            "task_id varchar(64)," +
            "pathname varchar(512),"+
            "filed integer,"+
            "local integer,"+
            "num integer)" 
          )
    conn.commit()
    conn.close()

def query(sql,values=None) :
    global conn,cur
    try :
        if values :
            cur.execute(sql,values)
        else :
            cur.execute(sql)
        conn.commit()
    except Exception,e:
        logging.error(sql)
        logging.error(e)
        return False
    return True

def check_task_id(tid) :
    global conn,cur
    sql = "select * from tasks where task_id='%s'" %tid
    if query(sql) :
        rows = cur.fetchall()
        if len(rows) > 0 :
            return True
    return False
def list_tasks() :
    global conn,cur
    sql = "select * from tasks"
    if query(sql) :
        for row in cur.fetchall():
            print "%s  %s %s %s %d" %(row[0],row[1],row[2],row[3],row[5])

def check_task_item_id(tid,num) :
    global conn,cur
    sql = "select * from task_items where task_id='?' and num='?'"
    if query(sql,[tid,num]) :
        rows = cur.fetchall()
        if len(rows) > 0 :
            return True
    return False

def insert_task(tid,task) :
    sql = "insert into tasks values(?,?,?,?,?,?)"
    return query(sql,task)

def insert_task_item(tid,task_item) :
    sql = "insert into task_items values(?,?,?,?,?)"
    return query(sql,task_item)

if  __name__ == '__main__' :
    init_db()


