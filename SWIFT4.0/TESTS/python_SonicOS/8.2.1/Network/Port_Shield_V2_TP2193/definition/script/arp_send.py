from scapy.all import *
import argparse


parser = argparse.ArgumentParser(description='send arp from PC2')
parser.add_argument('-srcmac', type=str, dest='srcmac',
                    required=True, help='source mac')
parser.add_argument('-iface', type=str, dest='iface',
                    required=True, help='interface send traffic')
parser.add_argument('-pdst', type=str, dest='pdst',
                    required=True, help='dest ip')
parser.add_argument('-psrc', type=str, dest='psrc',
                    required=True, help='src ip')
args = parser.parse_args()
srcmac = args.srcmac
iface = args.iface
psrc = args.psrc
pdst = args.pdst
p = Ether(dst="ff:ff:ff:ff:ff:ff", src=srcmac) / \
    ARP(psrc=psrc, hwsrc=srcmac, pdst=pdst, )
for i in range(20):
    output = srp(p, iface=iface, timeout=2)
    print(output)
