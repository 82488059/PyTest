import urllib2
import time

while True:
    req = urllib2.urlopen('http://localhost/index.php/Home/SendMesg/?ss=3', timeout = 100)
    data = req.read()
    print time.ctime()
    print data
    time.sleep(3)
