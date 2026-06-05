#!/usr/bin/python
import re
import time
from runner.settings import logger


def get_dhcp_lease(pc_login, eth, dhcp_options=''):
    initial_pc_eth_for_get_dhcp_lease(pc_login, eth)
    try:
        if dhcp_options:
            cmds = [
                f'timeout 20 dhclient {eth} -v -R {dhcp_options}',
                f'ifconfig {eth}'
            ]
        else:
            cmds = [
                f'timeout 20 dhclient {eth} -v',
                f'ifconfig {eth}'
            ]
        output = pc_login.send_commands(cmds)
        lease = re.search(r'(?<=inet )\d+\.\d+\.\d+.\d+', output, re.I).group()
        return lease
    except Exception as e:
        logger.error(repr(e))
        return ''


def check_dhcp_packets(packet_monitorapi, pc_login, option_list):  # mode =Discover/request/offer/ack
    typelist = ['DHCP: Discover', 'DHCP: Request', 'DHCP: Offer', 'DHCP: ACK']
    checkres = []
    stopres = packet_monitorapi.stop_capture()
    logger.info(f'start packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    logger.info(exportres)
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = pc_login.send_command(cmd)
    logger.info(f'fitter dhcp packet result: {pccmdres}')
    if pccmdres:
        dhcplist = pccmdres.split("Packet comments")
        for dhcptype in dhcplist:
            logger.info(dhcptype)
            for type in typelist:
                if type in dhcptype:
                    if option_list in dhcptype:
                        checkres.append(type)
                        logger.info(f'{option_list} is in {type} packet')
                    else:
                        logger.info(f'{option_list} is not in {type} packet')
    return checkres


def get_packets_txt(packet_monitorapi, pc_login):
    stopres = packet_monitorapi.stop_capture()
    logger.info(f'start packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    logger.info(exportres)
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = pc_login.send_command(cmd)
    logger.info(f'fitter dhcp packet result: {pccmdres}')
    if pccmdres:
        dhcplist = pccmdres.split("Packet comments")
        return dhcplist
    else:
        return ''


def check_dhcp_packets(packets_list, mode, check_list):
    checkres = []
    for packets in packets_list:
        if f'DHCP: {mode}' in packets:
            for check in check_list:
                if check in packets:
                    checkres.append(True)
                else:
                    checkres.append(False)
            return all(checkres)
    else:
        return False


def release_dhcp_lease(pc_login, eth):
    cmds = [
        f'timeout 20 dhclient {eth} -r',
        f'ifconfig {eth}'
    ]
    output1 = pc_login.send_commands(cmds)
    try:
        release_ip = re.search(r'(?<=inet )\d+\.\d+\.\d+.\d+', output1, re.I)
        if not release_ip:
            return True
        else:
            return False
    except Exception as e:
        logger.error(repr(e))
        return False


def initial_pc_eth_for_get_dhcp_lease(pc_login, eth):
    output1 = pc_login.send_command(f'ifconfig {eth}')
    try:
        lease = re.search(r'(?<=inet )\d+\.\d+\.\d+.\d+', output1, re.I)
        if not lease:
            logger.info(f'del dhclient process before get ip address')
            cmds1 = [
                f'rm -rf /var/lib/dhclient/dhclient--{eth}.lease',
                f'rm -rf /var/lib/dhclient/dhclient.lease',
                'timeout 20 killall dhclient'
            ]
            output2 = pc_login.send_commands(cmds1)
            logger.info(f'output2 is {output2}')
        else:
            logger.info(f'{eth} has ip address,release it first,begin to do ')
            cmds2 = [
                f'timeout 20 dhclient {eth} -4 -r',
                f'rm -rf /var/lib/dhclient/dhclient--{eth}.lease',
                'timeout 20 killall dhclient',
                f'ifconfig {eth}'
            ]
            output3 = pc_login.send_commands(cmds2)
            logger.info(f'output3 is {output3}')
    except Exception as e:
        logger.error(repr(e))


def start_capture_and_clear_packets(packet_monitorapi):
    logger.info('start to start and clear capture')
    stratres = packet_monitorapi.start_capture()
    logger.info(f'start packet monitor result: {stratres}')
    clearres = packet_monitorapi.clear_packets()
    logger.info(f'clear packet monitor result: {clearres}')
