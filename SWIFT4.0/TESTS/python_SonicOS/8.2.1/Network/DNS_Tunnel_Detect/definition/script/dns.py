from scapy.all import *
import sys

ip = IP(src='192.168.168.169', dst='12.12.1.169')
udp = UDP(sport=5000, dport=53)
dns = DNS(id=1, qd=DNSQR(qname='www.google.com'))
pkt = ip / udp / dns

if __name__ == '__main__':
    if sys.argv[1] == 'dns_1000':
        send(pkt, inter=0.001, count=2000, iface='eth1')
        exit()

    if sys.argv[1] == 'dns_100':
        send(pkt, inter=0.01, count=100, iface='eth1')
        exit()

    if sys.argv[1] == 'dns_10':
        dns_A = DNS(id=1, qd=DNSQR(qname='www.google.com'))
        dns_TXT = DNS(id=1, qd=DNSQR(qname='www.baidu.com', qtype=16))
        pkt_A = ip / udp / dns_A
        pkt_TXT = ip / udp / dns_TXT
        send(pkt_A, inter=0.01, count=900, iface='eth1')
        send(pkt_TXT, inter=0.01, count=200, iface='eth1')
        exit()

    if sys.argv[1] == 'dns_query':
        send(pkt, inter=1, count=10, iface='eth1')

