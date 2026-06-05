#!/usr/bin/python
import os
import sys
import getopt
import re
from definition.settings import json
from runner.settings import Params, logger
import time


def check_interface_ospfv3_status(dyroute_api, inf):
    output = dyroute_api.get_route_advanced_data()
    try:
        ipv6data = output['data']['ipv6']['interfaces']
        logger.info(ipv6data)
        for data in ipv6data:
            if f'"name": "{inf}"' in json.dumps(data):
                logger.info(data['OSPFv3']['neighborStatus'])
                status = data['OSPFv3']['neighborStatus']
                logger.info(f'ospfv3 status is {status}')
                if status > 0:           # -1 down ,0 down , 1 full
                    neibstatus = 'full'
                    return True, neibstatus
                else:
                    neighstatus = 'down'
                    return False, neighstatus
    except Exception as e:
        logger.error(repr(e))
        return False, 'error'


def check_ospfv3_hello_packets_num(resp, **kwargs):
    tag = []
    packets = resp.split('Packet number: ')
    packetin = f"in:{kwargs['iface_in']}"
    packetout = f"out:{kwargs['iface_out']}"
    ospftype = 'OSPF Type : 1'
    ospfversion = 'OSPF Version : 3'
    status = 'Generated (Sent Out)'
    tuples = (packetin, packetout, ospftype, ospfversion, status)
    for packet in packets:
        a = [x in packet for x in tuples]
        logger.info(a)
        if all(a):
            tag.append((packets))
    return len(tag)


def icmpv6_traffic_hit_check(resp, **kwargs):
    checkres = False
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
            checkres = True
    return checkres


# should add to System ->diag common_lib
# def get_tsr_dynamic_routing_protocol_setting(self, dynamic_pro):    #dynamic_pro = OSPF,OSPFv3,RIP,RIPing,BGP
#     self.download_tsr()
#     tsr_content = os.popen('cat /tmp/techSupport').read()
#     net_list = tsr_content.split('\n\n')
#     for net in net_list:
#         if f'Advanced Routing: {dynamic_pro} Settings' in net:
#             return net
#     return False


# should add to common_lib: cli_network_RouteCli
# def show_ospf3(self, mode=''):  ### mode = '' | 'neighbor' | 'database' | 'routes'
#     cmd = 'show routing ospfv3 '
#     if mode:
#         cmd = cmd + str(mode)
#     commands = [cmd]
#     result = self.fw.do_cli_commands(commands, tag=1)[1]
#     return result


# should add to common_lib: cli_network_RouteCli
# def show_ospf3_database(self, mode=''):  ### mode ='' | 'external' | 'inter-prefix' | 'inter-router' | 'intra-prefix' | 'link' | 'network' | 'router'
#     commands = ['configure', 'routing', 'ospfv3']
#     if mode:
#         commands.append(f'show ipv6 ospf database {mode}')
#     result = self.fw.do_cli_commands(commands, tag=1)[1]
#     return result


# should add to common_lib: api_network_DynamicRoutingApi
# def ospf3_config(self, msg=False, **kwargs):
#     '''
#     {"stream":"cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&
#     ZOspf3RouterId=10.10.10.10&
#     ZOspf3DefMetric=&
#     ZOspf3ABRType=1&
#     ZOspf3RefBW=100&
#     ZOspf3RedistStatics=off&
#     ZOspf3StaticsMetric=&
#     ZOspf3StaticsMType=2&
#     ZOspf3RedistConnected=off&
#     ZOspf3ConnectedMetric=&
#     ZOspf3ConnectedMType=2&
#     ZOspf3RedistRip=off&ZOspf3RipMetric=&
#     ZOspf3RipMType=2&
#     ZebosDefRtPbrMetric=110&
#     ZebosSyncEcmpToSonicOS=off"}
#     '''
#
#     ospf3_setting_dict = copy.deepcopy(DynamicRoutingApi.ospf3_setting)
#     ospf3_setting_dict.update(kwargs)
#     ospf3_dict = ospf3_setting_dict
#
#     abr_type_dict = {
#         'standard': '0',
#         'cisco': '1',
#         'ibm': '2',
#         'shortcut': '3',
#     }
#     logger.info(ospf3_dict)
#     cgi = 'cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&'
#     cgi += 'ZOspf3RouterId=' + ospf3_dict['router_id'] + '&'
#     cgi += 'ZOspf3DefMetric=&'
#     cgi += 'ZOspf3ABRType=' + abr_type_dict[ospf3_dict['abr_type']] + '&'
#     cgi += 'ZOspf3RefBW=' + str(ospf3_dict['bw']) + '&'
#
#     cgi += 'ZOspf3RedistStatics=' + ospf3_dict['static_route'] + '&'
#     if ospf3_dict['static_route'] == 'on':
#         cgi += f"ZOspf3StaticsMetric={ospf3_dict['static_metric']}&ZOspf3StaticsMType={ospf3_dict['static_metric_type']}&"
#     else:
#         cgi += 'ZOspf3StaticsMetric=&ZOspf3StaticsMType=2&'
#
#     cgi += 'ZOspf3RedistConnected=' + ospf3_dict['connect_network'] + '&'
#     if ospf3_dict['connect_network'] == 'on':
#         cgi += f"ZOspf3ConnectedMetric={ospf3_dict['connect_metric']}&ZOspf3ConnectedMType={ospf3_dict['connect_metric_type']}&"
#     else:
#         cgi += 'ZOspf3ConnectedMetric=&ZOspf3ConnectedMType=2&'
#
#     cgi += 'ZOspf3RedistRip=' + ospf3_dict['rip_route'] + '&'
#     if ospf3_dict['rip_route'] == 'on':
#         cgi += f"ZOspf3RipMetric={ospf3_dict['rip_metric']}&ZOspf3RipMType={ospf3_dict['rip_metric_type']}&"
#     else:
#         cgi += 'ZOspf3RipTag=&ZOspf3RipMetric=&ZOspfRipMType=2&'
#
#     cgi += 'ZebosDefRtPbrMetric=' + ospf3_dict['route_metric'] + '&'
#     cgi += 'ZebosSyncEcmpToSonicOS=' + ospf3_dict['allow_ecmp_route']
#     self.default_cgi['stream'] = cgi
#     res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
#     return res

