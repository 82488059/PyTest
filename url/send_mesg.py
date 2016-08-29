import urllib2
import time
import datetime
print "send message running"
print datetime.datetime.now()

d1 = datetime.datetime.now()

while True:
    d2 = datetime.datetime.now()
    if d2.hour - d1.hour > 0:
        print datetime.datetime.now()
        break
    req = urllib2.urlopen('http://localhost/index.php/Home/SendMesg/?ss=3', timeout = 1000)
    data = req.read()
    print datetime.datetime.now()
    # print data
    time.sleep(1)

