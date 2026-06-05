from scapy.all import *
from scapy.layers.inet6 import IPv6
from scapy.layers.inet import TCP
import sys

if len(sys.argv) < 3:
        print('ERROR: Please check the parameters!')
        sys.exit()

type = sys.argv[1]
ipv6_dst = sys.argv[2]
src_port = 12345
dst_port = 80
def send_tcp(type, ipv6_dst):
    if type == 'SA':
        packet = IPv6(dst=ipv6_dst)/TCP(sport=src_port, dport=dst_port, flags="SA")
        send(packet)
    else:
        ip6_packet = IPv6(dst=ipv6_dst)/TCP(dport=(1,1024), flags="S")
        fragments = fragment6(ip6_packet,8)
        for frag in fragments:
            send(frag, verbose=True)

if __name__ == '__main__':
    send_tcp(type, ipv6_dst) 
