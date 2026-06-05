import re
from scapy.all import *


def send_icmp_data_packet(icmpconf):
    conf.iface = icmpconf['iface']
    # packet = IP(dst='12.12.1.201', ttl=64)/ICMP()/(b'rootkit'*100)
    packet = IP(dst=icmpconf['dst'], ttl=64) / \
        ICMP() / (b'8' * icmpconf['lenth'])
    resp = srloop(packet, count=1)
    return resp


def send_udp_data_packet(udpconf):
    conf.iface = udpconf['iface']
    # packet = IP(dst='12.12.1.201', ttl=64)/ICMP()/(b'rootkit'*100)
    packet = IP(dst=udpconf['dst'], ttl=64, flags=2) / \
        UDP(dport=6666) / (b'9' * udpconf['lenth'])
    resp = srloop(packet, count=1)
    return resp


def udp_forworded_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    result_packet = []
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    packettype = f"Forwarded"
    for packet in packets:
        if srcip in packet:
            if dstip in packet:
                if packettype in packet:
                    result_packet.append(packet)
    forwarded = True if result_packet else False
    # fragmented = True if len(result_packet) > 1 else False
    # return forwarded, fragmented
    return forwarded


def vpn_name_check(vpnentry, vpnname):
    if vpnentry:
        try:
            if vpnentry['vpn']['policy'][0]['ipv4']['site_to_site']['name'] == vpnname:
                return True
        except BaseException:
            return False
    else:
        return False
