from socket import socket, AF_INET, SOCK_DGRAM, timeout
from struct import unpack
from time import ctime, sleep
from sys import argv

argv = argv[1:]
if len(argv) == 0:
    argv = ['3.3.3.22']

s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(5.0)

for server in argv:
    print(server, ":", end=" ")
    try:
        s.sendto(b'', (server, 37))
        t = unpack('!I', s.recv(16)[:4])[0]
        # Convert from 1900/01/01 epoch to 1970/01/01 epoch
        t -= 2208988800
        print(ctime(t))
    except timeout:
        print("TIMEOUT")
    except Exception as e:
        print("ERROR:", e)

s.close()
sleep(2)

argv = argv[1:]
if len(argv) == 0:
    argv = ['3.3.3.22']

s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(5.0)

for server in argv:
    print(server, ":", end=" ")
    try:
        s.sendto(b'', (server, 37))
        t = unpack('!I', s.recv(16)[:4])[0]
        # Convert from 1900/01/01 epoch to 1970/01/01 epoch
        t -= 2208988800
        print(ctime(t))
    except timeout:
        print("TIMEOUT")
    except Exception as e:
        print("ERROR:", e)

s.close()
sleep(2)
