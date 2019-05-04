from ruuvitag_sensor.ruuvitag import RuuviTag
import time

import socket

#send
UDPIPS = ['192.168.1.200','192.168.1.201','192.168.1.202']
UDP_IP = "192.168.1.?" ##service IP
UDP_PORT = 9011
MESSAGE = "Fall"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind(('0.0.0.0', UDP_PORT))


sensor = RuuviTag('CF:FC:1D:65:2E:98')
while True:
    state = sensor.update()

    state = sensor.state

    if int(state['acceleration_z'])<500:
        print(state['acceleration_x'],state['acceleration_y'],state['acceleration_z'])
        sock.sendto(bytes(MESSAGE.encode('utf8')), (UDPIPS[0], UDP_PORT))
