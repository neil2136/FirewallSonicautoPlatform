from scapy.all import conf, IPv6, ICMPv6EchoRequest, srloop
import argparse


def send_icmpv6_packet(tc):
    conf.iface = 'eth0'
    ip = IPv6()
    ip.dst = "2001:8888::1000"
    ip.src = "2001:2013::101"
    ip.tc = tc
    ip.show()
    print('-----------------------------------------\n')
    request = ICMPv6EchoRequest()
    request.id=98
    request.show()
    print('-----------------------------------------\n')

    resp = srloop(ip/request,count =5)
    return resp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='start send icmpv6 packet')
    parser.add_argument('-tc', type=int, dest='tc', required=True, help='traffic class')
    args = parser.parse_args()
    tc = args.tc
    send_icmpv6_packet(tc)