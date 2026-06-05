import os
import sys
import re
import time
import requests
from runner.settings import Params, logger


def dns_response_check(resp, src_ip, dst_ip):
    packets = resp.split('Packet number: ')
    lists = ['out:X2*, Forwarded', f'IP Type: UDP(0x11), Src=[{src_ip}], Dst=[{dst_ip}]', 'Src=[53]', 'DNS']
    for packet in packets:
        if all(x in packet for x in lists):
            return True, packet
    return False, ''


def pc_traffic_send(pc_obj, kwargs):
    if kwargs['type'] == 'ping':
        res = pc_obj.ping_from_eth(ip=kwargs['des'], eth=kwargs['eth'], num=10)
        return res
    if kwargs['type'] == 'cmd':
        res = pc_obj.send_command(kwargs['cmds'])
        return res
    if kwargs['type'] == 'http':
        res = requests.get(kwargs['url'])
        return True if res.status_code == 200 else False
    if kwargs['type'] == 'script':
        res = pc_obj.send_command(f'python3 {kwargs["path"]}protocolsend.py -t {kwargs["protocol"]} -u {kwargs["url"]}')
        return res
    if kwargs['type'] == 'nslookup':
        res = pc_obj.send_command(f'python3 {kwargs["path"]}nslookup.py -t {kwargs["protocol"]} -u {kwargs["url"]}')
        return res


def fw_packet_monitor_run(packet_obj, pc_obj, kwargs):
    packetres = ''
    logger.info('start run FW packet monitor...')
    clearres = packet_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packet_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    res = pc_traffic_send(pc_obj, kwargs)
    logger.info(f'pc traffic send result: {res}')

    stopres = packet_obj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')
    if 'packet' in kwargs.keys():
        if kwargs['packet'] == 'pcapng':
            packetres = packet_obj.export_captured_packets_pcapng()
    else:
        packetres = packet_obj.export_captured_packets()
    logger.info('run packet monitor end...')
    return res, packetres


def get_ip_lease_in_pc(pc_login, eth):
    res = False
    rang_ip_part = '192.168.20.13'
    cmds = [f'ifconfig {eth} 0.0.0.0', 'timeout 20 killall dhclient']
    pc_login.send_commands(cmds)
    for i in range(5):
        time.sleep(3)
        res = pc_login.send_command('timeout 20 dhclient -v {}'.format(eth))
        time.sleep(10)
        logger.info(f'run dhcp client on pc: {res}')
        if f'bound to {rang_ip_part}' in res:
            res = True
            break
        else:
            logger.info(f'pc {eth} failed to get ip address')
    return res


def release_ip_in_pc(pc_login, eth):
    cmds = ['killall dhclient', f'timeout 20 dhclient -r {eth}', f'timeout 5 ifconfig {eth} 0.0.0.0']
    pc_login.send_commands(cmds)
    time.sleep(3)
    logger.info('check if pc eth ip is released...')
    output = pc_login.send_command(f'ifconfig {eth}')
    if 'inet addr' not in output:
        logger.info(f"pc {eth} release successfully")
        return True
    else:
        logger.info(f"pc {eth} release failed")
        return False