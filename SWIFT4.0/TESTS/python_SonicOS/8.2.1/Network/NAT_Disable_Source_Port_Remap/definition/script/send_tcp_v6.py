from scapy.all import *
import argparse

parser = argparse.ArgumentParser(description='send ipv6 tcp traffic on PC1')
parser.add_argument('-src_ip', type=str, dest='src_ip',
                    required=True, help='source ipv6 address')
parser.add_argument('-dst_ip', type=str, dest='dst_ip',
                    required=True, help='destination ipv6 address')
parser.add_argument('-src_port', type=int, dest='src_port',
                    required=True, help='source ipv6 port number')
parser.add_argument('-dst_port', type=int, dest='dst_port',
                    required=True, help='source ipv6 port number')

args = parser.parse_args()
src_ip = args.src_ip
dst_ip = args.dst_ip
src_port = args.src_port
dst_port = args.dst_port

# ipv6 = IPv6(src='2000::100', dst='2001::100')
ipv6 = IPv6(src=src_ip, dst=dst_ip)
tcp = TCP(sport=src_port, dport=dst_port)
package = ipv6/tcp
send(package, count=5)
