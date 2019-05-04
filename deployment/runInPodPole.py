import socket
import netifaces as ni
import os
ip = ni.ifaddresses('net1@if2')[ni.AF_INET][0]['addr']
hostname = os.environ['HOSTNAME']
#send
UDP_IP = "192.168.1.51" ##service IP
UDP_PORT = 9011
MESSAGE = "Fall"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP



sock.bind(('0.0.0.0', UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print("?????")

    sock.sendto(bytes((str(ip)+','+str(hostname)).encode('utf8')),(UDP_IP,UDP_PORT)) # buffer size is 1024 bytes
    