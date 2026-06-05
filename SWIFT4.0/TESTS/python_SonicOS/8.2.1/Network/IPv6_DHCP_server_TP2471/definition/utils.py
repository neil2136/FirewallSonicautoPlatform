#!/usr/bin/python
# import os
# import sys
import re
import time
# from runner.settings import logger
from definition.settings import logger


def get_dhcpv6_leases(pc_login, eth):
    initial_pc_eth_for_get_dhcpv6_lease(pc_login, eth)
    try:
        cmds = [
            f'timeout 20 dhclient -6  {eth} -v',
            f'ifconfig {eth}'
        ]
        leaseoutput = pc_login.send_commands(cmds)
        lease_ipv6 = re.search('(?<=inet6 )\d+\:\d+\::[A-Za-z0-9]+', leaseoutput, re.I).group()
        return lease_ipv6
    except Exception as e:
        logger.error(repr(e))
        return ''


def get_dhcpv6_leases_on_remote_dut(re_interfacecli, interface, version):
    ipv6_addr = ''
    ipoutput = re_interfacecli.show_interface_ips(interface, version)
    lease_ipv6 = re.search(r'(?<=IP Address:)(\s+)\d+\:\d+\::[A-Za-z0-9]+', ipoutput, re.I)
    if lease_ipv6:
        ipv6_addr = lease_ipv6.group()
        return ipv6_addr.lstrip()
    else:
        return ipv6_addr


def release_dhcpv6_lease(pc_login, eth):
    cmds = [
        f'timeout 20 dhclient -6 {eth} -r',
        f'ifconfig {eth}'
    ]
    output1 = pc_login.send_commands(cmds)
    try:
        release_ipv6 = re.search('(?<=inet6 )\d+\:\d+\::\d+', output1, re.I)
        if not release_ipv6:
            return True
        else:
            return False
    except Exception as e:
        logger.error(repr(e))
        return False


def initial_pc_eth_for_get_dhcpv6_lease(pc_login, eth):
    output1 = pc_login.send_command(f'ifconfig {eth}')
    try:
        lease_ipv6 = re.search('(?<=inet6 )\d+\:\d+\::[A-Za-z0-9]+', output1, re.I)
        if not lease_ipv6:
            logger.info(f'del dhclient process before get dhcpv6 address')
            cmds1 = [
                'rm -rf /var/lib/dhclient/dhclient6.leases',
                'timeout 20 killall dhclient'
            ]
            output2 = pc_login.send_commands(cmds1)
            logger.info(f'output2 is {output2}')
        else:
            logger.info(f'{eth} has global ipv6 address,need delete or release it first,begin to do ')
            cmds2 = [
                f'timeout 20 dhclient {eth} -6 -r',
                'rm -rf /var/lib/dhclient/dhclient6.leases',
                f'ifconfig eth1 del {lease_ipv6.group()}/128',
                'timeout 20 killall dhclient',
                'ifconfig eth1'
            ]
            output3 = pc_login.send_commands(cmds2)
            logger.info(f'output3 is {output3}')
    except Exception as e:
        logger.error(repr(e))


def start_capture_and_clear_packets(packet_monitorapi):
    stratres = packet_monitorapi.start_capture()
    logger.info(f'start packet monitor result: {stratres}')
    clearres = packet_monitorapi.clear_packets()
    logger.info(f'clear packet monitor result: {clearres}')


def check_dhcpv6_packets(packet_monitorapi, pc_login, mestype_inlist, mestype_outlist='', mes=False):
    time.sleep(10)
    incheckres = []
    outcheckres = []
    mestypeinlist = []
    mestypeoutlist = []
    time.sleep(10)
    stopres = packet_monitorapi.stop_capture()
    logger.info(f'start packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    logger.info(exportres)
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = pc_login.send_command(cmd)
    logger.info(f'fitter dhcpv6 packet result: {pccmdres}')
    for inmestype in mestype_inlist:
        if inmestype in pccmdres:
            incheckres.append(True)
            logger.info(f'{inmestype} is in the packets')
            mestypeinlist.append(inmestype)
        else:
            logger.info(f'{inmestype} is not in the packets')
            incheckres.append(False)
            mestypeoutlist.append(inmestype)
    if mestype_outlist:
        for outmestype in mestype_outlist:
            if outmestype not in pccmdres:
                outcheckres.append(True)
                logger.info(f'{outmestype} is not in the packets')
                mestypeinlist.append(outmestype)
            else:
                logger.info(f'{outmestype} is in the packets')
                outcheckres.append(False)
                mestypeoutlist.append(outmestype)
        return all(incheckres), all(outcheckres)
    else:
       return all(incheckres)
    if mes:
        if mestype_outlist:
            return all(incheckres), all(outmestype), mestypeinlist, mestypeoutlist
        else:
            return all(incheckres), mestypeinlist


def get_t1_time_in_dhcpv6_packets(packet_monitorapi, pc_login):
    t1_time = ''
    time.sleep(10)
    stopres = packet_monitorapi.stop_capture()
    logger.info(f'start packet monitor result: {stopres}')
    exportres = packet_monitorapi.export_captured_packets_pcapng()
    logger.info(f'exportres is {exportres}')
    cmd = 'tshark -R "udp" -2 -r /tmp/packet-c.pcapng -V -T text'
    pccmdres = pc_login.send_command(cmd)
    logger.info(f'fitter dhcpv6 packet result: {pccmdres}')
    if pccmdres:
        dhcpv6typelist = pccmdres.split("Packet comments")
        for dhcpv6type in dhcpv6typelist:
            logger.info(dhcpv6type)
            if "Message type: Advertise (2)" in dhcpv6type:
                t1_time = re.search('(?<=T1: )\d+', dhcpv6type, re.I | re.S).group()
                return t1_time
    else:
        logger.error('no packets are captured')
        return t1_time


def send_information_request(pc_login, eth):
    cmds = [
        'rm -rf /var/lib/dhclient/dhclient6.leases',
        'timeout 20 killall dhclient',
        f'timeout 20 dhclient -6 {eth} -v -S'
    ]
    output = pc_login.send_commands(cmds)
    return output


# need add into cli_network_interface
# def show_interface_ips(self, interface=None, version='ipv4'):
#     commands = ['show interface ' + version + ' ' + interface + ' ips']
#     output = self.fw.do_cli_commands(commands, tag=1)[1]
#     return output