# should add to common_lib: api_network_DynamicRoutingApi
# def set_ospf3(self, msg=False, **kwargs):
#     '''
#     {"stream":"&cgiaction=none&tableIndex=0&refresh_page=newRoutePolicies.html&ZOspf3Mode=1&ZOspf3Area=0&
#     ZOspf3AreaType=0&ZOspf3InstId=0&ZOspf3DeadInterval=40&ZOspf3HelloInterval=10&ZOspf3IfCost=9&ZOspf3IfAutoCost=on
#     &ZOspf3IfPriority=1&auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+X0+%28LAN%29+OSPFv3+Configuration
#     }
#     '''
#     ospf3_setting_dict = copy.deepcopy(DynamicRoutingApi.default_ospf3)
#     # ospf3_dict.update(kwargs)
#     # kwargs = ospf3_dict
#     ospf3_setting_dict.update(kwargs)
#     ospf3_dict = ospf3_setting_dict
#     if 'interface' not in ospf3_dict:
#         logger.error('Please specify interface when config rip.')
#         return False
#     elif 'V' in ospf3_dict['interface'] or 'v' in ospf3_dict['interface']:
#         match = re.search('(X\d+):V(\d+)', ospf3_dict['interface'], re.I)
#         if match:
#             name = match.group(1)
#             vlan = match.group(2)
#             index = self.get_vlan_index(name, vlan)
#     else:
#         index = ospf3_dict['interface'].replace('X', '')
#     cgi = '&cgiaction=none&tableIndex=' + index + '&refresh_page=newRoutePolicies.html&'
#     mode = {
#         'disable': '0',
#         'enable': '1',
#         'passive': '2'
#     }
#     area_type = {
#         'normal': '0',
#         'stub area': '1',
#         'totally stubby area': '2',
#     }
#     ospf3_mode = mode[ospf3_dict['mode']]
#     cgi += 'ZOspf3Mode=' + ospf3_mode + '&'
#     if ospf3_mode == '2':
#         cgi += 'ZOspfArea=' + str(ospf3_dict['area']) + '&'
#     else:
#         cgi += 'ZOspf3Area=' + str(ospf3_dict['area']) + '&'
#         cgi += 'ZOspf3AreaType=' + area_type[ospf3_dict['area_type']] + '&'
#         cgi += 'ZOspf3InstId=0&'
#         cgi += 'ZOspf3DeadInterval=' + str(ospf3_dict['dead_interval']) + '&'
#         cgi += 'ZOspf3HelloInterval=' + str(ospf3_dict['hello_interval']) + '&'
#         cgi += 'ZOspf3IfCost=9&'
#         cgi += 'ZOspf3IfAutoCost=' + str(ospf3_dict['autocost']) + '&'
#         cgi += 'ZOspf3IfPriority=' + str(ospf3_dict['priority']) + '&'
#         # cgi += 'ZOspf3IfPriority=1'
#     cgi += 'auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+' + ospf3_dict[
#         'interface'] + '+%28LAN%29+OSPFv3+Configuration'
#     self.default_cgi['stream'] = cgi
#     logger.info(f'cgi is:{cgi}')
#     res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
#     return res

