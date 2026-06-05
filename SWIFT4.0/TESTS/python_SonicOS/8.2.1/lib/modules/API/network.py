from modules.API.network import WebproxyApi
from modules.API.network import InterfaceIPv4Api
from modules.API.network import ServiceObjectApi
from modules.API.network import ServiceGroupApi
from modules.API.network import AddressobjectsApi
from modules.API.network import InterfaceIPv6Api
from modules.API.network import ZoneObjectsApi
from modules.API.network import AddressgroupsApi
from modules.API.network import DHCPServerApi
from modules.API.network import NatpolicyApi
from modules.API.network import NetworkMonitorApi
from modules.API.network import DnsProxyApi
from modules.API.network import DnsSettingsApi
from modules.API.network import RoutePolicyApi
from modules.API.network import MacIPAntiSpoofApi
from modules.API.network import ArpApi
from modules.API.network import DNSSecurityApi
from modules.API.network import DnsFilteringApi
from modules.API.network import DnsPolicyApi
from modules.API.network import IpHelperApi
from modules.API.network import DDNSApi
from modules.API.network import MulticastApi


import copy
import json
import re
from runner.settings import logger
from modules.API.network import FailoverLbApi
from modules.API.network import DynamicRoutingApi
from modules.API.network import FloodProtectionApi
from modules.API.network import NeighborDiscoveryApi
from modules.API.network import VLANTranslationApi


class VLANTranslationApi(VLANTranslationApi):
     '''VLANTranslationApi class'''


class FailoverLbApi(FailoverLbApi):
    '''FailoverLbApi class'''
   
    def build_failover_groups_json(self,url,**kwargs):
        json_input = self.fw.api_get(url)
        path = json_input['failover_lb']['group'][0]
        # path['name'] = kwargs['name'].replace('+', ' ')
    
        logger.info('=========')
        logger.info(json_input)
        logger.info(path)
    
        if kwargs['interface' ] == 'X1':
            target = path['interface'][0]
        if kwargs['interface' ] == 'X2':
            target = path['interface'][1]
        if kwargs['interface' ] == 'X3':
            target = path['interface'][2]
        if kwargs['interface' ] == 'X4':
            target = path['interface'][3]
        if kwargs['interface' ] == 'X5':
            target = path['interface'][4]
           
        
        target['name'] = kwargs['interface']
        target['probe_type'] = kwargs['probe_type']

        if kwargs['probe_type'] == 'physical':
            target.pop('probe_condition')
            target.pop('main_target')
            target.pop('alternate_target')

        if kwargs['probe_type'] == 'logical':
            target['probe_condition'] = kwargs['probe_option']
            if 'main_target' and 'alternate_target' in target:
                target['main_target']['protocol'].clear()
                target['alternate_target']['protocol'].clear()
            else:
                target['main_target'] = {}
                target['alternate_target'] = {}
                target['main_target']['protocol'] = {}
                target['alternate_target']['protocol'] = {}
                target['default_target'] = {}
                target['default_target']['value'] = kwargs['default_value']

            if 'default_value' in target:
                target['default_target']['value'] = kwargs['default_value']
            
            if 'rank' in target:
                target['rank'] = kwargs['rank']

            if kwargs['main_protocol'] == 'tcp':
                target['main_target']['protocol']['tcp'] = {}
                target['main_target']['protocol']['tcp']['value'] = kwargs['main_value']
                target['main_target']['host'] = kwargs['main_host']
            elif kwargs['main_protocol'] == 'ping':
                target['main_target']['protocol'][kwargs['alter_protocol']] = kwargs['alter_value']
                target['main_target']['host'] = kwargs['alter_host']

            if kwargs['alter_protocol'] == 'tcp':
                target['alternate_target']['protocol']['tcp'] = {}
                target['alternate_target']['protocol']['tcp']['value'] = kwargs['alter_value']
                target['alternate_target']['host'] = kwargs['alter_host']
            elif kwargs['alter_protocol'] == 'ping':
                target['alternate_target']['protocol'][kwargs['alter_protocol']] = kwargs['alter_value']
                target['alternate_target']['host'] = kwargs['alter_host']

        return json_input


