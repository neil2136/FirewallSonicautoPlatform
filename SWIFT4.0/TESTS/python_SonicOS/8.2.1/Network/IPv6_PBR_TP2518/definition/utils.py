#!/usr/bin/python
import os
import sys
import getopt
import re
from definition.settings import Parameter, fw_api
from runner.settings import Params, logger
import time


def get_pbr_hit_time_in_tsr(tsr_routing, pbr_name):
    hittime = ''
    route_sp = tsr_routing.split('\n\n\n')
    for route in route_sp:
        if f'name: {pbr_name}' in route:
            logger.info(f'get ipv6 pbr from tsr is {route}')
            hittime = re.search('(?<=Time Last Hit:   )\d+/\d+/\d+\s+\d+:\d+:\d+.\d+', route, re.I | re.S).group()
            return hittime
    return hittime


def pc_traffic_send(pc_obj, **kwargs):
    if kwargs['type'] == 'ping':
        res = pc_obj.send_command(f"ping -I {kwargs['eth']} -c 5 {kwargs['des']}")
        return res
    if kwargs['type'] == 'ping6':
        res = pc_obj.send_command(f"ping6 -I {kwargs['eth']} -c 5 {kwargs['des']}")
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


def fw_packet_monitor_run(packet_obj, pc_obj, **kwargs):
    logger.info('start run FW packet monitor...')
    clearres = packet_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packet_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    res = pc_traffic_send(pc_obj, **kwargs)
    logger.info(f'pc traffic send result: {res}')

    stopres = packet_obj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')
    packetres = packet_obj.export_captured_packets()
    logger.info('run packet monitor end...')
    return res, packetres


def icmp_traffic_check(resp, **kwargs):
    request = False
    packets = resp.split('Packet number: ')
    packetin = f"in:{kwargs['iface_in']}"
    packetout = f"out:{kwargs['iface_out']}"
    icmptype = 'ICMP Type = 128'
    srcip = f"Src=[{kwargs['src_ip']}]"
    dstip = f"Dst=[{kwargs['dst_ip']}"
    status = 'Forwarded'
    tuples = (packetin, packetout, icmptype, srcip, dstip, status)
    for packet in packets:
        if all(x in packet for x in tuples):
            request = True
    logger.info(f'resuest is {request}')
    logger.info(f'request is {request}')
    if request:
        repacketin = f"in:{kwargs['iface_out']}"
        repacketout = f"out:{kwargs['iface_in']}"
        reicmptype = 'ICMP Type = 129'
        resrcip = f"Src=[{kwargs['dst_ip']}]"
        redstip = f"Dst=[{kwargs['src_ip']}]"
        retuples = (repacketin, repacketout, reicmptype, resrcip, redstip, status)
        for packet in packets:
            if all(x in packet for x in retuples):
                return True, packet
    else:
        return False, ''
