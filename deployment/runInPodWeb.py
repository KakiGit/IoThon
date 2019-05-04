import socket
import multiprocessing
#send
UDP_IP = "192.168.1.?" ##service IP
port = 80
MESSAGE = "Fall"
encoding = 'utf-8'
BUFSIZE = 1024
headers = {}

def socketServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(0)
    while True:
        client, cltadd = sock.accept()
        data = client.recv(1024)
        cltadd = cltadd
        with open('iot/index.html','r') as web:
            for line in web:
                client.send(bytes(line.encode(encoding)))
        
        print("accept a connect from:", client.getpeername())

if __name__ == "__main__":
    serv = multiprocessing.Process(target=socketServer)
    serv.start()
    