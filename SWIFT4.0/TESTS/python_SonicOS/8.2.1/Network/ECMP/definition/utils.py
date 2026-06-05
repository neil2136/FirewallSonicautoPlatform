from runner.settings import logger
import re

def check_packets(orgpacket, expectpkt, fwports):
    tag = []
    lenfwports = len(fwports)
    for fwport in fwports:
        logger.info('start search interface : {}'.format(fwport))
        expectpkt['out'] = fwport
        for packet in orgpacket.split('Packet number: '):
            if expectpkt['src'] in packet:
                if expectpkt['dst'] in packet:
                    if expectpkt['in'] in packet:
                        if expectpkt['out'] in packet:
                            if expectpkt['proto'] in packet:
                                logger.info(
                                    '{} packet is found :{}'.format(fwport, packet))
                                tag.append(1)
                                break
    return True if len(tag) == lenfwports else False


def check_1gw_TSR(tsr, ecmp_1gw_api_rt_dict, gw_list):
    tag = []
    res_1gw = re.search('dns_server (.*?)\n(.*?)\n(.*?)\n(.*?)\n', tsr)
    try:
        for gw in gw_list:
            if gw['value'] in res_1gw.group():
                tag.append(1)
    except:
        logger.error('can not get value key in {}'.format(gw_list))

    if len(tag) == len(gw_list):
        logger.info("{} is found".format(res_1gw.group()))
        return True
    else:
        logger.error("{} can't found".format(ecmp_1gw_api_rt_dict))
        return False


def check_4gw_TSR(tsr, ecmp_4gw_api_rt_dict, port_list):
    tag = []
    res_4gw = re.search('server_pc (.*?)\n(.*?)\n(.*?)\n(.*?)\n', tsr)
    try:
        for port in port_list:
            if port in res_4gw.group():
                tag.append(1)
    except:
        logger.error('can not get port in {}'.format(port_list))

    if len(tag) == len(port_list):
        logger.info("{} is found".format(res_4gw.group()))
        return True
    else:
        logger.error("{} can't found".format(ecmp_4gw_api_rt_dict))
        return False


"""
from scapy.all import *
from runner.settings import logger
from settings import *


def send_ICMP_packet(iface, src, dst):
    conf.iface = iface
    icmp_packet = IP(src=src, dst=dst)/ICMP()
    resp = srloop(icmp_packet, inter=1, count=1)
    logger.info(resp)
    return resp
"""