import socket
import json
import re
while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.114.151',55555))

    message = s.recv(2048)
    print(message)
    msg = str(message)
    lines=msg[2:]
    lin =lines[:-1]
    #print(lin)

    data_out = json.loads(lin)
    print(data_out)
    TS1 = data_out["TS1"]
    #print("TS1 Angle  : ",TS1["Angle"])
    #print("TS1 xp1  : ", TS1["xp1"])
    #print("Heading : ",data_out["Haeding"])
    #print("Angle : ",data_out["Angle"])