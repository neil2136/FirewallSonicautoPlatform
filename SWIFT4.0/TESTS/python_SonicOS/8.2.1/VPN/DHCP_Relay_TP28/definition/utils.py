#!/usr/bin/python
import os
import sys
import getopt
import re
from definition.settings import Parameter, fw_api, r_fw_api
from runner.settings import Params, logger
import time


def renew_dhcp_lease(RMT_HOST, interface):
    processres = RMT_HOST.send_command("ps -ef | grep 'dhclient -v eth1' | awk ' {print $2 '\\t' $8}'")
    if 'dhclient' in processres:
        processres = RMT_HOST.send_command("ps -ef | grep 'dhclient -v eth1' | awk ' {print $2 '\\t' $8}'")
        dhclientid = re.findall('\d+(?=dhclient)', processres, re.I)[0]
        RMT_HOST.send_command(f'kill -9 {dhclientid}')
        out = RMT_HOST.send_command(f'dhclient -v {interface}')
        logger.info(out)
        try:
            dhcplease = re.search('(?<=bound to )\d+\.\d+\.\d+\.\d+', out, re.I | re.S).group()
            return dhcplease
        except Exception as e:
            logger.error(repr(e))
            return ''
    else:
        return ''


def get_dhcp_lease(RMT_HOST, interface):
    out = RMT_HOST.send_command(f'dhclient -v {interface}')
    logger.info(out)
    try:
        dhcplease = re.search('(?<=bound to )\d+\.\d+\.\d+\.\d+', out, re.I | re.S).group()
        return dhcplease
    except Exception as e:
        logger.error(repr(e))
        return ''


def release_dhcp_lease(RMT_HOST, interface, lox0net, rex0ip):
    ethinfo = RMT_HOST.send_command(f'ifconfig {interface}')
    routprint = RMT_HOST.send_command('ip -4 r')
    if 'inet addr:' in ethinfo:
        if f'{lox0net}/24 via {rex0ip} dev {interface}' not in routprint:
            logger.info(
                'need add static route otherwise dynanic lease entry cannot disappear on remote and centrral FWs')
            res = add_route_on_pc(RMT_HOST, lox0net, rex0ip, 'central')
            logger.info(f'add route is : {res}')
        RMT_HOST.send_command(f'dhclient -r {interface}')
        ethinfo1 = RMT_HOST.send_command(f'ifconfig {interface}')
        if 'inet addr:' not in ethinfo1:
            return True
        else:
            return False
    else:
        # released before process
        res = RMT_HOST.send_command(f'dhclient -r {interface}')
        logger.info(res)
        return False


def log_event_filter(log, base_time, event_id):
    # event_id = 225: getlease
    # event_id = 224: release
    leasemessage = 'DHCP lease relayed to remote device'
    releasemessage = 'DHCP RELEASE received from remote device'
    time_array = time.strptime(log['time'], '%m/%d/%Y %H:%M:%S')
    logger.info(f'time_array is : {time_array} \n base time is : {base_time}')
    if time_array >= base_time:
        logger.info('fw log id time is : {}'.format(log['time']))
        logger.info(f'event_id is :{event_id}')
        if event_id == 225:
            # {'time': '11/14/2022 22:59:25', 'id': 225, 'category': 'VPN', 'priority': 'Information', 'src_int_': 'X0',
            #  'dst_int_': None, 'src_ip': '192.168.168.169', 'src_port': 67, 'dst_ip': '172.16.1.10', 'dst_port': 67,
            #  'ip_protocol': 'udp', 'user_name': 'admin', 'application': None, 'notes': None,
            #  'message': 'DHCP lease relayed to remote device'}
            if log['message'] == leasemessage and log['src_ip'] == Parameter.LAN_PC and \
                    log['dst_ip'] == Parameter.RELAY_IP:
                logger.info(f'check DHCP lease relayed to remote device result:\n {log}')
                return True
        elif event_id == 224:
            # {'time': '11/17/2022 00:17:45', 'id': 224, 'category': 'VPN', 'priority': 'Information', 'src_int_': 'X1',
            #   'dst_int_': None, 'src_ip': '172.16.1.10', 'src_port': 68, 'dst_ip': '192.168.168.169', 'dst_port': 67,
            #   'ip_protocol': 'udp', 'user_name': None, 'application': None, 'notes': None,
            #   'message': 'DHCP RELEASE received from remote device'},
            if log['message'] == releasemessage and log['src_ip'] == Parameter.RELAY_IP and \
                    log['dst_ip'] == Parameter.LAN_PC:
                logger.info(f'check DHCP lease relayed to remote device result:\n {log}')
                return True
    return False


