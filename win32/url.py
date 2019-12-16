import urllib.request, urllib.error, urllib.parse
import time

while True:
    req = urllib.request.urlopen('http://localhost/index.php/Home/SendMesg/?ss=3', timeout = 100)
    data = req.read()
    print(time.ctime())
    print(data)
    time.sleep(3)
