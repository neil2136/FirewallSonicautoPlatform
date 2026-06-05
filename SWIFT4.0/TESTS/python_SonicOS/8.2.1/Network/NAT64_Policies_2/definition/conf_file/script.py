import sys
import subprocess
import pexpect
from scapy.all import *


def send_icmpv6_fragment_pkt_from_wan():
    ipv6 = IPv6(dst='64:9999::c0c:1a9')
    icmpv6 = ICMPv6EchoRequest()
    payload = 'a' * 2450
    pkt_6 = ipv6 / icmpv6 / payload
    f_pkt = fragment6(pkt=pkt_6, fragSize=1300)
    for i in range(3):
        for p in f_pkt:
            send(p, inter=1)


def send_ipv6_udp():
    ipv6 = IPv6(dst='64:ff9b::c0c:1a9')
    udp = UDP(sport=5555, dport=12345)
    pkt_6 = ipv6 / udp
    send(pkt_6, inter=1, count=5)


def send_ipv6_tcp():
    ipv6 = IPv6(dst='64:ff9b::c0c:1a9')
    tcp = TCP(sport=4444, dport=10101)
    pkt_6 = ipv6 / tcp
    send(pkt_6, inter=1, count=5)


def send_icmpv6_fragment_packet():
    ipv6 = IPv6(dst='64:ff9b::c0c:1a9')
    icmpv6 = ICMPv6EchoRequest()
    payload = 'a' * 2450
    pkt_6 = ipv6 / icmpv6 / payload
    f_pkt = fragment6(pkt=pkt_6, fragSize=1300)
    for i in range(3):
        for p in f_pkt:
            send(p, inter=1)


def send_ipv6_udp_fragment_packet():
    ipv6 = IPv6(dst='64:ff9b::c0c:1a9')
    udp = UDP(sport=3333, dport=22222)
    payload = 'a' * 2450
    pkt_6 = ipv6 / udp / payload
    f_pkt = fragment6(pkt=pkt_6, fragSize=1300)
    for i in range(3):
        for p in f_pkt:
            send(p, inter=1)


def send_ipv6_tcp_fragment_packet():
    ipv6 = IPv6(dst='64:ff9b::c0c:1a9')
    tcp = TCP(sport=4444, dport=10101)
    payload = 'a' * 2450
    pkt_6 = ipv6 / tcp / payload
    f_pkt = fragment6(pkt=pkt_6, fragSize=1300)
    for i in range(3):
        for p in f_pkt:
            send(p, inter=1)


if __name__ == '__main__':
    if sys.argv[1] not in ('udp', 'tcp', 'icmpv6_f', 'udp_f', 'tcp_f', 'icmpv6_from_wan'):
        print('pls specify correct argv in tcp or udp')
        exit(1)
    if sys.argv[1].lower() == 'udp':
        send_ipv6_udp()
        exit()
    if sys.argv[1].lower() == 'tcp':
        send_ipv6_tcp()
        exit()
    if sys.argv[1].lower() == 'icmpv6_f':
        send_icmpv6_fragment_packet()
        exit()
    if sys.argv[1].lower() == 'udp_f':
        send_ipv6_udp_fragment_packet()
        exit()
    if sys.argv[1].lower() == 'tcp_f':
        send_ipv6_tcp_fragment_packet()
        exit()
    if sys.argv[1].lower() == 'icmpv6_from_wan':
        send_icmpv6_fragment_pkt_from_wan()
        exec()
