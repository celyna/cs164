import socket
import sys
from check import ip_checksum

# Datagram (udp) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = '';
port = 2401;

# set up window size, base, and sequence values
windowSize = 4
base = 1
nextseqnum = 1

# set up the packet list, size 10
pktList = []
n = 1
pktList.append(0)
while(n < 11) :
    pktList.append(n)
    n = n + 1

old_msg = ''
count = 0 
while 1:
    if base == 10 :
        break
    # get the next piece of data in the pktList
    elif nextseqnum < base + windowSize :
        msg = str(pktList[nextseqnum])
    try :
        # timeout
        s.settimeout(3)
        if msg == '2':
            if count == 0:
                # break the checksum intentionally
                d = ip_checksum(msg + '1')
                msg_d = d + msg
                msg_seq_d = str(nextseqnum) + msg_d
                count = count + 1
            else:
                d = ip_checksum(msg)
                msg_d = d + msg
                msg_seq_d = str(nextseqnum) + msg_d
        else :
            d = ip_checksum(msg)
            msg_d = d + msg
            msg_seq_d = str(nextseqnum) + msg_d # number + chksm + msg
       
        if nextseqnum < base + windowSize :
            print 'Sending... PKT' + msg_seq_d[3:]
            s.sendto(msg_seq_d, (host, port))
            nextseqnum = nextseqnum + 1
        
        # receive data back from server for ACK
        try:
            data = s.recvfrom(1024)
            reply = data[0]
            addr = data[1]
        except :
            print 'Timeout.'
            nextseqnum = base
            continue

        # update base if received correctly
        if reply == str(base) :
            base = base + 1

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()