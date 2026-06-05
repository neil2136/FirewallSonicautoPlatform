import time
import re
from scapy.all import *
from runner.settings import logger
from tools.trafficGen import ScapyPacketSend


def get_pc_int_mac(pc_obj, iface):
    rc = pc_obj.send_command(f"ifconfig {iface}")
    res = re.search("(\S+:){5}\S+", rc)
    if res:
        iface_mac = res[0]
    else:
        iface_mac = ''
        logger.info(f"can't find the mac of {pc_obj}")
    return iface_mac.lower()


def fw_packet_monitor_run(packetobj, pcobj, kwargs, protocol):
    
    scapysend = ScapyPacketSend(iface='eth1', count=1)

    logger.info('start run FW packet monitor...')

    clearres = packetobj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')

    startres = packetobj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    if protocol == 'icmp':
        sendicmpres = scapysend.send_icmp_packet(**kwargs)
        logger.info('Send icmp packet result:{}'.format(sendicmpres))
    elif protocol == 'tcp':
        sendtcpres = scapysend.send_tcp_packet(**kwargs)
        logger.info('Send tcp packet result:{}'.format(sendtcpres))
    elif protocol == 'udp':
        sendudpres = scapysend.send_udp_packet(**kwargs)
        logger.info('Send udp packet result:{}'.format(sendudpres))
    elif protocol == 'icmpv6':
        for i in range(2, 20):
            icmpv6_dict = kwargs
            icmpv6_dict['IPv6']['src'] = "2001:2018:" + ":" + str(i)
            scapysend.send_icmpv6_echo_request_packet(**icmpv6_dict)
        logger.info('Send icmpv6 packet result')

    time.sleep(5)
    stopres = packetobj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')

    packetobj.export_captured_packets_pcapng()
    filterdnscmd = f'tshark -R "{protocol}" -r /tmp/packet-c.pcapng -V -T text'
    logger.info(f'filterdnscmd: {filterdnscmd}')

    filteredpackets = pcobj.send_command(filterdnscmd)
    logger.info('run packet monitor end...')

    return filteredpackets


def check_packet(exportres, filter_tuple, check_list):
    '''this function is verify the caputured packets contain all check_list with filter_tuple '''
    flag_list = []
    logger.info(f'check check_list: {check_list}')
    packets = exportres.split('Packet comments\n')
    logger.info(f'check filter tuple: {filter_tuple}')
    for check_point in check_list:
        logger.info(f'check_point is : {check_point}')
        for packet in packets:
            if check_point in packet:
                checkres = [x in packet for x in filter_tuple]
                logger.info(f'check packet result with {check_point}: {checkres}')
                if all(checkres):
                    logger.info(f'packet found:\n{packet}')
                    flag_list.append(True)
                    break

    logger.info(f"the final result list: {flag_list}")
    res = True if len(flag_list) == len(check_list) else False
    return res
