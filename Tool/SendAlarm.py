import HTMLParser
import urllib
import sys
import time
url = "http://3.showweixin.sinaapp.com/Home/SendMesg"
urlText = []
# class parseText(HTMLParser. HTMLParser):
#     def handle_data(self, data):
#         if data != '\n':
#             urlText.append(data)
#             lParser = parseText()
#             lParser.feed(urllib.urlopen(url).read())
#             lParser.close()
#             fp = open("/home/zhou/web text.txt","w")
#             for item in urlText:
#                 print item
#             fp.write(item)
#             fp.close()
data = time.strftime("%d/%m/%Y")


def run():
    for i in xrange(0, 24*60*20):
        td = time.strftime("%d/%m/%Y")
        if td != data:
            return

        nt = time.strftime("%H:%M:%S")
        if nt >= "23:59:55":
            return

        time.sleep(3)
        from urllib import urlopen
        urlopen("http://3.showweixin.sinaapp.com/Home/SendMesg").read()

    return