class DynamicRoutingApi(DynamicRoutingApi): 
 '''DynamicRoutingApi class'''


class WebproxyApi(WebproxyApi):
    '''WebproxyApi class'''

        
class DnsFilteringApi(DnsFilteringApi):
    '''DnsFilteringApi class'''


class InterfaceIPv4Api(InterfaceIPv4Api):
    '''InterfaceIPv4Api class'''


class ServiceObjectApi(ServiceObjectApi):
    '''ServiceObjectApi class'''


class ServiceGroupApi(ServiceGroupApi):
    '''ServiceGroupApi class'''


class AddressobjectsApi(AddressobjectsApi):
    '''AddressobjectsApi class'''


class AddressgroupsApi(AddressgroupsApi):
    '''AddressgroupsApi class'''


class InterfaceIPv6Api(InterfaceIPv6Api):
    '''InterfaceIPv6Api class'''

    def build_json_ipv6_interface(self, **kwargs):
        json_input = {}
        print(kwargs)
        ipv6_dhcpv6_json = {
            # "prefix_delegation": False,
            "prefix_delegation": {},
            "rapid_commit": False,
            #    "send_hints": False,
            "mode": "auto",
            "aftr_name_option": False
        }

        ipv6_static_json = {
            "ip": "::",
            "prefix_length": 64,

        }
        try:
            json_input = copy.deepcopy(self.initial_ipv6_interface_json)
            json_input['interfaces'][0]['ipv6']['name'] = kwargs['name']
            if 'vlan' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['vlan'] = int(kwargs['vlan'])
            # set common parameters for general tab
            if 'mgmt_http' in kwargs.keys():
                # mgmt_http only can be set when enable "Allow management via HTTP" in Administration tab
                json_input['interfaces'][0]['ipv6']['management']['http'] = kwargs['mgmt_http']
            if 'mgmt_https' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['https'] = kwargs['mgmt_https']
                if json_input['interfaces'][0]['ipv6']['management']['https']:
                    dict = {'https_redirect': True, }
                    json_input['interfaces'][0]['ipv6'].update(dict)
            if 'mgmt_ssh' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['ssh'] = kwargs['mgmt_ssh']
            if 'mgmt_ping' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['ping'] = kwargs['mgmt_ping']
            if 'mgmt_snmp' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['snmp'] = kwargs['mgmt_snmp']
            # mgmt source only support nsv build
            if 'https_source' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['https_source'] = kwargs['https_source']
            if 'ssh_source' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['ssh_source'] = kwargs['ssh_source']
            if 'ping_source' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['ping_source'] = kwargs['ping_source']
            if 'snmp_source' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['management']['snmp_source'] = kwargs['snmp_source']
            if 'user_https' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['user_login']['https'] = kwargs['user_https']
            if 'user_http' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['user_login']['http'] = kwargs['user_http']
            if 'ipv6_traffic' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['ipv6_traffic'] = kwargs['ipv6_traffic']
            if 'dad_transmit' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['duplicate_address_detection_transmits'] = kwargs['dad_transmit']
            if 'listen_router_advertisement' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['listen_router_advertisement'] = kwargs['listen_router_advertisement']
            if 'stateless_address_autoconfig' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['stateless_address_autoconfig'] = kwargs['stateless_address_autoconfig']
            if 'ipv6_traffic' in kwargs.keys():
                json_input['interfaces'][0]['ipv6']['ipv6_traffic'] = kwargs['ipv6_traffic']
            if (not kwargs['mgmt_https'] and not kwargs['user_https']) and "https_redirect" in kwargs.keys():
                logger.error('https_redirect only can be disabled and enabled when mgmt_https is enabled ')
            # set different parameters for different mode
            if kwargs['mode'] == 'auto':
                json_input = copy.deepcopy(self.initial_ipv6_auto_interface_json)
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode'] = {
                    "auto": True
                }
                #new add(2024/6/6)
                if 'mgmt_https' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['https'] = kwargs['mgmt_https']
                if 'mgmt_ssh' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['ssh'] = kwargs['mgmt_ssh']
                if 'mgmt_ping' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['ping'] = kwargs['mgmt_ping']
                if 'mgmt_snmp' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['snmp'] = kwargs['mgmt_snmp']
                if 'interface_identifier' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['interface_identifier'] = kwargs['interface_identifier']  
            elif kwargs['mode'] == 'dhcpv6':
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6'] = {}
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6'] = copy.deepcopy(ipv6_dhcpv6_json)
                # json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['prefix_delegation'] = kwargs['dhcpv6']['prefix_delegation']

                # set prefix_delegation
                if 'prefix_delegation' in kwargs['dhcpv6'].keys() and kwargs['dhcpv6']['prefix_delegation']:
                    # prefix_delegation_json = {
                    #     "preferred": {},
                    #     "send_hints": False
                    # }
                    # json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6'][
                    #     'prefix_delegation'] = copy.deepcopy(prefix_delegation_json)
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['prefix_delegation'] = \
                    kwargs['dhcpv6']['prefix_delegation']
                    if 'preferred_delegated_prefix' in kwargs['dhcpv6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['prefix_delegation'][
                            'preferred']['addr'] = kwargs['dhcpv6']['preferred_delegated_prefix_addr']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['prefix_delegation'][
                            'preferred']['prefix'] = kwargs['dhcpv6']['preferred_delegated_prefix_prefix']
                    if 'send_hints' in kwargs['dhcpv6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['prefix_delegation'][
                            'send_hints'] = kwargs['dhcpv6']['send_hints']
                if 'rapid_commit' in kwargs['dhcpv6'].keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['rapid_commit'] = \
                    kwargs['dhcpv6']['rapid_commit']
                # json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['send_hints'] = kwargs['dhcpv6']['send_hints']

                if 'mode' in kwargs['dhcpv6'].keys() and kwargs['dhcpv6']['mode'] == 'manual':
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['mode'] = 'manual'
                    if 'info_only' in kwargs['dhcpv6'] and kwargs['dhcpv6']['info_only']:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['info_only'] = True
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['info_only'] = False
                if 'mode' in kwargs['dhcpv6'].keys() and kwargs['dhcpv6']['mode'] == 'auto':
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['mode'] = 'auto'
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['aftr_name_option'] = \
                kwargs['dhcpv6']['aftr_name_option']
            elif kwargs['mode'] == 'pppoe6':
                if 'listen_router_advertisement' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['listen_router_advertisement'] = kwargs['listen_router_advertisement']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6'] = {}
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['inactivity'] = {}
                if kwargs['pppoe6']['inactivity']:
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['inactivity']['value'] = kwargs['pppoe6']['inactivity']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['reconnect'] = {}
                if kwargs['pppoe6']['reconnect']:
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['reconnect']['value'] = kwargs['pppoe6']['reconnect']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['lcp_echo_packets'] = kwargs['pppoe6']['lcp_echo_packets']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['ncp_neg_retrans'] = kwargs['pppoe6']['ncp_neg_retrans']
                if 'mode_assign' not in kwargs['pppoe6']:
                    logger.error('Please specify mode_assign to one of auto, dhcpv6, static')
                    return False
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['mode_assignment'] = kwargs['pppoe6']['mode_assign']
                if kwargs['pppoe6']['mode_assign'] == 'auto':
                    json_input['interfaces'][0]['ipv6'].pop('listen_router_advertisement')
                elif kwargs['pppoe6']['mode_assign'] == 'dhcpv6':
                    if 'dhcp_mode' in kwargs['pppoe6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['mode'] = kwargs['pppoe6']['dhcp_mode']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['prefix_delegation'] = kwargs['pppoe6']['prefix_delegation']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['rapid_commit'] = kwargs['pppoe6']['rapid_commit']
                elif kwargs['pppoe6']['mode_assign'] == 'static':

                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['gateway'] = kwargs['pppoe6']['gateway']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['ip'] = kwargs['pppoe6']['ip']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['prefix_length'] = kwargs['pppoe6']['prefix_length']

                    if 'dns' in str(kwargs['pppoe6'].keys()):
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['primary'] = kwargs['pppoe6']['dns1']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['secondary'] = kwargs['pppoe6']['dns2']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['tertiary'] = kwargs['pppoe6']['dns3']

                    if 'advertise_subnet_prefix' in kwargs['pppoe6']:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['advertise_subnet_prefix'] = kwargs['pppoe6']['advertise_subnet_prefix']

                    if 'router_advertisement' in kwargs['pppoe6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['enable'] = kwargs['pppoe6']['router_advertisement']['enable']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['interval'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['interval']['min'] = kwargs['pppoe6']['router_advertisement']['interval_min']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['interval']['max'] = kwargs['pppoe6']['router_advertisement']['interval_max']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['link_mtu'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['link_mtu']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['link_mtu']['value'] = kwargs['pppoe6']['router_advertisement']['link_mtu']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['reachable_time'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['reachable_time']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['reachable_time']['value'] = kwargs['pppoe6']['router_advertisement']['reachable_time']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['retransmit_timer'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['retransmit_timer']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['retransmit_timer']['value'] = kwargs['pppoe6']['router_advertisement']['retransmit_timer']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['current_hop_limit'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['current_hop_limit']['value'] = kwargs['pppoe6']['router_advertisement']['current_hop_limit']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['router'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['router']['lifetime'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['router']['lifetime']['value'] = kwargs['pppoe6']['router_advertisement']['router_lifetime']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['router']['preference'] = kwargs['pppoe6']['router_advertisement']['router_preference']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['managed'] = kwargs['pppoe6']['router_advertisement']['managed']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement']['other_config'] = kwargs['pppoe6']['router_advertisement']['other_config']
            elif kwargs['mode'] == 'static':
                if kwargs['zone'] == 'WAN':
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode'] = {
                        "static": {
                            "ip": "::",
                            "prefix_length": 64,
                            # "dns": {
                            #     "primary": "::",
                            #     "secondary": "::",
                            #     "tertiary": "::"
                            # },
                            "gateway": "::",
                            "advertise_subnet_prefix": False,
                            "router_advertisement": {
                                "enable": False,
                                "interval": {
                                    "min": 200,
                                    "max": 600
                                },
                                "link_mtu": {
                                },
                                "reachable_time": {
                                },
                                "retransmit_timer": {
                                },
                                "current_hop_limit": {
                                    "value": 64
                                },
                                "router": {
                                    "lifetime": {
                                        "value": 1800
                                    },
                                    "preference": "medium"
                                },
                                "managed": False,
                                "other_config": False
                            }
                        }
                    }
                else:
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode'] = {
                        "static": {
                            "ip": "::",
                            "prefix_length": 64,
                            "advertise_subnet_prefix": False,
                            "router_advertisement": {
                                "enable": False,
                                "interval": {
                                    "min": 200,
                                    "max": 600
                                },
                                "link_mtu": {
                                },
                                "reachable_time": {
                                },
                                "retransmit_timer": {
                                },
                                "current_hop_limit": {
                                    "value": 64
                                },
                                "router": {
                                    "lifetime": {
                                        "value": 1800
                                    },
                                    "preference": "medium"
                                },
                                "managed": False,
                                "other_config": False
                            }
                        }
                    }
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['ip'] = kwargs['ip']
                if 'prefix_length' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['prefix_length'] = kwargs[
                        'prefix_length']
                if 'adv_pref' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['advertise_subnet_prefix'] = \
                    kwargs['adv_pref']
                if 'router_adv' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'enable'] = kwargs['router_adv']
                if 'ra_min' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'interval']['min'] = kwargs['ra_min']
                if 'ra_max' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'interval']['max'] = kwargs['ra_max']
                if 'link_mtu' in kwargs.keys():
                    if kwargs['link_mtu'] == 0:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'link_mtu'] = {}
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'link_mtu']['value'] = kwargs['link_mtu']
                if 'reach_time' in kwargs.keys():
                    if kwargs['reach_time'] == 0:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'reachable_time'] = {}
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'reachable_time']['value'] = kwargs['reach_time']
                if 'retrans_time' in kwargs.keys():
                    if kwargs['retrans_time'] == 0:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'retransmit_timer'] = {}
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'retransmit_timer']['value'] = kwargs['retrans_time']
                if 'current_hop_limit' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'current_hop_limit']['value'] = kwargs['current_hop_limit']
                if 'lifetime' in kwargs.keys():
                    if kwargs['lifetime'] == 0:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'router']['lifetime'] = {}
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                            'router']['lifetime']['value'] = kwargs['lifetime']
                if 'managed' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'managed'] = kwargs['managed']
                if 'other_config' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                        'other_config'] = kwargs['other_config']
                # dns parameter and gateway only wan interfaces
                if 'dns' in kwargs.keys():
                    dict = {"dns": {
                        "primary": "::",
                        "secondary": "::",
                        "tertiary": "::"
                    },
                    }
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static'].update(dict)
                    if 'primary' in kwargs['dns'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['dns']['primary'] = \
                        kwargs['dns']['primary']
                    if 'secondary' in kwargs['dns'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['dns']['secondary'] = \
                        kwargs['dns']['secondary']
                    if 'tertiary' in kwargs['dns'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['dns']['tertiary'] = \
                        kwargs['dns']['tertiary']
                if 'gateway' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['gateway'] = kwargs[
                        'gateway']
                if 'advertise_subnet_prefix' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['advertise_subnet_prefix'] = \
                    kwargs['advertise_subnet_prefix']
                if 'listen_router_advertisement' in kwargs:
                    json_input['interfaces'][0]['ipv6']['listen_router_advertisement'] = kwargs['listen_router_advertisement']
                if 'stateless_address_autoconfig' in kwargs:
                    json_input['interfaces'][0]['ipv6']['stateless_address_autoconfig'] = kwargs['stateless_address_autoconfig']
                if 'interface_identifier' in kwargs:
                    json_input['interfaces'][0]['ipv6']['interface_identifier'] = kwargs['interface_identifier']
        except Exception as e:
            print(e)
        # print("interface json obtained")
        print(f'json_input is \n{json_input}')
        return json_input

    
class ZoneObjectsApi(ZoneObjectsApi):
    '''ZoneObjectsApi class'''


class DHCPServerApi(DHCPServerApi):
    '''DHCPServerApi class'''


class NatpolicyApi(NatpolicyApi):
    '''NatpolicyApi class'''

        
class NetworkMonitorApi(NetworkMonitorApi):
    '''NetworkMonitorApi class'''

    
class DnsProxyApi(DnsProxyApi):
    '''DnsProxyApi class'''
    default_options = {
   
        'enforce_all_dns_requests': False,
        'dns_cache': True
    }

    def __init__(self,fw):
       
        super().__init__(fw)
        self.initial_dnsproxy_json ={
            "dns_proxy": {
                "enforce_all_dns_requests": False,
                "dns_cache": True
            }
        }

    def build_json_dnsproxy(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_dnsproxy_json)
            json_input['dns_proxy']['enforce_all_dns_requests'] = kwargs['enforce_all_dns_requests']
            json_input['dns_proxy']['dns_cache'] = kwargs['dns_cache']
        except KeyError:
            logger.info("Error: In creating JSON for dnsproxy")    
        return json_input 

    def config_dnsproxy(self, msg=False, **kwargs):
        self.options = dict(DnsProxyApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options 
        json_input = self.build_json_dnsproxy(**kwargs)
        dns_proxy_resp = self.fw.api_put(self.url, msg, data=json_input)
        return dns_proxy_resp 



class DnsSettingsApi(DnsSettingsApi):
    '''DnsSettingsApi class'''

    
class RoutePolicyApi(RoutePolicyApi):
    '''RoutePolicyApi class'''

    
class MacIPAntiSpoofApi(MacIPAntiSpoofApi):
    '''MacIPAntiSpoofApi class'''


class ArpApi(ArpApi):
    '''Arp class'''

        
class DNSSecurityApi(DNSSecurityApi):
    '''DNSSecurity class'''

        
class DnsPolicyApi(DnsPolicyApi):
    '''DnsPolicyApi class'''


class IpHelperApi(IpHelperApi):
    '''IpHelperApi class'''

class FloodProtectionApi(FloodProtectionApi):
    '''FloodProtectionApi class'''

class NeighborDiscoveryApi(NeighborDiscoveryApi):
    '''NeighborDiscoveryApi class'''


class MulticastApi(MulticastApi):
    '''MulticastApiApi class'''


class DDNSApi(DDNSApi):
    '''DDNSApi'''