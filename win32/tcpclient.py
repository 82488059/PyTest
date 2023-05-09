

import socket
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.200",8888))
 
 
while True:
    data = '[{"name":"ModVoiIP","calls":"{\'serverAddress\':\'192.168.2.151\',\'netmask\':\'netmask\',\'gateway\':\'gateway\',\'id\':\'1\'}"}]'
    data = "[{\"name\":\"ModVoiIP\",\"calls\":\"{\\'serverAddress\\':\\'192.168.2.151\\',\\'netmask\\':\\'netmask\\',\\'gateway\\':\\'gateway\\',\\'id\\':\\'1\\'}\"}]"
    sd = data.encode("utf-8")
    client.send(sd)
    info = client.recv(1024)
    print("服务器说：",info)
    break
