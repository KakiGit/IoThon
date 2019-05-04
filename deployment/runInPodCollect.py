import socket

#send
UDP_PORT = 9011

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind(('0.0.0.0', UDP_PORT))
database = {}

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    ip, hostname = data.split(',')[0],data.split(',')[1]
    if ip in database.keys():
        database[ip] = database[ip] + 1
    else:
        database[ip] = 1
    with open('dataFile.txt','w') as mFile:
        for k,v in database:
            mFile.write(hostname+' '+k+' '+v)

    print(database)