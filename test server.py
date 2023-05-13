import socket
import json
import numpy as np
import matplotlib.pyplot as plt

HOST = "192.168.50.112" # IP address
PORT = 2049 # Port to listen on (use ports > 1023)

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mapping_of_title = dict()
mapping_of_title[(0,0)] = 'right'
mapping_of_title[(0,1)] = 'left'
mapping_of_title[(1,0)] = 'jump'
mapping_of_title[(1,1)] = 'shot'
    
s.bind((HOST, PORT))
###print('Listening for broadcast at ', s.getsockname())
fig, axs = plt.subplots(3, 2)
plt.tight_layout()

for index in range(0,2):
        for j in range(0,2):
            axs[index,j].set_title(mapping_of_title[(index,j)])
t=0

while True:
    data,addr = s.recvfrom(1024)
    print('Server received from {}:{}'.format(addr, data.decode('utf-8')))
    obj = json.loads(data)
    t = t+1
    axs[0,0].scatter(t, obj['right'], color='tab:blue', s=25)
    axs[0,1].scatter(t, obj['left'], color='tab:orange', s=25)
    axs[1,0].scatter(t, obj['jump'], color='tab:green', s=25)
    axs[1,1].scatter(t, obj['shot'], color='tab:green', s=25)
    
    plt.pause(0.001)