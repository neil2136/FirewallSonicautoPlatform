from scapy.all import conf, IP, TCP, srloop, UDP
import argparse


def send_tcp_packet(iface, dst_ip):
    conf.iface = iface
    tcp_packet = IP(dst=dst_ip)/TCP(dport=3389, flags="S")
    resp = srloop(tcp_packet, count=3)
    return resp

def send_udp_packet(iface, dst_ip):
    conf.iface = iface
    udp_packet = IP(dst=dst_ip)/UDP(dport=3389)
    resp = srloop(udp_packet, count=3)
    return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='start send packet')
    parser.add_argument('-dst', type=str, dest='dst', required=True, help='ip where send packet to')
    parser.add_argument('-protocol', type=str, dest='protocol', required=True, help='protocol')
    args = parser.parse_args()
    dst = args.dst
    prot = args.protocol
    if prot == 'TCP':
       send_tcp_packet('eth1', dst)
    elif prot == 'UDP':
        send_udp_packet('eth1', dst)
    else:
        print("you should specify the protocol")
