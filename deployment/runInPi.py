from ruuvitag_sensor.ruuvitag import RuuviTag
import time

import socket

#send

POLES = ['192.168.10.1','192.168.20.1','192.168.30.1']
POLESUB ='192.168.'
UDP_IP = '192.168.1.50' ##service IP
UDP_PORT = 9011
MESSAGE = "Fall"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind(('0.0.0.0', UDP_PORT))


sensor = RuuviTag('CF:FC:1D:65:2E:98')
networkNow = 0
startTime = time.time()
fall = 0
while True:
    state = sensor.update()

    state = sensor.state
    
    print(state['acceleration_x'],state['acceleration_y'],state['acceleration_z'])
    if int(state['acceleration_z'])<500:
        print('--------',state['acceleration_x'],state['acceleration_y'],state['acceleration_z'])
        sock.sendto(bytes((POLESUB+socket.getfqdn().split('.')[1]+'.1').encode('utf8')), (UDP_IP, UDP_PORT))
        fall += 1
    
    if fall > 3 and int(state['acceleration_z'])<0:
        networkNow = 1