def check_log_by_time(fw_time, fw_logs, event_id):
    if type(fw_time) is dict:
        part_time = fw_time['time']['date'].replace(':', '/') + ' ' + fw_time['time']['time']
        base_time = time.strptime(part_time, '%Y/%m/%d %H:%M:%S')
        logger.info(f'fw_time is : {fw_time}')
        logger.info(f'fw system base_time is : {part_time}')
        if type(fw_logs) is list:
            for log in fw_logs:
                if log_event_filter(log, base_time, event_id):
                    logger.info('march log event via filter successful !')
                    return True
        elif type(fw_logs) is dict:
            return log_event_filter(fw_logs, base_time, event_id)

        else:
            logger.info('fw_logs is not list or dict.')
    else:
        logger.info('fw_time is not dict.')
    return False


def add_route_on_pc(rmt_host, net, gw, to_dut):  # to_dut:central or remote
    logger.info(f"add a route to {to_dut} local sub... ")
    command = f'route add -net {net}/24 gw {gw}'
    output = rmt_host.send_command(command)
    logger.info(f'add a route to {to_dut} local sub result: {output}')
    time.sleep(10)
    routeoutput = rmt_host.send_command('ip -4 r')
    logger.info(f'routeoutput is : {routeoutput}')
    logger.info(f'{net}/24 via {gw}')
    if f'{net}/24 via {gw}' in routeoutput:
        return True
    else:
        return False


def check_dhcp_over_vpn_lease_num(leases_info, check_dict):
    slease = []
    dlease = []
    try:
        for lease in leases_info:
            # here are leases_info
            # [{'ip_address': '172.16.1.5', 'host_name': None, 'ethernet_address': 'FA-16-3E-A6-DD-C7', 'vendor': None,
            #   'lease_time': 'IN PROGRESS', 'tunnel_name': 'centralvpn'},
            #  {'ip_address': '172.16.1.7', 'host_name': None, 'ethernet_address': 'FA-16-3E-A6-DD-C7', 'vendor': None,
            #   'lease_time': '11/30/2022 01:46', 'tunnel_name': 'centralvpn'},
            #  {'ip_address': '172.16.1.10', 'host_name': None, 'ethernet_address': '2C-B8-ED-9D-81-00',
            #   'vendor': 'SONICWALL', 'lease_time': 'Static', 'tunnel_name': 'centralvpn'},
            #  {'ip_address': '172.16.1.11', 'host_name': None, 'ethernet_address': '2C-B8-ED-9D-81-00',
            #   'vendor': 'SONICWALL', 'lease_time': 'Static', 'tunnel_name': 'centralvpn'}]
            if ("/" in lease['lease_time']) and (":" in lease['lease_time']) or ('IN PROGRESS' in lease['lease_time']):
                if lease['ip_address'] in str(check_dict['dhcpleaseip']):
                    dlease.append(lease)
                    logger.info(f'dynamic lease:{dlease}')
            elif lease['lease_time'] == 'Static':
                if lease['ip_address'] in str(check_dict['staticleaseip']):
                    slease.append(lease)
                    logger.info(f'static lease:{slease}')
        return len(leases_info), len(dlease), len(slease)
    except Exception as e:
        logger.error(repr(e))
        return 0, 0, 0

# need add to common lib
# def delete_dhcp_over_vpn_dynamic_lease(self, lease_ip):
#     url = f'api/sonicos/reporting/dhcp-over-vpn/leases/ip/{lease_ip}'
#     dhcp_resp = self.fw.api_delete(url)
#     logger.info(f'dhcp_resp is : {dhcp_resp}')
#     return dhcp_resp
