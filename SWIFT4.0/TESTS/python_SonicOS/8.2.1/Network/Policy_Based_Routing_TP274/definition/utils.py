import os
import sys
import re
import requests
from runner.settings import Params, logger


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


def fw_packet_monitor_run(packet_obj, pc_obj, kwargs):
    logger.info('start run FW packet monitor...')
    clearres = packet_obj.clear_packets()
    logger.info(f'clear packets on FW result: {clearres}')
    startres = packet_obj.start_capture()
    logger.info(f'start packets on FW result: {startres}')

    res = pc_traffic_send(pc_obj, kwargs)
    logger.info(f'pc traffic send result: {res}')

    stopres = packet_obj.stop_capture()
    logger.info(f'start packets on FW result: {stopres}')
    packetres = packet_obj.export_captured_packets()
    logger.info('run packet monitor end...')
    return res, packetres


def icmp_request_check(resp, src_ip, dst_ip, status='Forwarded'):
    packets = resp.split('Packet number: ')
    packetin = 'in:X0'
    packetout = 'out:X2'
    icmptype = 'ICMP Type = 8'
    srcip = f"Src=[{src_ip}]"
    dstip = f"Dst=[{dst_ip}]"
    for packet in packets:
        if packetin in packet and packetout in packet:
            if icmptype in packet:
                if srcip in packet and dstip in packet:
                    if status in packet:
                        return True, packet
    return False, ''


def http_request_check(resp, packet_out='X2', src_ip='', status='Forwarded'):
    packets = resp.split('Packet number: ')
    # check request via x0 to x2/x3
    packetout = f'out:{packet_out}'
    flag = 'SYN'
    srcip = f"Src=[{src_ip}]"
    dstport = f"Dst=[443]"
    for packet in packets:
        if packetout in packet and flag in packet:
            if srcip in packet and dstport in packet:
                if status in packet:
                    return True, packet
    return False, ''


def http_reponse_check(resp, packet_in='X2', dst_ip='', status='Forwarded'):
    packets = resp.split('Packet number: ')
    # check response via x2/x3 to x0
    packetin = f'in:{packet_in}'
    packetout = 'out:X0'
    flag = 'ACK'
    dstip = f"Dst=[{dst_ip}]"
    srcport = f"Src=[443]"
    for packet in packets:
        if packetin in packet and packetout in packet:
            if flag in packet:
                if dstip in packet and srcport in packet:
                    if status in packet:
                        return True, packet
    return False, ''


def ftp_request_check(resp, packet_in='X0', src_ip='', status='Forwarded'):
    packets = resp.split('Packet number: ')
    # check request via x0 to x2
    packetin = f'in:{packet_in}'
    packetout = 'out:X2'
    flag = 'SYN'
    srcip = f"Src=[{src_ip}]"
    dstport = f"Dst=[21]"
    for packet in packets:
        if packetin in packet and packetout in packet:
            if flag in packet:
                if srcip in packet and dstport in packet:
                    if status in packet:
                        return True, packet
    return False, ''



# must add to common lib file object, because edit_addressgroup can not support add name to api url
def edit_addressgroup_by_name(self, version='v4', name='', msg=False, **kwargs):
    json_input = copy.deepcopy(kwargs)
    logger.info(json_input)
    if version == 'v4':
        url_edit = self.url_v4
    else:
        url_edit = self.url_v6
    if name is '':
        logger.error('key parameter: name do not empty.')
        return (False, {}) if msg else False
    resp = self.fw.api_put(url_edit+'name/'+name, msg, data=json_input)
    return resp


# must add to common lib file network, because the config_failover_groups can not support set the multi interfaces
def config_failover_groups_by_multi(self, msg=False, **kwargs):
    try:
        base_dict = kwargs['failover_lb']['group'][0]
        if 'name' in base_dict.keys():
            name = base_dict['name'].replace(' ', '%20')
        else:
            logger.error('the key: name must be exist in kwargs.')
            return (False, {}) if msg else False
        url = self.groups_url + '/name/{}'.format(name)
        res = self.fw.api_put(url, msg, data=kwargs)
        return res
    except Exception as e:
        logger.error(repr(e))
        logger.error('the kwargs was not a valid wan lb json')
        return (False, {}) if msg else False



