import socket
import sys
from check import ip_checksum

HOST = ''
PORT = 2401

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'
count = 0

while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    # get nextseqnum
    seq = data[0:1]
    # get ip_checksum
    msg_sum = data[1:3]
    # get message
    msg = data[3:len(data)]
    msg_checksum = ip_checksum(msg)

    if msg_sum != msg_checksum:
        count = count + 1
        # 404 Error if received error
        temp = int('404')
        reply = str(temp)
        s.sendto(reply, addr)
    else:
        reply = seq
        print 'Sent ACK' + reply
        s.sendto(reply, addr)
    if not data:
        break
    
s.close()