from scapy.all import IP, TCP, send
from time import sleep
import sys

if __name__ == '__main__':
    if sys.argv[1] == 'stress':
        pkt = IP(dst='12.12.1.169') / TCP(dport=12345)
        send(pkt, inter=0.001, count=10000)
        exit(0)

    if sys.argv[1] == 'count':
        for i in range(20):
            ip = f'12.12.1.{i + 10}'
            print(ip)
            pkt = IP(dst=ip) / TCP(dport=10000 + i)
            send(pkt, count=3)
            sleep(3)
        exit(0)
