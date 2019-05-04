import threading
import socket
import hashlib
import base64
import multiprocessing
import os
import time
from multiprocessing import Value, Array
import struct

encoding = 'utf-8'
BUFSIZE = 1024
port = 9011
headers = {}

connection = Value('b', False)


def parse_data(msg):
    v = msg[1] & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = msg[p:p+4]
    data = msg[p+4:]
    return ''.join([chr(v ^ mask[k % 4]) for k, v in enumerate(data)])


def sendMessage(client, message):
    msgLen = len(message)
    backMsgList = []
    backMsgList.append(struct.pack('B', 129))

    if msgLen <= 125:
        backMsgList.append(struct.pack('b', msgLen))
    elif msgLen <= 65535:
        backMsgList.append(struct.pack('b', 126))
        backMsgList.append(struct.pack('>h', msgLen))
    elif msgLen <= (2 ^ 64-1):
        backMsgList.append(struct.pack('b', 127))
        backMsgList.append(struct.pack('>h', msgLen))
    else:
        print("the message is too long to send in a time")
        return
    message_byte = bytes()
    for c in backMsgList:
        message_byte += c
    message_byte += bytes(message, encoding="utf8")

    client.send(message_byte)


def socketServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(0)
    while True:
        client, cltadd = sock.accept()
        data = client.recv(1024)
        cltadd = cltadd
        header, sub = data.split(str("\r\n\r\n").encode(encoding), 1)
        for line in header.split(str('\r\n').encode(encoding))[1:]:
            key, value = line.split(str(': ').encode(encoding), 1)
            headers[key] = value
        key = (bytes.decode(headers[str('Sec-WebSocket-Key').encode(encoding)],
                            encoding) + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode(encoding)
        ser_key = hashlib.sha1(key).digest()
        token = base64.b64encode(ser_key)
        client.send(('\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: {}\r\n\r\n\
'.format(bytes.decode(token, encoding))).encode(encoding))
        multiprocessing.Process(target=systemPara, args=(client,)).start()
        global connection
        connection.value = True
        print("accept a connect from:", client.getpeername())


def receiveData(client):
    while True:
        data = client.recv(1024)
        if(data):
            tmp = parse_data(data)
            print(tmp, "from", client.getpeername())
        else:
            break

    global connection
    connection.value = False
    print("close:", client.getpeername())


def systemPara(client):
    oldTime = time.time()
    while True:
        dataToBeSent = ''
        with open('dataFile.txt','r') as mFile:
            for line in mFile:
                dataToBeSent+=line
        sendMessage(client, dataToBeSent)
        time.sleep(1)


if __name__ == "__main__":
    connection.value = False
    serv = multiprocessing.Process(target=socketServer)
    serv.start()