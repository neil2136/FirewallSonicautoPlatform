import copy
import json
import re
import ipaddress
from netaddr import IPAddress
from collections import OrderedDict
from runner.settings import logger
from runner.utils.assertion import Assertion


class WebproxyApi:
    '''WebproxyApi class'''
    default_options = {
        'server': '',
        'port': '',
        'bypass_upon_failure': False,
        'forward_public_requests': False,
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/web-proxy/base'
        self.initial_webproxy_json = {
            "web_proxy": {
                "server": None, "port": {}, "bypass_upon_failure": None, "forward_public_requests": None
            }
        }

    def config_webproxy(self, msg=False, **kwargs):
        self.options = dict(WebproxyApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_webproxy(kwargs['server'], kwargs['port'], kwargs['bypass_upon_failure'],
                                              kwargs['forward_public_requests'])
        webproxy_resp = self.fw.api_put(self.url, msg, data=json_input)
        return webproxy_resp

    def build_json_webproxy(self, server, port, bypass_upon_failure, forward_public_requests):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_webproxy_json)
            json_input['web_proxy']['server'] = server
            json_input['web_proxy']['port']['value'] = int(port)
            json_input['web_proxy']['bypass_upon_failure'] = bypass_upon_failure
            json_input['web_proxy']['forward_public_requests'] = forward_public_requests
            logger.info("webproxy json obtained")
            logger.info(json_input)
        except KeyError:
            logger.info("Error: In creating JSON for webporxy")
        return json_input

    def edit_bypass_upon_failure(self, action, msg=False):
        json_input = {"web_proxy": {"bypass_upon_failure": action, }}
        webproxy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return webproxy_resp

    def edit_forward_public_requests(self, action, msg=False):
        json_input = {"web_proxy": {"forward_public_requests": action, }}
        webproxy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return webproxy_resp

    def show_webproxy(self):
        response = self.fw.api_get(self.url)
        return response

    def add_user_proxy_server(self, *ips, msg=False):
        json_input = {"web_proxy": {"user_proxy_server": []}}
        for ip in ips:
            json_input['web_proxy']['user_proxy_server'].append({"server_host": ip})
        webproxy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return webproxy_resp

    def del_user_proxy_server(self, *ips, msg=False):
        json_input = {"web_proxy": {"user_proxy_server": []}}
        for ip in ips:
            json_input['web_proxy']['user_proxy_server'].append({"server_host": ip})
        webproxy_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return webproxy_resp


class InterfaceIPv4Api:
    '''InterfaceIPv4Api class'''
    default_options = {
        'if': 'x2',
        'zone': 'WAN',
        'mode': 'static',
        'comment': 'test',
        'mac_override': False,
        'shut_down': False,
        # '344': False,
        'mgmt_https': False,
        'mgmt_ping': False,
        'mgmt_ssh': False,
        'mgmt_snmp': False,
        # 'https_redirect': True,
        'user_http': False,
        'user_https': False,
        'ip': '0.0.0.0',
        'netmask': '255.255.255.0',
        'gateway': '0.0.0.0',
        # advance tab
        # 'link_speed': 'auto', #half-100,half-10,full-10,full-100,full-1000,auto
        # 'shutdown_port': False,
        'flow_reporting': True,
        'multicast': False,
        # 'dns_proxy': False,
        'cos_8021p': False,
        'exclude_route': False,
        'management_traffic_only': False,
        # 'fragment_packets': True,
        # 'ignore_df_bit': False,
        'asymmetric_route': False,
        # 'send_icmp_fragmentation': False,
        'bandwidth_management': False,
        # 'redundancy_aggregation_port': 'None',# None,aggregation,redundancy
        # 'aggregation_ports': [],
        # 'redundancy_port': '',
        # l2bridge option
        'bridge_to': 'X0',
        'bridge_block_non_ip': False,
        'bridge_captive': False,
        # 'bridge_only_sniff': False,
        'bridge_route_on_bridge_pair': False,
        'bridge_stateless': False,
        'bridge_vlan_filter': 'block',  # block or allow
        'bridge_vlan_list': [1, 2, 3],
        #
        'transparent_range': '',
        'transparent_if': 'x1',
        # native
        'nativebridge_to': '-1',
        'nativebridge_do_fw': False,
        'firewalling': False,
        # wire mode
        'wire_type': 'bypass',  # bypass, inspect, secure
        'wire_paired_interface': '',
        'wire_paired_zone': '',
        'wire_dis_inspection': True,
        'wire_link_propagation': True,
        # tap mode
        'stateful_inspection': True,
        'dns1': '0.0.0.0',
        'dns2': '0.0.0.0',
        'dns3': '0.0.0.0',
        # dhcp mode
        'dhcp_hostname': 'dhcphost',
        'dhcp_renew_on_startup': False,
        'dhcp_renew_on_link_up': False,
        'dhcp_initiate_renewals_with_discover': False,
        'dhcp_force_discover_interval': 0,
        # pppoe mode
        'pppoe_user': '',
        'pppoe_passwd': '',
        'pppoe_service': '',
        'pppoe_schedule': 'always_on',
        'pppoe_dynamic': True,
        'pppoe_inactivity': 0,
        'pppoe_lcp_echo_packets': False,
        'pppoe_reconnect': 0,
        # pptp mode
        'pptp_hostname': 'pptp-hostname',
        'pptp_dynamic': True,
        'pptp_server': '0.0.0.0',
        'pptp_user': 'pptp-test',
        'pptp_passwd': 'password',
        'pptp_netmask': '255.255.255.0',
        'pptp_inactivity': 10,
        'pptp_schedule': 'always_on',
        # l2tp mode
        'l2tp_schedule': 'always_on',
        'l2tp_user': 'l2tp-test',
        'l2tp_server': '0.0.0.0',
        'l2tp_passwd': 'password',
        'l2tp_hostname': 'l2tp-hostname',
        'l2tp_inactivity': 10,
        'l2tp_dynamic': True,
        'l2tp_shared_secret': '',
        'l2tp_netmask': '255.255.255.0',
        # wlan zone
        'sp_limit': 16,
        'reserve_address': 'dynamic',
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/interfaces/ipv4'
        self.url_tunnel_4to6 = 'api/sonicos/tunnel-interfaces/4to6'
        self.url_tunnel_vpn = 'api/sonicos/tunnel-interfaces/vpn'
        self.initial_ipv4_wan_json = {
            "interfaces": [{
                "ipv4": {
                    "name": None,
                    "comment": None,
                    "ip_assignment": {
                        "zone": 'WAN',
                        "mode": {
                            # "static": {
                            # "ip": None,
                            # "netmask": "255.255.255.0",
                            # "gateway": None
                            # }
                        }
                    },
                    "management": {
                        "https": False,
                        "ping": False,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "link_speed": {},
                    #         "https_redirect": True,
                    "mac": {
                        "default": True
                        # "override": "AA:BB:CC:DD:EE:FF"
                    },
                    # "shutdown_port": False,
                    "flow_reporting": True,
                    "multicast": False,
                    "cos_8021p": False,
                    "exclude_route": False,
                    "asymmetric_route": False,
                    "mtu": 1500
                }
            }]
        }

        self.initial_ipv4_mgmt_json = {
            "interfaces": [{
                "ipv4": {
                    "name": "MGMT",
                    "comment": "Default MGMT",
                    "ip_assignment": {
                        "zone": 'MGMT',
                        "mode": {
                            "static": {
                                "ip": "192.168.1.254",
                                "netmask": "255.255.255.0",
                                "gateway": None
                            }
                        }
                    },
                    "management": {
                        "https": True,
                        "ping": True,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "link_speed": {},
                    "mac": {
                        "default": True
                        # "override": "AA:BB:CC:DD:EE:FF"
                    },
                    # "shutdown_port": False,
                    "flow_reporting": True,
                    "mtu": 1500
                }
            }]
        }
        self.initial_ipv4_lan_json = {
            "interfaces": [{
                "ipv4": {
                    "name": None,
                    "comment": None,
                    "ip_assignment": {
                        "zone": 'LAN',
                        "mode": {
                            # "static": {
                            # "ip": None,
                            # "netmask": "255.255.255.0",
                            # "gateway": None
                            # }
                        }
                    },
                    "management": {
                        "https": True,
                        "ping": True,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "link_speed": {},
                    "mac": {
                        "default": True
                        # "override": "AA:BB:CC:DD:EE:FF"
                    },
                    # "shutdown_port": False,
                    "flow_reporting": True,
                    "multicast": False,
                    "cos_8021p": False,
                    "exclude_route": False,
                    "routed_mode": {
                    },
                    "asymmetric_route": False,
                    "mtu": 1500
                }
            }]
        }

        self.initial_ipv4_l2bridge_json = {
            "interfaces": [{
                "ipv4": {
                    "name": None,
                    "comment": None,
                    "ip_assignment": {
                        "zone": 'LAN',
                        "mode": {
                            # "static": {
                            # "ip": None,
                            # "netmask": "255.255.255.0",
                            # "gateway": None
                            # }
                        }
                    },
                    "management": {
                        "https": True,
                        "ping": True,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "link_speed": {},
                    "mac": {
                        "default": True
                        # "override": "AA:BB:CC:DD:EE:FF"
                    },
                    # "shutdown_port": False,
                    "flow_reporting": True,
                    "multicast": False,
                    "cos_8021p": False,
                    "exclude_route": False,
                    "asymmetric_route": False,
                    "mtu": 1500
                }
            }]
        }

        self.initial_ipv4_wlan_json = {
            "interfaces": [{
                "ipv4": {
                    "name": 'W0',
                    "comment": 'test WLAN',
                    "ip_assignment": {
                        "zone": 'WLAN',
                        "mode": {
                            # "static": {
                            #     "ip": "11.11.11.11",
                            #     "netmask": "255.255.255.0"
                        }
                    },
                    "management": {
                        "https": True,
                        "ping": True,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "link_speed": {
                    #     "auto_negotiate": True
                    # },
                    "mac": {
                        "default": True
                        # "override": "AA:BB:CC:DD:EE:FF"
                    },
                    # "shutdown_port": False,
                    "flow_reporting": True,
                    "multicast": False,
                    "cos_8021p": False,
                    "exclude_route": False,
                    "asymmetric_route": False,
                    "mtu": 1400,
                    "sonicpoint": {
                        "limit": {
                            "value": 8
                        },
                        "reserve_address": {
                            "dynamic": True
                        }
                    }
                }
            }]
        }

        self.initial_ipv4_safemode_json = {
            "interfaces": [{
                "ipv4": {
                    "shutdown_port": False,
                    "management_traffic_only": False,
                    "flow_reporting": True,
                    "exclude_route": False,
                    "mtu": 1500,
                    # "link_speed": {"auto_negotiate": True},
                    "port": {"redundancy_aggregation": False},
                    "name": "X2",
                    "ip_assignment": {
                        "zone": "LAN",
                        "mode": {
                            "wire_mode": {
                                "paired_interface": {"interface": "X3"},
                                "paired_interface_zone": "LAN",
                                "linkstate_propagation": False,
                                "type": "bypass"
                            }
                        }
                    }
                }
            }]
        }

        self.initial_wlan_tunnel_json = {
            "interfaces": [{
                "ipv4": {
                    "management": {
                        "https": False,
                        "ping": False,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    "comment": "",
                    "sonicpoint": {
                        "limit": {"value": 16},
                        "reserve_address": {"dynamic": True}
                    },
                    "mac": {"default": True},
                    "cos_8021p": False,
                    "management_traffic_only": False,
                    "flow_reporting": False,
                    "multicast": False,
                    "exclude_route": False,
                    "asymmetric_route": False,
                    "routed_mode": {},
                    "mtu": 1500,
                    "name": "X1",
                    "ip_assignment": {
                        "zone": "WLAN",
                        "mode": {
                            "static": {
                                "ip": "2.2.2.2",
                                "netmask": "255.255.255.0"}
                        }
                    },
                    "tunnel": 1}
            }]
        }

        self.initial_ipv4_vpn_tunnel_json = {
            "tunnel_interfaces": [
                {
                    "vpn": {
                        "comment": 'test vpn tunnel',
                        "name": '',
                        "ip_assignment": {
                            "zone": 'VPN',
                            "mode": {
                                "static": {
                                    "ip": "0.0.0.0",
                                    "netmask": "255.255.255.0",
                                }
                            }
                        },
                        'policy': 'test-vpntunnel',
                        "management": {
                            "https": True,
                            "ping": True,
                            "snmp": False,
                            "ssh": False
                        },
                        "user_login": {
                            "http": False,
                            "https": False
                        },
                        "flow_reporting": True,
                        "multicast": False,
                        "asymmetric_route": False
                    }
                }
            ]
        }

        self.initial_4to6_json = {  # edit by cyuan, init_json wrong
            "tunnel_interfaces": [
                {
                    "4to6": {
                        "name": "gre 4to6",
                        "type": {
                        },
                        "flow_reporting": True,
                        "fragment_packets": True,
                        "ignore_df_bit": False,
                        "send_icmp_fragmentation": True,
                        "comment": "GRE 4to6 Tunnel"
                    }
                }
            ]
        }

        self.initial_ipv4_unassign_json = {
            "interfaces": [
                {
                    "ipv4": {
                        "name": "",
                        "ip_assignment": {
                        },
                        "native_bridge": {
                        },
                        #                 "link_speed": {
                        #                     "auto_negotiate": True
                        #                 },
                        "mac": {
                            "default": True
                        },
                        "shutdown_port": False,
                        "flow_reporting": True,
                        "cos_8021p": False,
                        "exclude_route": False,
                        "asymmetric_route": False,
                        "management_traffic_only": False,
                        "port": {
                            "redundancy_aggregation": False
                        },
                        "mtu": 1500,
                        "bandwidth_management": {
                            "egress": {
                            },
                            "ingress": {
                            }
                        }
                    }
                }
            ]
        }

        self.initial_ipv4_vlan_unassign_json = {
            "interfaces": [
                {
                    "ipv4": {
                        "mac": {
                            "default": True
                        },
                        "flow_reporting": False,
                        "exclude_route": False,
                        "asymmetric_route": False,
                        "mtu": 1500,
                        "default_8021p_cos": {
                            "enable": False,
                        },
                        "name": "",
                        "ip_assignment": {},
                        "native_bridge": {},
                        "vlan": 0,
                    }
                }
            ]
        }

        self.initial_ipv4_vlan_wiremode_json = {
            "interfaces": [
                {
                    "ipv4": {
                        "flow_reporting": True,
                        "exclude_route": False,
                        "default_8021p_cos": {
                            "enable": False,
                        },
                        "mtu": 1500,
                        "name": "",
                        "ip_assignment": {
                            "zone": "LAN",
                            "mode": {
                                "wire_mode": {
                                    "paired_interface": {
                                        "interface": ""
                                    },
                                    "paired_interface_zone": "LAN",
                                    "linkstate_propagation": False,
                                    "type": "bypass"
                                }
                            }
                        },
                        "vlan": 0
                    }
                }
            ]
        }

        self.initial_ipv4_vlan_wlan_json = {
            "interfaces": [
                {
                    "ipv4": {
                        "mac": {
                            "default": True
                        },
                        "flow_reporting": False,
                        "multicast": False,
                        "exclude_route": False,
                        "asymmetric_route": False,
                        "routed_mode": {},
                        "mtu": 1500,

                        "comment": "",
                        "name": "W0",
                        "ip_assignment": {
                            "zone": "WLAN",
                            "mode": {
                                "static": {
                                    "ip": "",
                                    "netmask": "255.255.255.0"
                                }
                            }
                        },
                        "vlan": 0
                    }
                }
            ]
        }

    def config_interface(self, msg=False, **kwargs):
        self.options = dict(InterfaceIPv4Api.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        kwargs['if'].upper()
        if kwargs['if'] == 'X0':
            kwargs['zone'] = 'LAN'
        if kwargs['if'] == 'X1':
            kwargs['zone'] = 'WAN'
        if kwargs['if'] == 'W0':
            kwargs['zone'] = 'WLAN'
        if kwargs['if'] == 'MGMT':
            kwargs['zone'] = 'MGMT'
        if kwargs['zone'].upper() in ['LAN', 'WAN', 'WLAN', 'SSLVPN', 'VPN', 'MULTICAST', 'DMZ']:
            kwargs['zone'] = kwargs['zone'].upper()
        if kwargs['zone'] == 'WAN':
            json_input = self.build_json_wan(**kwargs)
        elif kwargs['zone'] == 'LAN' or kwargs['zone'] == 'DMZ':
            json_input = self.build_json_lan(**kwargs)
        elif kwargs['zone'] == 'WLAN':
            json_input = self.build_json_wlan(**kwargs)
        elif kwargs['zone'] == 'MGMT':
            json_input = self.build_json_mgmt(**kwargs)
        elif kwargs['zone'] == 'VPN':
            json_input = self.build_json_vpntunnel(**kwargs)
        else:
            json_input = self.build_json_lan(**kwargs)

        if 'redundancy_aggregation_port' in kwargs.keys():
            print("Run here")
            tmp_json = self._get_redundancy_aggregation_ports(**kwargs)
            print(tmp_json)
            json_input["interfaces"][0]["ipv4"].update(tmp_json)

        if kwargs['mode'] == 'portshield':
            json_input['interfaces'][0]['ipv4'].pop('flow_reporting')
            json_input['interfaces'][0]['ipv4'].pop('multicast')
            json_input['interfaces'][0]['ipv4'].pop('asymmetric_route')
            json_input['interfaces'][0]['ipv4'].pop('routed_mode')
            json_input['interfaces'][0]['ipv4'].pop('cos_8021p')
            json_input['interfaces'][0]['ipv4'].pop('exclude_route')
            json_input['interfaces'][0]['ipv4'].pop('mtu')

        if kwargs['mode'] == 'nativebridge':
            json_input['interfaces'][0]['ipv4'].pop('comment')
            json_input['interfaces'][0]['ipv4'].pop("management")
            json_input['interfaces'][0]['ipv4'].pop("user_login")
            json_input['interfaces'][0]['ipv4'].pop("multicast")
            json_input['interfaces'][0]['ipv4'].pop("routed_mode")

        logger.info(json_input)
        if kwargs['zone'] == 'VPN':
            url = self.url_tunnel_vpn + '/name/' + kwargs["tunnel_name"]
        else:
            url = self.url + '/name/' + kwargs['if']
        if "one_arm_mode" in kwargs.keys() and kwargs['one_arm_mode']:
            if "one_arm_peer" in kwargs.keys() and kwargs['one_arm_peer']:
                json_input['interfaces'][0]['ipv4']['one_arm_mode'] = True
                json_input['interfaces'][0]['ipv4']['one_arm_peer'] = kwargs['one_arm_peer']
            else:
                logger.error('not one_arm_peer key, value in kwargs...')
                return False

        interface_resp = self.fw.api_put(url, msg, data=json_input)
        return interface_resp

    def config_vlan_interface_to_wiremode(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.initial_ipv4_vlan_wiremode_json)
        json_input['interfaces'][0]['ipv4']['name'] = kwargs['if']
        json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
        json_input['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['paired_interface_zone'] = kwargs[
            'wire_paired_zone']
        json_input['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['paired_interface']['interface'] = \
        kwargs['wire_paired_interface']
        json_input['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type'] = kwargs['type']
        json_input['interfaces'][0]['ipv4']['vlan'] = kwargs['vlan_id']
        logger.info(json_input)
        interface = kwargs['if'].split(":")[0]
        url = self.url + '/name/' + interface + '/vlan/' + str(kwargs['vlan_id'])
        logger.info(url)
        interface_resp = self.fw.api_put(url, msg, data=json_input)
        return interface_resp

    def add_vlan_interface_under_wlan(self, msg=False, **kwargs):
        json_input = copy.deepcopy(self.initial_ipv4_vlan_wlan_json)
        logger.info(json_input)
        if 'vlan_tag' in kwargs.keys():
            json_input['interfaces'][0]['ipv4']['vlan'] = kwargs['vlan_tag']
        if 'ip' in kwargs.keys():
            json_input['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip'] = kwargs['ip']
        logger.info(json_input)
        interface_resp = self.fw.api_post(self.url, msg, data=json_input)
        return interface_resp

    def add_gre4to6_tunnel_interface(self, msg=False, **kwargs):
        '''
        params example:
        opt = {
            'name': 'gre_t1',
            'ip_addr': '1.1.1.1',
            'bound_to_if': 'X2',
            'remote_ipv6_addr': '2012::169',
            'local': {'dynamic': True}
        }
        the keys <name>, <ip_addr>, <bound_to_if>, <remote_ipv6_addr>, <local> are must
        '''
        url = self.url_tunnel_4to6
        input_json = self.build_gre4to6_interface_json(**kwargs)
        return self.fw.api_post(url, msg, data=input_json)

    def build_gre4to6_interface_json(self, **kwargs):
        '''
        params example:
        opt = {
            'name': 'gre_t1',
            'ip_addr': '1.1.1.1',
            'bound_to_if': 'X2',
            'remote_ipv6_addr': '2012::169',
            'local': {'dynamic': True}
        }
        the keys <name>, <ip_addr>, <bound_to_if>, <remote_ipv6_addr>, <local> are must
        '''
        input_json = copy.deepcopy(self.initial_4to6_json)
        init_type_part = {
            'gre4to6': {
                'bound_to': {'interface': ''},
                'ip': '',
                'local': {},
                'netmask': '255.255.255.0',
                'remote': {'ipv6': ""}
            }
        }
        try:
            input_json['tunnel_interfaces'][0]['4to6'].update(kwargs)
            input_json['tunnel_interfaces'][0]['4to6']['type'] = init_type_part
            input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['ip'] = kwargs['ip_addr']
            if 'netmask' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['netmask'] = kwargs['netmask']
            input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['bound_to']['interface'] = kwargs[
                'bound_to_if'].upper()
            input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['remote']['ipv6'] = kwargs['remote_ipv6_addr']
            input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['local'] = kwargs['local']
        except Exception as e:
            logger.error(repr(e))
        return input_json

    def edit_gre4to6_tunnel_interface_by_name(self, msg=False, tunnel_name=None, **kwargs):
        '''
        params example:
        opt = {
            'comment': "edit gre4to6 tunnel interface"
        }
        any key in self.initial_4to6_json["tunnel_interfaces"][0]['4to6'] is OK
        any key in input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6'] is OK
        '''
        url = self.url_tunnel_4to6 + '/name/' + tunnel_name
        input_json = self.get_tunnel_interface_status(name=tunnel_name, type='4to6')
        try:
            input_json['tunnel_interfaces'][0]['4to6'].update(kwargs)
            if 'ip_addr' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['ip'] = kwargs['ip_addr']
            if 'netmask' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['netmask'] = kwargs['netmask']
            if 'bound_to_if' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['bound_to']['interface'] = kwargs[
                    'bound_to_if'].upper()
            if 'remote_ipv6_addr' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['remote']['ipv6'] = kwargs[
                    'remote_ipv6_addr']
            if 'local' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']['gre4to6']['local'] = kwargs['local']
        except Exception as e:
            logger.error(repr(e))
        return self.fw.api_put(url, msg, data=input_json)

    def delete_gre4to6_tunnel_interface_by_name(self, name=None, msg=False):
        url = self.url_tunnel_4to6 + '/name/' + name
        return self.fw.api_delete(url, msg)

    def add_dslite_tunnel_interface(self, msg=False, **kwargs):
        '''
        params example:
        opt = {
            "name": "ds-lite_t1",
            "bound_to_if": "X1",
            "local": {"dynamic": True},
            "remote": {"dynamic": True},
            "comment":"ds-lite tunnel interface"
        }
        '''
        input_json = copy.deepcopy(self.initial_4to6_json)
        init_type_part = {
            "dslite": {
                "bound_to": {"interface": ""},
                "local": {},
                "remote": {},
                "local_ipv4": "192.0.0.2"
            }
        }
        try:
            input_json['tunnel_interfaces'][0]['4to6']["name"] = kwargs["name"]
            if "flow_reporting" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["flow_reporting"] = kwargs["flow_reporting"]
            if "fragment_packets" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["fragment_packets"] = kwargs["fragment_packets"]
            if "ignore_df_bit" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["ignore_df_bit"] = kwargs["ignore_df_bit"]
            if "send_icmp_fragmentation" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["send_icmp_fragmentation"] = kwargs[
                    "send_icmp_fragmentation"]
            if "comment" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["comment"] = kwargs["comment"]
            input_json['tunnel_interfaces'][0]['4to6']['type'] = init_type_part
            input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['bound_to']['interface'] = kwargs[
                'bound_to_if'].upper()
            input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['local'] = kwargs['local']
            input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['remote'] = kwargs['remote']
            if 'local_ipv4' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]["local_ipv4"] = kwargs['local_ipv4']
        except Exception as e:
            logger.error(repr(e))
        return self.fw.api_post(self.url_tunnel_4to6, msg, data=input_json)

    def edit_dslite_tunnel_interface_by_name(self, tunnel_name, msg=False, **kwargs):
        '''
        params example:
        opt = {
            'comment': "edit dslite tunnel interface"
        }
        any key in self.initial_4to6_json["tunnel_interfaces"][0]['4to6'] is OK
        any key in input_json['tunnel_interfaces'][0]['4to6']['type']['dslite'] is OK
        '''
        url = self.url_tunnel_4to6 + '/name/' + tunnel_name
        input_json = self.get_tunnel_interface_status(name=tunnel_name, type='4to6')
        try:
            # input_json['tunnel_interfaces'][0]['4to6'].update(kwargs)
            if "name" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["name"] = kwargs["name"]
            if "flow_reporting" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["flow_reporting"] = kwargs["flow_reporting"]
            if "fragment_packets" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["fragment_packets"] = kwargs["fragment_packets"]
            if "ignore_df_bit" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["ignore_df_bit"] = kwargs["ignore_df_bit"]
            if "send_icmp_fragmentation" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["send_icmp_fragmentation"] = kwargs[
                    "send_icmp_fragmentation"]
            if "comment" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']["comment"] = kwargs["comment"]
            if "bound_to_if" in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['bound_to']['interface'] = kwargs[
                    "bound_to_if"].upper()
            if 'local' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['local'] = kwargs['local']
            if 'remote' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]['remote'] = kwargs['remote']
            if 'local_ipv4' in kwargs:
                input_json['tunnel_interfaces'][0]['4to6']['type']["dslite"]["local_ipv4"] = kwargs['local_ipv4']
        except Exception as e:
            logger.error(repr(e))
        return self.fw.api_put(url, msg, data=input_json)

    def build_json_wan(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_ipv4_wan_json)
            # Genaral tab
            print(kwargs['mode'])
            if kwargs['mode'] == 'static':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wan_static(**kwargs)
            elif kwargs['mode'] == 'dhcp':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wan_dhcp(**kwargs)
            elif kwargs['mode'] == 'pppoe':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wan_pppoe(**kwargs)
            elif kwargs['mode'] == 'pptp':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wan_pptp(**kwargs)
            elif kwargs['mode'] == 'l2tp':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wan_l2tp(**kwargs)
            elif kwargs['mode'] == 'transparent':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_transmode(**kwargs)
                del json_input['interfaces'][0]['ipv4']['routed_mode']
            elif kwargs['mode'] == 'wire-mode':
                wiremode_json_input = copy.deepcopy(self.initial_ipv4_safemode_json)
                wiremode_json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
                wiremode_json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wiremode(
                    **kwargs)
                return wiremode_json_input
            elif kwargs['mode'] == 'tap-mode':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_tapmode(**kwargs)
            else:
                logger.error(
                    'Make sure wan mode {} is one of: static, pptp, l2tp, wire-mode, tap-mode, pppoe, dhcp.'.format(
                        kwargs['mode']))
                return False
            json_input['interfaces'][0]['ipv4']['name'] = kwargs['if']
            json_input['interfaces'][0]['ipv4']['comment'] = kwargs['comment']
            json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
            json_input['interfaces'][0]['ipv4']['management'] = self._get_interface_management(**kwargs)
            json_input['interfaces'][0]['ipv4']['user_login'] = self._get_interface_user(**kwargs)
            if (not kwargs['user_http'] and kwargs['user_https']) or (
                    'mgmt_http' in kwargs.keys() and not kwargs['mgmt_http'] and kwargs['mgmt_https']):
                if 'https_redirect' in kwargs:
                    json_input['interfaces'][0]['ipv4']['https_redirect'] = kwargs['https_redirect']
            if 'link_speed' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['link_speed'] = {}
                if kwargs['link_speed'] == 'auto':
                    json_input['interfaces'][0]['ipv4']['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(\d+)_(full|half)', kwargs['link_speed'], re.I)
                    json_input['interfaces'][0]['ipv4']['link_speed'][m.group(2)] = m.group(1)
                else:
                    logger('Error: link_speed invalid!')
            if not kwargs['mac_override']:
                json_input['interfaces'][0]['ipv4']['mac']['default'] = True
            else:
                json_input['interfaces'][0]['ipv4']['mac']['override'] = kwargs['mac_override']
            if 'shutdown_port' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['shutdown_port'] = kwargs['shutdown_port']
            json_input['interfaces'][0]['ipv4']['flow_reporting'] = kwargs['flow_reporting']
            json_input['interfaces'][0]['ipv4']['multicast'] = kwargs['multicast']
            json_input['interfaces'][0]['ipv4']['cos_8021p'] = kwargs['cos_8021p']
            json_input['interfaces'][0]['ipv4']['exclude_route'] = kwargs['exclude_route']
            json_input['interfaces'][0]['ipv4']['asymmetric_route'] = kwargs['asymmetric_route']
            # json_input['interfaces'][0]['ipv4']['management_traffic_only'] = kwargs['management_traffic_only']
            if 'fragment_packets' in kwargs:
                json_input['interfaces'][0]['ipv4']['fragment_packets'] = kwargs['fragment_packets']
            if 'mtu' in kwargs:
                json_input['interfaces'][0]['ipv4']['mtu'] = kwargs['mtu']
            if 'ignore_df_bit' in kwargs:
                json_input['interfaces'][0]['ipv4']['ignore_df_bit'] = kwargs['ignore_df_bit']
            try:
                if kwargs['send_icmp_fragmentation']:
                    json_input['interfaces'][0]['ipv4']['send_icmp_fragmentation'] = kwargs['send_icmp_fragmentation']
            except:
                pass
            if kwargs['bandwidth_management']:
                if kwargs['ibwm'] and kwargs['ibwm_amount']:
                    json_input['interfaces'][0]['ipv4']['bandwidth_management']['ingress'] = kwargs['ibwm_amount']
                if kwargs['ebwm'] and kwargs['ebwm_amount']:
                    json_input['interfaces'][0]['ipv4']['bandwidth_management']['egress'] = kwargs['ebwm_amount']
        except KeyError as e:
            logger.info("Error: In creating JSON for interface wan: {}".format(e))
        logger.info("interface wan json obtained")
        return json_input

    def build_json_mgmt(self, **kwargs):
        json_input = {}

        try:
            json_input = copy.deepcopy(self.initial_ipv4_mgmt_json)
            # Genaral tab
            json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
            json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_static(**kwargs)
            json_input['interfaces'][0]['ipv4']['name'] = kwargs['if']
            json_input['interfaces'][0]['ipv4']['comment'] = kwargs['comment']
            json_input['interfaces'][0]['ipv4']['management'] = self._get_interface_management(**kwargs)
            json_input['interfaces'][0]['ipv4']['user_login'] = self._get_interface_user(**kwargs)
            if (not kwargs['user_http'] and kwargs['user_https']) or (
                    'mgmt_http' in kwargs.keys() and not kwargs['mgmt_http'] and kwargs['mgmt_https']):
                if 'https_redirect' in kwargs:
                    json_input['interfaces'][0]['ipv4']['https_redirect'] = kwargs['https_redirect']
            if 'shutdown_port' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['shutdown_port'] = kwargs['shutdown_port']
            json_input['interfaces'][0]['ipv4']['flow_reporting'] = kwargs['flow_reporting']
            if 'mtu' in kwargs:
                json_input['interfaces'][0]['ipv4']['mtu'] = kwargs['mtu']
            # if 'dns_proxy' in kwargs.keys():
            #     dict = {'dns_proxy': False,}
            #     json_input['interfaces'][0]['ipv4'].update(dict)
            #     json_input['interfaces'][0]['ipv4']['dns_proxy'] = kwargs['dns_proxy']
            if 'link_speed' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['link_speed'] = {}
                if kwargs['link_speed'] == 'auto':
                    json_input['interfaces'][0]['ipv4']['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(\d+)_(full|half)', kwargs['link_speed'], re.I)
                    json_input['interfaces'][0]['ipv4']['link_speed'][m.group(2)] = m.group(1)
                else:
                    logger('Error: link_speed invalid!')
            if kwargs['bandwidth_management']:
                json_input['interfaces'][0]['ipv4']['bandwidth_management'] = {'ingress': {}, 'egress': {}}
                if kwargs['ibwm'] and kwargs['ibwm_amount']:
                    json_input['interfaces'][0]['ipv4']['bandwidth_management']['ingress'] = kwargs['ibwm_amount']
                if kwargs['ebwm'] and kwargs['ebw_amount']:
                    json_input['interfaces'][0]['ipv4']['bandwidth_management']['egress'] = kwargs['ebwm_amount']
        except Exception as e:
            logger.error("Error: In creating JSON for interface MGMT {}".format(e))
        logger.info("interface MGMT json obtained")
        return json_input

    def build_json_lan(self, **kwargs):
        json_input = {}

        try:
            json_input = copy.deepcopy(self.initial_ipv4_lan_json)
            # Genaral tab
            json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
            if kwargs['mode'] == 'static':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_static(**kwargs)
            elif kwargs['mode'] == 'unnumbered':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_unnumber(
                    **kwargs)
            elif kwargs['mode'] == 'l2bridge':
                json_input = copy.deepcopy(self.initial_ipv4_l2bridge_json)
                json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_l2bridge(
                    **kwargs)
            elif kwargs['mode'] == 'wire-mode':
                wiremode_json_input = copy.deepcopy(self.initial_ipv4_safemode_json)
                wiremode_json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
                wiremode_json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_wiremode(
                    **kwargs)
                return wiremode_json_input
            elif kwargs['mode'] == 'tap-mode':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_tapmode(**kwargs)
            elif kwargs['mode'] == 'nativebridge':
                json_input['interfaces'][0]['ipv4']['ip_assignment'] = {}
                json_input['interfaces'][0]['ipv4']['native_bridge'] = self._get_interface_lan_native(**kwargs)
                json_input['interfaces'][0]['ipv4']['firewalling'] = kwargs['firewalling']
            elif kwargs['mode'] == 'portshield':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_portshield(
                    **kwargs)
                json_input['interfaces'][0]['ipv4'].pop('management')
                json_input['interfaces'][0]['ipv4'].pop('user_login')
            elif kwargs['mode'] == 'transparent':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_transmode(**kwargs)
                del json_input['interfaces'][0]['ipv4']['routed_mode']
            else:
                logger.error(
                    'Make sure lan mode {} is one of: static, transparent, l2bridge, wire-mode, tap-mode, unnumbered, portshield, nativebridge.'.format(
                        kwargs['mode']))
                return False
            json_input['interfaces'][0]['ipv4']['name'] = kwargs['if']
            json_input['interfaces'][0]['ipv4']['comment'] = kwargs['comment']
            if kwargs['mode'] != 'portshield':
                json_input['interfaces'][0]['ipv4']['management'] = self._get_interface_management(**kwargs)
                json_input['interfaces'][0]['ipv4']['user_login'] = self._get_interface_user(**kwargs)
                if (not kwargs['user_http'] and kwargs['user_https']) or (
                        'mgmt_http' in kwargs.keys() and not kwargs['mgmt_http'] and kwargs['mgmt_https']):
                    if 'https_redirect' in kwargs:
                        json_input['interfaces'][0]['ipv4']['https_redirect'] = kwargs['https_redirect']
            if not kwargs['mac_override']:
                json_input['interfaces'][0]['ipv4']['mac']['default'] = True
            else:
                json_input['interfaces'][0]['ipv4']['mac']['override'] = kwargs['mac_override']
            if 'shutdown_port' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['shutdown_port'] = kwargs['shutdown_port']
            if 'dns_proxy' in kwargs.keys():
                dict = {'dns_proxy': False, }
                json_input['interfaces'][0]['ipv4'].update(dict)
                json_input['interfaces'][0]['ipv4']['dns_proxy'] = kwargs['dns_proxy']
            if 'link_speed' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['link_speed'] = {}
                if kwargs['link_speed'] == 'auto':
                    json_input['interfaces'][0]['ipv4']['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(\d+)_(full|half)', kwargs['link_speed'], re.I)
                    json_input['interfaces'][0]['ipv4']['link_speed'][m.group(2)] = m.group(1)
                else:
                    logger('Error: link_speed invalid!')
            if 'multicast' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['multicast'] = kwargs['multicast']
            if 'mtu' in kwargs:
                json_input['interfaces'][0]['ipv4']['mtu'] = kwargs['mtu']
            if 'routed_mode' in kwargs:
                json_input['interfaces'][0]['ipv4']['routed_mode'] = kwargs['routed_mode']
            if 'asymmetric_route' in kwargs:
                json_input['interfaces'][0]['ipv4']['asymmetric_route'] = kwargs['asymmetric_route']
            if kwargs['mode'] != 'tap-mode' or kwargs['mode'] != 'wire-mode':
                # interface source only support policy mode in LAN Zone.
                getmgmtsource = self._get_interface_source(**kwargs)
                logger.info(f'get mgmt source result: {getmgmtsource}')
                if getmgmtsource:
                    json_input['interfaces'][0]['ipv4']['management'].update(getmgmtsource)

            # if 'vlan' in kwargs:
            #     json_input['interfaces'][0]['ipv4']['vlan'] = kwargs['vlan']
        except Exception as e:
            logger.error("Error: In creating JSON for interface lan {}".format(e))
        logger.info("interface lan json obtained")
        return json_input

    def build_json_wlan(self, **kwargs):
        json_input = {}

        try:
            json_input = copy.deepcopy(self.initial_ipv4_wlan_json)
            # Genaral tab
            json_input['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
            if kwargs['mode'] == 'static':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_static(**kwargs)
            elif kwargs['mode'] == 'l2bridge':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_l2bridge(
                    **kwargs)
            elif kwargs['mode'] == 'nativebridge':
                json_input['interfaces'][0]['ipv4']['ip_assignment'] = {}
                json_input['interfaces'][0]['ipv4']['native_bridge'] = self._get_interface_lan_native(**kwargs)
                json_input['interfaces'][0]['ipv4']['firewalling'] = kwargs['firewalling']
            elif kwargs['mode'] == 'portshield':
                json_input['interfaces'][0]['ipv4']['ip_assignment']['mode'] = self._get_interface_lan_portshield(
                    **kwargs)
            else:
                logger.error('Make sure wlan mode {} is one of: static, l2bridge, portshield, nativebridge.'.format(
                    kwargs['mode']))
                return False
            if 'mtu' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['mtu'] = kwargs['mtu']
            if 'multicast' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['multicast'] = kwargs['multicast']
            if kwargs['mode'] == 'static' or kwargs['mode'] == 'l2bridge':
                if kwargs['sp_limit']:
                    json_input['interfaces'][0]['ipv4']['sonicpoint']['limit']['value'] = kwargs['sp_limit']
                # json_input['interfaces'][0]['ipv4']['sonicpoint']['limit']['value'] = kwargs['sp_limit']
                # json_input['interfaces'][0]['ipv4']['sonicpoint']['reserve_address'] = {'dynamic': True}
                # if 'sp_reserve_address' in kwargs.keys():
                # json_input['interfaces'][0]['ipv4']['sonicpoint']['limit']['reserve_address'] = {'manual': None}
                # json_input['interfaces'][0]['ipv4']['sonicpoint']['limit']['reserve_address']['manual'] = kwargs['sp_reserve_address']
                json_input['interfaces'][0]['ipv4']['name'] = kwargs['if']
                logger.info(json_input['interfaces'][0]['ipv4']['name'])
                json_input['interfaces'][0]['ipv4']['comment'] = kwargs['comment']
                json_input['interfaces'][0]['ipv4']['management'] = self._get_interface_management(**kwargs)
                json_input['interfaces'][0]['ipv4']['user_login'] = self._get_interface_user(**kwargs)
            if (not kwargs['user_http'] and kwargs['user_https']) or (
                    'mgmt_http' in kwargs.keys() and not kwargs['mgmt_http'] and kwargs['mgmt_https']):
                if 'https_redirect' in kwargs:
                    json_input['interfaces'][0]['ipv4']['https_redirect'] = kwargs['https_redirect']
            ####w0 not need sonicpoint
            if kwargs['if'] == 'W0':
                del json_input['interfaces'][0]['ipv4']['sonicpoint']
            # advance tab
            if not kwargs['mac_override']:
                json_input['interfaces'][0]['ipv4']['mac']['default'] = True
            else:
                json_input['interfaces'][0]['ipv4']['mac']['override'] = kwargs['mac_override']
            if 'shutdown_port' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['shutdown_port'] = kwargs['shutdown_port']
            if 'dns_proxy' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['dns_proxy'] = kwargs['dns_proxy']
            if 'link_speed' in kwargs.keys():
                json_input['interfaces'][0]['ipv4']['link_speed'] = {}
                if kwargs['link_speed'] == 'auto':
                    json_input['interfaces'][0]['ipv4']['link_speed']['auto_negotiate'] = True
                elif 'full' in kwargs['link_speed'] or 'half' in kwargs['link_speed']:
                    m = re.match(r'(\d+)_(full|half)', kwargs['link_speed'], re.I)
                    json_input['interfaces'][0]['ipv4']['link_speed'][m.group(2)] = m.group(1)
                else:
                    logger('Error: link_speed invalid!')
        except KeyError as e:
            logger.error("Error: In creating JSON for interface wlan {}".format(e))
        logger.info("interface wlan json obtained")
        return json_input

    def build_json_unassign(self, interface, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_ipv4_unassign_json)
        json_input['interfaces'][0]['ipv4'].update(kwargs)
        json_input['interfaces'][0]['ipv4']['name'] = interface
        logger.info(json_input)
        return json_input

    def build_json_vlan_unassign(self, interface, vlan, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_ipv4_vlan_unassign_json)
        json_input['interfaces'][0]['ipv4'].update(kwargs)
        json_input['interfaces'][0]['ipv4']['name'] = interface
        json_input['interfaces'][0]['ipv4']['vlan'] = int(vlan)
        logger.info(json_input)
        return json_input

    def get_ipv4_interface(self):
        response = self.fw.api_get(self.url)
        return response

    def _get_interface_lan_static(self, **kwargs):
        static_json = {'static': {}}
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')
            return False
        else:
            static_json['static']['ip'] = kwargs['ip']
        if 'netmask' in kwargs.keys():
            static_json['static']['netmask'] = kwargs['netmask']
        else:
            static_json['static']['netmask'] = '255.255.255.0'

        if kwargs['zone'] != 'WLAN':
            if 'gateway' in kwargs.keys():
                static_json['static']['gateway'] = kwargs['gateway']
                if kwargs['zone'] == 'test3':
                    del static_json['static']['gateway']
                    logger.info('delete gateway ')

        logger.info('static_json:{}'.format(static_json))
        return static_json

    def _get_interface_lan_l2bridge(self, **kwargs):
        l2bridge_json = {'l2bridge': {}}
        if 'bridge_to' not in kwargs.keys():
            logger.error('Bridged interface should be specified when l2bridge mode.')
            return False
        else:
            l2bridge_json['l2bridge']['bridge_to'] = kwargs['bridge_to']
        l2bridge_json['l2bridge']['block_non_ip'] = kwargs['bridge_block_non_ip']
        l2bridge_json['l2bridge']['route_on_bridge_pair'] = kwargs['route_on_bridge_pair']
        # l2bridge_json['l2bridge']['only_sniff'] = kwargs['bridge_block_non_ip']
        l2bridge_json['l2bridge']['stateful_inspection'] = kwargs['stateful_inspection']
        l2bridge_json['l2bridge']['vlan_filtering_mode'] = kwargs['bridge_vlan_filter']
        if kwargs['bridge_vlan_list']:
            l2bridge_json['l2bridge']['filtered_vlan'] = []
            for vlan in kwargs['bridge_vlan_list']:
                l2bridge_json['l2bridge']['filtered_vlan'].append({
                    "filtered_vlan": int(vlan)
                })
        return l2bridge_json

    def _get_interface_lan_unnumber(self, **kwargs):
        unnumber_json = {'unnumbered': {}}
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')
            return False
        else:
            unnumber_json['unnumbered']['ip'] = kwargs['ip']
        if 'netmask' in kwargs.keys():
            unnumber_json['unnumbered']['netmask'] = kwargs['netmask']
        else:
            unnumber_json['unnumbered']['netmask'] = '255.255.255.0'
        if 'gateway' in kwargs.keys():
            unnumber_json['unnumbered']['gateway'] = kwargs['gateway']
        return unnumber_json

    def _get_interface_lan_portshield(self, **kwargs):
        portshield_json = {}
        try:
            portshield_json['portshield'] = kwargs['portshield_to']
        except Exception as e:
            logger.error('Error info: {}'.format(e))
        return portshield_json

    def _get_interface_lan_native(self, **kwargs):
        native_json = {}
        try:
            native_json['interface'] = kwargs['native_bridge_to']
        except Exception as e:
            logger.error('Error info: {}'.format(e))
        return native_json

    def _get_interface_transmode(self, **kwargs):
        wire_json = {}
        wire_json['transparent'] = {}
        # transparent mode options
        try:
            wire_json['transparent']['transparent_range'] = kwargs['transparent_range']
            wire_json['transparent']['gratuitous_arp_wan_forwarding'] = kwargs['gratuitous_arp_wan_forwarding']
            wire_json['transparent']['gratuitous_arp_wan_generation'] = kwargs['gratuitous_arp_wan_generation']
        except Exception as e:
            logger.error(repr(e))
        return wire_json

    def _get_interface_wiremode(self, **kwargs):
        wire_json = {}
        wire_json['wire_mode'] = {}
        # tap mode
        try:
            wire_json['wire_mode']['type'] = kwargs['type']
            wire_json['wire_mode']['paired_interface'] = {}
            wire_json['wire_mode']['paired_interface']['interface'] = kwargs['wire_paired_interface']
            wire_json['wire_mode']['paired_interface_zone'] = kwargs['wire_paired_zone']
            wire_json['wire_mode']['linkstate_propagation'] = kwargs['wire_link_propagation']
            if kwargs['type'] == 'inspect':
                wire_json['wire_mode']['restrict_analysis'] = kwargs['restrict_analysis']
            if kwargs['type'] == 'inspect' and kwargs['type'] == 'secure':
                wire_json['wire_mode']['stateful_inspection'] = kwargs['stateful_inspection']
        ####not get disable stateful inspection from postman
        # wire_json['wire_mode']['disable_stateful inspection'] = kwargs['wire_dis_inspection']
        except Exception as e:
            logger.error('Error info: {}'.format(e))
        return wire_json

    def _get_interface_tapmode(self, **kwargs):
        tap_json = {}
        tap_json['tap_mode'] = {}
        try:
            tap_json['tap_mode']['stateful_inspection'] = kwargs['stateful_inspection']
        except Exception as e:
            logger.error('Error info: {}'.format(e))
        return tap_json

    def _get_interface_wan_pptp(self, **kwargs):
        pptp_json = {'pptp': {}}
        pptp_json['pptp']['user_name'] = kwargs['pptp_user']
        pptp_json['pptp']['password'] = kwargs['pptp_passwd']
        pptp_json['pptp']['server'] = kwargs['pptp_server']
        pptp_json['pptp']['hostname'] = kwargs['pptp_hostname']
        pptp_json['pptp']['dynamic'] = kwargs['pptp_dynamic']
        pptp_json['pptp']['inactivity'] = kwargs['pptp_inactivity']
        pptp_json['pptp']['schedule'] = {}
        if kwargs['pptp_schedule'].lower() == 'always_on':
            pptp_json['pptp']['schedule']['always_on'] = True
        else:
            match = re.search(r'(.*) (\d*:\d*) to (\d*:\d*)', kwargs['pptp_schedule'])
            if match:
                pptp_json['pptp']['schedule']['days'] = {}
                pptp_json['pptp']['schedule']['days']['days'] = match.group(1)
                pptp_json['pptp']['schedule']['days']['time'] = {}
                pptp_json['pptp']['schedule']['days']['time']['begin'] = match.group(2)
                pptp_json['pptp']['schedule']['days']['time']['end'] = match.group(3)
            else:
                pptp_json['pptp']['schedule']['name'] = kwargs['pptp_schedule']
        if 'pptp_ip' in kwargs.keys() and re.search(r'\d+.\d+.\d+.\d+', kwargs['pptp_ip']):
            pptp_json['pptp']['dynamic'] = False
            pptp_json['pptp']['ip'] = kwargs['pptp_ip']
            pptp_json['pptp']['netmask'] = kwargs['pptp_netmask']
            pptp_json['pptp']['gateway'] = kwargs['pptp_gateway']
        else:
            pptp_json['pptp']['dynamic'] = True
        return pptp_json

    def _get_interface_wan_l2tp(self, **kwargs):
        l2tp_json = {'l2tp': {}}
        l2tp_json['l2tp']['user_name'] = kwargs['l2tp_user']
        l2tp_json['l2tp']['password'] = kwargs['l2tp_passwd']
        l2tp_json['l2tp']['server'] = kwargs['l2tp_server']
        l2tp_json['l2tp']['hostname'] = kwargs['l2tp_hostname']
        l2tp_json['l2tp']['dynamic'] = kwargs['l2tp_dynamic']
        l2tp_json['l2tp']['inactivity'] = kwargs['l2tp_inactivity']
        l2tp_json['l2tp']['schedule'] = {}
        if kwargs['l2tp_schedule'].lower() == 'always_on':
            l2tp_json['l2tp']['schedule']['always_on'] = True
        else:
            match = re.search(r'(.*) (\d*:\d*) to (\d*:\d*)', kwargs['l2tp_schedule'])
            if match:
                l2tp_json['l2tp']['schedule']['days'] = {}
                l2tp_json['l2tp']['schedule']['days']['days'] = match.group(1)
                l2tp_json['l2tp']['schedule']['days']['time'] = {}
                l2tp_json['l2tp']['schedule']['days']['time']['begin'] = match.group(2)
                l2tp_json['l2tp']['schedule']['days']['time']['end'] = match.group(3)
            else:
                l2tp_json['l2tp']['schedule']['name'] = kwargs['l2tp_schedule']
        if 'l2tp_ip' in kwargs.keys() and re.search(r'\d+.\d+.\d+.\d+', kwargs['l2tp_ip']):
            l2tp_json['l2tp']['dynamic'] = False
            l2tp_json['l2tp']['ip'] = kwargs['l2tp_ip']
            l2tp_json['l2tp']['netmask'] = kwargs['l2tp_netmask']
            l2tp_json['l2tp']['gateway'] = kwargs['l2tp_gateway']
        else:
            l2tp_json['l2tp']['dynamic'] = True
        return l2tp_json

    def _get_interface_wan_pppoe(self, **kwargs):
        # 'pppoe_user': 'abc', 'pppoe_passwd': 'password', 'pppoe_service': '', 'pppoe_schedule': 'always_on', 'pppoe_dynamic': True, 'pppoe_inactivity': 10, 'pppoe_lcp_echo_packets': True, 'pppoe_reconnect': False
        pppoe_json = {'pppoe': {}}
        pppoe_json['pppoe']['user_name'] = kwargs['pppoe_user']
        pppoe_json['pppoe']['password'] = kwargs['pppoe_passwd']
        pppoe_json['pppoe']['service_name'] = kwargs['pppoe_service']
        pppoe_json['pppoe']['dynamic'] = kwargs['pppoe_dynamic']
        pppoe_json['pppoe']['inactivity'] = kwargs['pppoe_inactivity']
        pppoe_json['pppoe']['lcp_echo_packets'] = kwargs['pppoe_lcp_echo_packets']
        pppoe_json['pppoe']['reconnect'] = kwargs['pppoe_reconnect']
        if 'ncp_neg_retrans' in kwargs.keys():
            pppoe_json['pppoe']['ncp_neg_retrans'] = kwargs['ncp_neg_retrans']
        pppoe_json['pppoe']['schedule'] = {}
        if kwargs['pppoe_schedule'].lower() == 'always_on':
            pppoe_json['pppoe']['schedule']['always_on'] = True
        else:
            match = re.search(r'(.*) (\d*:\d*) to (\d*:\d*)', kwargs['pppoe_schedule'])
            if match:
                pppoe_json['pppoe']['schedule']['days'] = {}
                pppoe_json['pppoe']['schedule']['days']['days'] = match.group(1)
                pppoe_json['pppoe']['schedule']['days']['time'] = {}
                pppoe_json['pppoe']['schedule']['days']['time']['begin'] = match.group(2)
                pppoe_json['pppoe']['schedule']['days']['time']['end'] = match.group(3)
            else:
                pppoe_json['pppoe']['schedule']['name'] = kwargs['pppoe_schedule']
        if 'pppoe_ip' in kwargs.keys() and re.search(r'\d+.\d+.\d+.\d+', kwargs['pppoe_ip']):
            pppoe_json['pppoe']['dynamic'] = False
            pppoe_json['pppoe']['ip'] = kwargs['pppoe_ip']
        elif 'pppoe_unnumbered' in kwargs.keys():
            pppoe_json['pppoe']['dynamic'] = False
            pppoe_json['pppoe']['unnumbered'] = kwargs['pppoe_unnumbered']
        else:
            pppoe_json['pppoe']['dynamic'] = True
        print(pppoe_json)
        return pppoe_json

    def _get_interface_wan_static(self, **kwargs):
        static_json = {'static': {}}
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')
            return False
        else:
            static_json['static']['ip'] = kwargs['ip']
        if 'netmask' in kwargs.keys():
            static_json['static']['netmask'] = kwargs['netmask']
        else:
            static_json['static']['netmask'] = '255.255.255.0'
        if 'gateway' in kwargs.keys():
            static_json['static']['gateway'] = kwargs['gateway']
        static_json['static']['dns'] = {}
        static_json['static']['dns']['primary'] = kwargs['dns1']
        static_json['static']['dns']['secondary'] = kwargs['dns2']
        static_json['static']['dns']['tertiary'] = kwargs['dns3']

        return static_json

    def _get_interface_wan_dhcp(self, **kwargs):
        dhcp_json = {'dhcp': {}}
        dhcp_json['dhcp']['hostname'] = kwargs['dhcp_hostname']
        dhcp_json['dhcp']['renew_on_startup'] = kwargs['dhcp_renew_on_startup']
        if 'type' not in kwargs or kwargs['type'] != 'vlan':
            dhcp_json['dhcp']['renew_on_link_up'] = kwargs['dhcp_renew_on_link_up']
        dhcp_json['dhcp']['initiate_renewals_with_discover'] = kwargs['dhcp_initiate_renewals_with_discover']
        dhcp_json['dhcp']['force_discover_interval'] = kwargs['dhcp_force_discover_interval']
        return dhcp_json

    def _get_interface_management(self, **kwargs):
        mgmt_json = {}
        mgmt_json['https'] = kwargs['mgmt_https']
        mgmt_json['ping'] = kwargs['mgmt_ping']
        mgmt_json['ssh'] = kwargs['mgmt_ssh']
        mgmt_json['snmp'] = kwargs['mgmt_snmp']
        if 'mgmt_http' in kwargs.keys():
            mgmt_json['http'] = kwargs['mgmt_http']
        if 'fqdn_assignment' in kwargs.keys():
            mgmt_json['fqdn_assignment'] = kwargs['fqdn_assignment']
        return mgmt_json

    def _get_interface_source(self, **kwargs):
        source_json = {}
        # only support policy mode
        if 'https_source' in kwargs.keys():
            source_json['https_source'] = kwargs['https_source']
        if 'ssh_source' in kwargs.keys():
            source_json['ssh_source'] = kwargs['ssh_source']
        if 'ping_source' in kwargs.keys():
            source_json['ping_source'] = kwargs['ping_source']
        if 'snmp_source' in kwargs.keys():
            source_json['snmp_source'] = kwargs['snmp_source']
        return source_json

    def _get_interface_user(self, **kwargs):
        user_json = {}
        user_json['https'] = kwargs['user_https']
        user_json['http'] = kwargs['user_http']
        return user_json

    def _get_redundancy_aggregation_ports(self, **kwargs):
        ports_json = {'port': {}}
        if 'redundancy_aggregation_port' in kwargs.keys():
            try:
                if kwargs['redundancy_aggregation_port'] == 'redundancy':
                    ports_json['port']['redundancy'] = {}
                    ports_json['port']['redundancy']['interface'] = kwargs['redundancy_port']
                elif kwargs['redundancy_aggregation_port'] == 'aggregation':
                    ports_json['port']['aggregation'] = {}
                    ports_json['port']['aggregation']['aggregate'] = []
                    for index, port in enumerate(kwargs['aggregation_ports']):
                        ports_json['port']['aggregation']['aggregate'].append({'aggno': index + 1, 'interface': port})
                else:
                    ports_json['port']['redundancy_aggregation'] = False
            except Exception as e:
                logger.error('Error info: {}'.format(e))
        return ports_json

    def add_interface(self, msg=False, **kwargs):
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of vlan, 4to6, wlan-tunnel, vpn_tunnel when add an interface.')
            return False
        if kwargs['type'] == 'vlan' and 'if' not in kwargs.keys():
            logger.error('Please specify if name.')
            return False
        self.options = dict(InterfaceIPv4Api.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        kwargs['if'].upper()
        if kwargs['if'] == 'X0':
            kwargs['zone'] = 'LAN'
        if kwargs['if'] == 'X1':
            kwargs['zone'] = 'WAN'
        if kwargs['if'] == 'W0':
            kwargs['zone'] = 'WLAN'
        if kwargs['zone'].upper() in ['LAN', 'WAN', 'WLAN', 'SSLVPN', 'VPN', 'MULTICAST', 'DMZ']:
            kwargs['zone'] = kwargs['zone'].upper()
        if kwargs['zone'] == 'WAN':
            json_input = self.build_json_wan(**kwargs)
        elif kwargs['zone'] == 'LAN' or kwargs['zone'] == 'DMZ':
            json_input = self.build_json_lan(**kwargs)
        elif kwargs['zone'] == 'WLAN':
            json_input = self.build_json_wlan(**kwargs)
        elif kwargs['zone'] == 'VPN':
            kwargs['type'] = 'vpn_tunnel'
        else:
            json_input = self.build_json_lan(**kwargs)

        if kwargs['mode'] == 'nativebridge':
            json_input['interfaces'][0]['ipv4'].pop('comment')
            json_input['interfaces'][0]['ipv4'].pop("management")
            json_input['interfaces'][0]['ipv4'].pop("user_login")
            json_input['interfaces'][0]['ipv4'].pop("multicast")
            json_input['interfaces'][0]['ipv4'].pop("routed_mode")

        if kwargs['type'] == 'vlan':
            url = self.url
            json_input['interfaces'][0]['ipv4']['vlan'] = kwargs['vlan_tag']
            #    json_input['interfaces'][0]['ipv4'].pop('link_speed')
            json_input['interfaces'][0]['ipv4'].pop('cos_8021p')
        #    json_input['interfaces'][0]['ipv4'].pop('shutdown_port')
        elif kwargs['type'] == 'vpn_tunnel':
            url = self.url_tunnel_vpn
            json_input = self.build_json_vpntunnel(**kwargs)
        elif kwargs['type'] == '4to6':
            url = self.url_tunnel_4to6
            json_input = self._get_interface_4to6(**kwargs)
        elif kwargs['type'] == 'wlan-tunnel':
            json_input = self._get_interface_wti(**kwargs)
            url = self.url
        else:
            logger.error('{} is not one of vlan, vpn_tunnel, wlan-tunnel, 4to6.'.format(kwargs['type']))

        interface_resp = self.fw.api_post(url, msg, data=json_input)
        return interface_resp

    def edit_interface(self, interface_name, vlan_id, msg=False, **kwargs):
        if interface_name == '' or vlan_id == '':
            logger.error("fileds can't be empty ...")
            return False
        url = 'api/sonicos/interfaces/ipv4/name/' + str(interface_name) + '/vlan/' + str(vlan_id)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def build_json_vpntunnel(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_ipv4_vpn_tunnel_json)
            # Genaral tab
            if 'ip' not in kwargs.keys():
                logger.error('Interface ip should be specified when static mode.')
                return False
            else:
                json_input['tunnel_interfaces'][0]['vpn']['ip_assignment']['mode']['static']['ip'] = kwargs['ip']
            if 'netmask' in kwargs.keys():
                json_input['tunnel_interfaces'][0]['vpn']['ip_assignment']['mode']['static']['netmask'] = kwargs[
                    'netmask']
            else:
                json_input['tunnel_interfaces'][0]['vpn']['ip_assignment']['mode']['static'][
                    'netmask'] = '255.255.255.0'
            json_input['tunnel_interfaces'][0]['vpn']['name'] = kwargs['tunnel_name']
            json_input['tunnel_interfaces'][0]['vpn']['comment'] = kwargs['comment']
            json_input['tunnel_interfaces'][0]['vpn']['ip_assignment']['zone'] = 'VPN'
            json_input['tunnel_interfaces'][0]['vpn']['policy'] = kwargs['vpn_policy']
            json_input['tunnel_interfaces'][0]['vpn']['management'] = self._get_interface_management(**kwargs)
            json_input['tunnel_interfaces'][0]['vpn']['user_login'] = self._get_interface_user(**kwargs)
            json_input['tunnel_interfaces'][0]['vpn']['flow_reporting'] = kwargs['flow_reporting']
            json_input['tunnel_interfaces'][0]['vpn']['multicast'] = kwargs['multicast']
            json_input['tunnel_interfaces'][0]['vpn']['asymmetric_route'] = kwargs['asymmetric_route']
            # json_input['interfaces'][0]['ipv4']['management_traffic_only'] = kwargs['management_traffic_only']
            if 'fragment_packets' in kwargs:
                json_input['tunnel_interfaces'][0]['vpn']['fragment_packets'] = kwargs['fragment_packets']
            if 'ignore_df_bit' in kwargs:
                json_input['tunnel_interfaces'][0]['vpn']['ignore_df_bit'] = kwargs['ignore_df_bit']

            if kwargs['bandwidth_management']:
                if kwargs['ibwm'] and kwargs['ibwm_amount']:
                    json_input['tunnel_interfaces'][0]['vpn']['bandwidth_management']['ingress'] = kwargs['ibwm_amount']
                if kwargs['ebwm'] and kwargs['ebw_amount']:
                    json_input['tunnel_interfaces'][0]['vpn']['bandwidth_management']['egress'] = kwargs['ebwm_amount']
        except KeyError as e:
            logger.info("Error: In creating JSON for add vpn tunnel: {}".format(e))
        logger.info("interfaces vpn tunnel json obtained")
        return json_input

    def del_interface(self, msg=False, **kwargs):
        if kwargs['type'] == 'vlan':
            url = self.url + '/name/' + kwargs['if'].upper() + '/vlan/' + str(kwargs['vlan_tag'])
        elif kwargs['type'] == 'vpn_tunnel':
            url = self.url_tunnel_vpn + '/name/' + kwargs['tunnel_name']
            # json_input = self.build_json_vpntunnel(**kwargs)
        elif kwargs['type'] == '4to6':
            url = self.url_tunnel_4to6 + '/name/' + kwargs['tunnel_name']
        elif kwargs['type'] == 'wlan-tunnel':
            url = self.url + '/name/' + kwargs['tunnel-name'].upper()
        else:
            logger.error('{} is not one of vlan, vpn_tunnel, wlan-tunnel, 4to6.'.format(kwargs['type']))

        interface_resp = self.fw.api_delete(url, msg, data=None)
        return interface_resp

    def del_tunnel_interface_by_name(self, name: str, msg=False):
        url = self.url_tunnel_vpn + '/name/' + name
        if ' ' in name:
            logger.info('name should not contain space')
            return False
        if isinstance(name, str) and name:
            logger.info(f'del_tunnel_interface_by_name delete url: {url}')
            return self.fw.api_delete(url, msg)
        else:
            logger.info('the del name type/value invalid!')
            return False

    def _get_tunnel_interface_isatap(self, tag=True, **kwargs):
        pass

    def _get_interface_wti(self, **kwargs):
        wlan_json = copy.deepcopy(self.initial_wlan_tunnel_json)
        wlan_json['interfaces'][0]['ipv4']['tunnel'] = kwargs['tunnel-id']
        wlan_json['interfaces'][0]['ipv4']['name'] = kwargs['tunnel-if']
        wlan_json['interfaces'][0]['ipv4']['ip_assignment']['zone'] = kwargs['zone']
        wlan_json['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip'] = kwargs['ip']
        wlan_json['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['netmask'] = kwargs['netmask']
        wlan_json['interfaces'][0]['ipv4']['sonicpoint']['limit']['value'] = kwargs['sp-limit']
        return wlan_json

    def _get_interface_4to6(self, **kwargs):
        tunnel_json = copy.deepcopy(self.initial_4to6_json)
        tunnel_json['tunnel_interface']['4to6']['name'] = kwargs['tunnel_name']
        tunnel_json['tunnel_interface']['4to6']['comment'] = kwargs['comment']
        tunnel_json['tunnel_interface']['4to6']['flow_reporting'] = kwargs['flow_reporting']
        # json_input['interfaces'][0]['ipv4']['management_traffic_only'] = kwargs['management_traffic_only']
        if 'fragment_packets' in kwargs:
            tunnel_json['tunnel_interface']['4to6']['fragment_packets'] = kwargs['fragment_packets']
        if 'ignore_df_bit' in kwargs:
            tunnel_json['tunnel_interface']['4to6']['ignore_df_bit'] = kwargs['ignore_df_bit']
        tunnel_json['tunnel_interface']['4to6']['send_icmp_fragmentation'] = kwargs['send_icmp_fragmentation']
        tunnel_json['tunnel_interface']['4to6']['type'] = {}
        try:
            if 'tunnel_type' not in kwargs.keys():
                logger.error('Tunnel type should be specified when add a 4to6 tunnel.')
                return False
            else:
                tunnel_json['tunnel_interface']['4to6']['type'][kwargs['tunnel_type']] = {}
            if kwargs['tunnel_type'] == 'dslite':
                tunnel_json['tunnel_interface']['4to6']['type']['dslite']['local_ipv4'] = kwargs['local_ipv4']
                tunnel_json['tunnel_interface']['4to6']['type']['dslite']['bound_to'] = {}
                tunnel_json['tunnel_interface']['4to6']['type']['dslite']['bound_to']['interface'] = kwargs['bound_to']
                tunnel_json['tunnel_interface']['4to6']['type']['dslite']['local'] = {}
                if kwargs['local_ipv6'] == 'dynamic':
                    tunnel_json['tunnel_interface']['4to6']['type']['dslite']['local']['dynamic'] = True
                else:
                    tunnel_json['tunnel_interface']['4to6']['type']['dslite']['local']['ipv6'] = kwargs['local_ipv6']
                tunnel_json['tunnel_interface']['4to6']['type']['dslite']['remote'] = {}
                if kwargs['aftr_addr'] == 'dynamic':
                    tunnel_json['tunnel_interface']['4to6']['type']['dslite']['remote']['dynamic'] = True
                elif re.search(r'\.', kwargs['aftr_addr']):
                    tunnel_json['tunnel_interface']['4to6']['type']['dslite']['remote']['fqdn'] = kwargs['aftr_addr']
                else:
                    tunnel_json['tunnel_interface']['4to6']['type']['dslite']['local']['ipv6'] = kwargs['aftr_addr']
            elif kwargs['tunnel_type'] == 'gre4to6':
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['ip'] = kwargs['ip_ipv4']
                if 'netmask' in kwargs.keys():
                    tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['netmask'] = kwargs['netmask']
                else:
                    tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['netmask'] = '255.255.255.0'
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['bound_to'] = {}
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['bound_to']['interface'] = kwargs['bound_to']
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['local'] = {}
                if kwargs['local_ipv6'] == 'dynamic':
                    tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['local']['dynamic'] = True
                else:
                    tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['local']['ipv6'] = kwargs['local_ipv6']
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['remote'] = {}
                tunnel_json['tunnel_interface']['4to6']['type']['gre4to6']['remote']['ipv6'] = kwargs['aftr_addr']
            else:
                logger.error('Only dslite gre4to6 are supported.')
                return False
        except KeyError as e:
            logger.info("Error: In creating JSON for add 4to6 tunnel: {}".format(e))
        logger.info("interface vpn tunnel json obtained")
        return tunnel_json

    def unassign_interface(self, msg=False, interface=None, **kwargs):
        if interface.upper() == 'X0' or interface.upper() == 'X1':
            logger.error('Interface X0 or X1 cannot be unassigned')
            return False
        json_input = self.build_json_unassign(interface.upper(), **kwargs)
        interface_resp = self.fw.api_put(self.url, msg, data=json_input)
        return interface_resp

    def enforce_unassign_interface(self, msg=False, interface=None, **kwargs):
        if interface.upper() == 'X0':
            logger.error('Interface X0 cannot be unassigned')
            return False
        json_input = self.build_json_unassign(interface.upper(), **kwargs)
        interface_resp = self.fw.api_put(self.url, msg, data=json_input)
        return interface_resp

        # interface is X2,X3,X4...

    def unassign_interface_name(self, interface, msg=False, **kwargs):
        if interface.upper() == 'X0' or interface.upper() == 'X1':
            logger.error('Interface X0 or X1 cannot be unassigned')
            return False
        json_input = self.build_json_unassign(interface.upper(), **kwargs)
        interface_resp = self.fw.api_put(self.url + '/name/' + interface.upper(), msg, data=json_input)
        return interface_resp

    def unassign_vlan_interface(self, msg=False, interface=None, vlan_id=None, **kwargs):
        if interface.upper() == 'X0' or interface.upper() == 'X1':
            logger.error('Interface X0 or X1 cannot be unassigned')
            return False
        url = self.url + '/name/' + interface + '/vlan/' + vlan_id
        logger.info(url)
        json_input = self.build_json_vlan_unassign(interface.upper(), vlan=vlan_id, **kwargs)
        logger.info(json_input)
        interface_resp = self.fw.api_put(url, msg, data=json_input)
        return interface_resp

    def get_interface_status(self, name):
        url = self.url + '/name/' + name
        interface_resp = self.fw.api_get(url)
        return interface_resp

    #    def get_vlan_interface_status(self, name, vlan_id = None):
    #        url = self.url + '/name/' + name + '/vlan/' + vlan_id
    #        interface_resp = self.fw.api_get(url)
    #        return interface_resp

    def get_vlan_interface_status(self, name=None, vlan_id=''):
        url = self.url + '/name/' + name.upper() + '/vlan/' + vlan_id
        interface_resp = self.fw.api_get(url)
        return interface_resp

    def get_wlan_tunnel_interface_status(self, name=None, tunnel_id=''):  # add by cyuan
        url_tunnel_wlan = 'api/sonicos/interfaces/ipv4/name/' + name.upper() + '/tunnel/' + tunnel_id
        interface_resp = self.fw.api_get(url_tunnel_wlan)
        return interface_resp

    def get_tunnel_interface_status(self, name=None, type=None):
        if type == 'vpn':
            url = self.url_tunnel_vpn + '/name/' + name
        elif type == '4to6':
            url = self.url_tunnel_4to6 + '/name/' + name
        else:
            logger.error('type should be one of vpn or 4to6')
        interface_resp = self.fw.api_get(url)
        return interface_resp

    def click_dhcp_release(self, name, version='v4', msg=False):
        url_tmp = 'api/sonicos/release/'
        if version == 'v4':
            url_tmp = url_tmp + 'ipv4'
        else:
            url_tmp = url_tmp + 'ipv6'

        if name:
            url_tmp = url_tmp + '/name/' + name.upper()
        else:
            logger.error('interface name shoule be specified for click_dhcp_release.')
            return False
        logger.info(url_tmp)
        resp = self.fw.api_post(url_tmp, msg)
        logger.info(resp)
        return resp

    def click_dhcp_renew(self, name, version='v4', msg=False):
        url_tmp = 'api/sonicos/renew/'
        if version == 'v4':
            url_tmp = url_tmp + 'ipv4'
        else:
            url_tmp = url_tmp + 'ipv6'

        if name:
            url_tmp = url_tmp + '/name/' + name.upper()
        else:
            logger.error('interface name shoule be specified for click_dhcp_renew.')
            return False
        logger.info(url_tmp)
        resp = self.fw.api_post(url_tmp, msg)
        logger.info(resp)
        return resp

        # added by Celia

    def click_pppoe_disconnect(self, interface):
        if interface:
            url = 'api/sonicos/disconnect/' + interface.upper()
        else:
            logger.error('interface name shoule be specified for click_pppoe_disconnect.')
            return False
        resp = self.fw.api_post(url)
        logger.info(resp)
        return resp

    def click_pppoe_connect(self, interface):
        if interface:
            url = 'api/sonicos/connect/' + interface.upper()
        else:
            logger.error('interface name shoule be specified for click_pppoe_connect.')
            return False
        resp = self.fw.api_post(url)
        logger.info(resp)
        return resp

    def get_interface_address(self, name, version='v4'):
        url_tmp = 'api/sonicos/reporting/interfaces/'
        if version == 'v4':
            url_tmp = url_tmp + 'ipv4/ip'
        else:
            url_tmp = url_tmp + 'ipv6/ip'
        if name:
            if 'vlan' not in name:
                url_tmp = url_tmp + '/name/' + name.upper()
            else:
                url_tmp = url_tmp + '/name/' + name
        else:
            logger.error('interface name shoule be specified for get_interface_address.')
            return False
        logger.info(url_tmp)
        resp = self.fw.api_get(url_tmp)
        return resp

    def get_vlan_interface_address(self, name, vlan, version='v4'):
        url_tmp = 'api/sonicos/reporting/interfaces/'
        if version == 'v4':
            url_tmp = url_tmp + 'ipv4/ip'
        else:
            url_tmp = url_tmp + 'ipv6/ip'
        if name:
            url_tmp = url_tmp + '/name/' + name + '/vlan/' + vlan
        else:
            logger.error('interface name shoule be specified for get_interface_address.')
            return False
        logger.info(url_tmp)
        resp = self.fw.api_get(url_tmp)
        return resp

    def get_interface_mac(self, interface):
        mac_url = 'api/sonicos/reporting/interfaces/mac'
        mac_resp = self.fw.api_get(mac_url)
        try:
            for item in mac_resp:
                if item['name'].upper() == interface.upper():
                    return item['config_mac']
        except Exception:
            logger.error("can not find interface mac address")
            return None

    def disable_interface(self, name=None, msg=False):
        url = 'api/sonicos/interface/shutdown/' + name
        resp = self.fw.api_post(url, msg)
        logger.info(resp)
        return resp

    def enable_interface(self, name=None, msg=False):
        url = 'api/sonicos/interface/shutdown/' + name
        resp = self.fw.api_delete(url, msg)
        logger.info(resp)
        return resp

    def config_advance_part_for_unassign_interface(self, msg=False, **kwargs):
        '''
        this def used to config the advanced part for an unassgined interface
        key <name> is necessary!
        x2_advance_opt = {
            "name": "x2",
            "cos_8021p": True
        }
        '''
        if 'name' not in kwargs:
            logger.error(f'interface name muste be specify!!')
            return False
        url = self.url + '/name/' + kwargs['name'].lower()
        init_advance_part_json = {
            "name": "",
            "link_speed": {"auto_negotiate": True},
            "mac": {"default": True},
            "shutdown_port": False,
            "flow_reporting": True,
            "ip_assignment": {},
            "cos_8021p": False,
            "exclude_route": False,
            "management_traffic_only": False,
            "asymmetric_route": False,
            "flow_control": False,
            "port": {"redundancy_aggregation": False},
            "bandwidth_management": {"egress": {}, "ingress": {}},
            # "native_bridge":{}
        }
        init_advance_part_json.update(kwargs)
        json_input = {"interfaces": [{"ipv4": init_advance_part_json}]}
        return self.fw.api_put(url, msg=False, data=json_input)

    def get_interface_ip(self, interface):
        ip_url = 'api/sonicos/reporting/interfaces/ipv4/ip'
        interface_resp = self.fw.api_get(ip_url)
        try:
            for i in interface_resp:
                for key, value in i.items():
                    if value == interface:
                        return i['ip_address']
        except Exception:
            logger.error("can not find interface ip address")
            return None

    def config_default_wlan_interface(self, msg=False, **kwargs):
        url = self.url + '/name/W0'
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def get_interface_report_status(self):
        url = 'api/sonicos/reporting/interfaces/ipv4/status'
        interface_resp = self.fw.api_get(url)
        return interface_resp

    def get_interface_statistics(self):
        ip_url = 'api/sonicos/reporting/interfaces/ipv4/statistics'
        resp = self.fw.api_get(ip_url)
        return resp

    def get_interface_report(self):
        report_url = 'api/sonicos/reporting/interfaces/ipv4/ip'
        resp = self.fw.api_get(report_url)
        return resp

    # Added by Celia
    def enable_interfaces_display_all_traffic(self, msg=False):
        url = 'api/sonicos/interfaces/display-all-traffic'
        json_input = {"interface_statistics": {"display_all_traffic": True}}
        resp = self.fw.api_put(url, msg, data=json_input)
        logger.info(resp)
        return resp

    def disable_interfaces_display_all_traffic(self, msg=False):
        url = 'api/sonicos/interfaces/display-all-traffic'
        json_input = {"interface_statistics": {"display_all_traffic": False}}
        resp = self.fw.api_put(url, msg, data=json_input)
        logger.info(resp)
        return resp

    # add by cyuan
    def edit_vlan_interface(self, msg=False, **kwargs):
        resp = {}
        if 'name' in kwargs and 'vlan' in kwargs:
            url = self.url + '/name/' + kwargs['name'] + '/vlan/' + str(kwargs['vlan'])
            init_json = self.get_vlan_interface_status(name=kwargs['name'], vlan_id=str(kwargs['vlan']))
            json_input = copy.deepcopy(init_json)
            try:
                json_input['interfaces'][0]['ipv4'].update(kwargs)
            except Exception as e:
                logger.error(f'error: {e}')
            resp = self.fw.api_put(url, msg, data=json_input)
            return resp
        else:
            logger.error('interface name and vlan id must be specified')
            return (False, {}) if msg else False

    # add by xrli
    def clear_statistics(self):
        url = 'api/sonicos/reporting/interfaces/ipv4/statistics'
        resp = self.fw.api_delete(url)
        logger.info(resp)
        return resp


class ServiceObjectApi:
    '''ServiceObjectApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/service-objects'
        self.initial_group1 = {
            "service_objects": [{"name": None}]}

    def get_serviceobject(self):
        get_resp = self.fw.api_get(self.url)
        return get_resp

    def config_service_object(self, msg=False, **kwargs):
        json_input = self.build_json_serviceobject(kwargs)
        serviceobject_resp = self.fw.api_post(self.url, msg, data=json_input)
        get_resp = self.get_serviceobject()
        for i in get_resp["service_objects"]:
            if i["name"] == kwargs["name"]:
                uuid = i["uuid"]
                return serviceobject_resp, uuid
        return serviceobject_resp

    def build_json_serviceobject(self, service_object):
        json_input = {}
        object_type = service_object['object_type'].lower()
        try:
            json_input = copy.deepcopy(self.initial_group1)
            json_input["service_objects"][0]["name"] = service_object['name']
        except KeyError as e:
            logger.info("Error: In creating json for name object : {}".format(e))
        if object_type == "custom":
            try:
                logger.info("Custom service object Json obtained")
                logger.info(json_input)
                json_input["service_objects"][0]["custom"] = service_object['custom']
            except Exception as e:
                logger.info("Error: In creatng json for custom service object : {}".format(e))

        elif object_type == "icmp":
            try:
                logger.info("ICMP service object Json obtained")
                logger.info(json_input)
                json_input['service_objects'][0]['icmp'] = service_object['icmp']
            except KeyError:
                logger.error("Error: In creating JSON for ICMP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creating json for ICMP service object : {}".format(e))

        elif object_type == "igmp":
            try:
                logger.info("IGMP service object Json obtained")
                logger.info(json_input)
                json_input['service_objects'][0]['igmp'] = service_object['igmp']
            except KeyError:
                logger.info("Error: In creating JSON for IGMP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creating json for IGMP service object : {}".format(e))


        elif object_type == "tcp":
            try:
                if (service_object['tcp']['begin'] == "") or (service_object['tcp']['end'] == ""):
                    raise Exception("Port range is not mentioned")
                else:
                    logger.info("TCP service object Json obtained")
                    logger.info(json_input)
                    json_input['service_objects'][0]['tcp'] = service_object['tcp']
            except KeyError:
                logger.info("Error: In creating JSON for TCP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creating json for tcp service object : {}".format(e))

        elif object_type == "udp":
            try:
                if (service_object['udp']['begin'] == "") or (service_object['udp']['end'] == ""):
                    raise Exception("Port range is not mentioned")
                else:
                    logger.info("UDP service object Json obtained")
                    logger.info(json_input)
                    json_input['service_objects'][0]['udp'] = service_object['udp']
            except KeyError:
                logger.info("Error: In creating JSON for UDP Service Object")
                raise Exception
            except Exception as g:
                logger.info("Error: In creatng json for udp begin service object : {}".format(g))
            except Exception as e:
                logger.info("Error: In creatng json udp end for service object : {}".format(e))

        elif object_type == "6over4":
            try:
                if service_object['6over4'] != True:
                    raise Exception("6over4 is disabled")
                else:
                    logger.info("6over4 service object Json obtained")
                    logger.info(json_input)
                    json_input["service_objects"][0]["6over4"] = service_object['6over4']
            except KeyError:
                logger.info("Error: In creating JSON for 6over4 Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creating json for 6over4 service object : {}".format(e))

        elif object_type == "gre":
            try:
                if service_object['gre'] != True:
                    raise Exception("GRE is disabled")
                else:
                    logger.info("GRE service object Json obtained")
                    logger.info(json_input)
                    json_input["service_objects"][0]["gre"] = service_object['gre']
            except KeyError:
                logger.info("Error: In creating JSON for GRE Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creating json for GRE service object : {}".format(e))

        elif object_type == "esp":
            try:
                if service_object['esp'] != True:
                    raise Exception("ESP is disabled")
                else:
                    logger.info("ESP service object Json obtained")
                    logger.info(json_input)
                    json_input["service_objects"][0]["esp"] = service_object['esp']
            except KeyError:
                logger.info("Error: In creating JSON for ESP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for esp service object : {}".format(e))

        elif object_type == "ah":
            try:
                if service_object['ah'] != True:
                    raise Exception("AH is disabled")
                else:
                    logger.info("AH service object Json obtained")
                    logger.info(json_input)
                    json_input["service_objects"][0]["ah"] = service_object['ah']
            except KeyError:
                logger.info("Error: In creating JSON for AH Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for AH service object : {}".format(e))

        elif object_type == "eigrp":
            try:
                if service_object['eigrp'] != True:
                    raise Exception("EIGRP is disabled")
                else:
                    logger.info("EIGRP service object Json obtained")
                    loggerinfo(json_input)
                    json_input["service_objects"][0]["eigrp"] = service_object['eigrp']
            except KeyError:
                logger.info("Error: In creating JSON for EIGRP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for EIGRP service object : {}".format(e))

        elif object_type == "l2tp":
            try:
                if service_object['l2tp'] != True:
                    raise Exception("L2TP is disabled")
                else:
                    logger.info("L2TP service object Json obtained")
                    logger.info(json_input)
                    json_input["service_objects"][0]["l2tp"] = service_object['l2tp']
            except KeyError:
                logger.info("Error: In creating JSON for L2TP Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for l2tp service object : {}".format(e))

        elif object_type == "icmpv6":
            try:
                logger.info("ICMPV6 service object Json obtained")
                logger.info(json_input)
                json_input["service_objects"][0]["icmpv6"] = service_object['icmpv6']
            except KeyError:
                logger.info("Error: In creating JSON for ICMPV6 Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for ICMPV6 service object : {}".format(e))

        elif object_type == "ospf":
            try:
                logger.info("OSPF service object Json obtained")
                logger.info(json_input)
                json_input["service_objects"][0]["ospf"] = service_object['ospf']
            except KeyError:
                logger.info("Error: In creating JSON for OSPF Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for ospf service object : {}".format(e))

        elif object_type == "pim":
            try:
                logger.info("PIM service object Json obtained")
                logger.info(json_input)
                json_input["service_objects"][0]["pim"] = service_object['pim']
            except KeyError:
                logger.info("Error: In creating JSON for PIM Service Object")
                raise Exception
            except Exception as e:
                logger.info("Error: In creatng json for PIM service object : {}".format(e))

        else:
            json_input = {"Error": "Invalid service object type entered"}

        return json_input

    def edit_service_object(self, obj_path, obj_value, json_put, put_url=None, msg=False):
        put_url = put_url + '/' + obj_path + '/' + obj_value
        putservobj_resp = self.fw.api_put(put_url, msg, data=json_put)
        return putservobj_resp

    def delete_service_object(self, obj_path=None, obj_value=None, del_url=None):
        del_url = del_url + '/' + obj_path + '/' + obj_value
        serviceobject_resp = self.fw.api_delete(del_url)
        return serviceobject_resp

    def edit_service_obj_by_name(self, ser_name: str, msg=False, **kwargs):
        if not ser_name:
            logger.error('service object name must be specified')
            return False
        url = self.url + '/name/' + ser_name
        json_input = self.build_json_serviceobject(kwargs)
        logger.info(f'input json is:\n{json_input}')
        return self.fw.api_put(url, msg, data=json_input)


class ServiceGroupApi:
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/service-groups'
        self.initial_group_json = {
            "service_groups": [{"name": None,
                                "service_object": [
                                    {
                                        "name": None
                                    }
                                ],
                                "service_group": [
                                    {
                                        "name": None
                                    }

                                ]}]
        }

    def get_servicegroup(self):
        get_resp = self.fw.api_get(self.url)
        return get_resp

    # the standard api use the groups name
    def get_service_groups_via_name(self, name=''):
        if not name:
            logger.info('Please specify group name')
            return False
        get_resp = self.fw.api_get(self.url + '/name/' + name)
        return get_resp

    def get_servicegroup_by_name(self, name=None, version=None):
        if not name or not version:
            logger.info('Please specify ao name and version')
            return False
        name = name.replace(' ', '+')
        get_response = self.fw.api_get(self.url + f'{version}/name/{name}')
        return get_response

    def config_service_group(self, msg=False, **kwargs):
        json_input = self.build_json_servicegroup(kwargs)
        servicegroup_resp = self.fw.api_post(self.url, msg, data=json_input)
        get_resp = self.get_servicegroup()
        for i in get_resp["service_groups"]:
            if i["name"] == kwargs["name"]:
                uuid = i["uuid"]
                return servicegroup_resp, uuid
        return servicegroup_resp

    def build_json_servicegroup(self, service_group):
        json_input = {}
        so_list = []
        sg_list = []
        json_input = copy.deepcopy(self.initial_group_json)
        try:
            json_input["service_groups"][0]["name"] = service_group["name"]
            if 'service_object' in service_group.keys() and service_group['service_object']:
                for so_name in service_group["service_object"]:
                    so_list.append(so_name)
                json_input["service_groups"][0]["service_object"] = so_list
            else:
                del json_input["service_groups"][0]["service_object"]
            if 'service_group' in service_group.keys() and service_group['service_group']:
                for sg_name in service_group["service_group"]:
                    sg_list.append(sg_name)
                json_input["service_groups"][0]["service_group"] = sg_list
            else:
                del json_input["service_groups"][0]["service_group"]
        except KeyError as ke:
            logger.info(ke)
        return json_input

    def edit_service_group(self, obj_path, obj_value, json_put, put_url=None, msg=False):
        put_url = put_url + '/' + obj_path + '/' + obj_value
        putservgroup_resp = self.fw.api_put(put_url, msg, data=json_put)
        return putservgroup_resp

    def delete_service_group(self, obj_path=None, obj_value=None):
        del_url = self.url + '/' + obj_path + '/' + obj_value
        servicegroup_resp = self.fw.api_delete(del_url)
        return servicegroup_resp

    def delete_service_group_by_name(self, name, msg=False):
        del_url = self.url + '/name/' + name
        resp = self.fw.api_delete(del_url, msg)
        return resp

    def edit_service_group_by_name(self, name=None, msg=False, **kwargs):
        if not name:
            logger.info('Please specify service group name')
            return False
        url_edit = self.url + '/name/' + name
        logger.info(url_edit)
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(url_edit, msg, data=json_input)
        return resp


class AddressobjectsApi():

    def __init__(self, fw):
        self.fw = fw
        self.address_object_url = 'api/sonicos/address-objects/'
        self.base_url = 'api/sonicos/address-object/'
        self.ao_ipv4 = 'api/sonicos/address-objects/ipv4'
        self.ao_ipv6 = 'api/sonicos/address-objects/ipv6'

        self.initial_host_json = {
            "address_objects": [{"ipv4": {"name": None, "zone": None, "host": {"ip": None}}}]}
        self.initial_range_json = {
            "address_objects": [{"ipv4": {"name": None, "zone": None, "range": {"begin": None, "end": None}}}]}
        self.initial_network_json = {
            "address_objects": [{"ipv4": {"name": None, "zone": None, "network": {"subnet": None, "mask": None}}}]}
        self.initial_mac_json = {
            "address_objects": [{"mac": {"name": None, "zone": None, "address": None, "multi_homed": None}}]}
        self.initial_fqdn_json = {
            "address_objects": [{"fqdn": {"name": None, "zone": None, "domain": None, "dns_ttl": 0}}]}

        self.initial_ipv6_host_json = {
            "address_objects": [{"ipv6": {"name": None, "zone": None, "host": {"ip": None}}}]}
        self.initial_ipv6_network_json = {
            "address_objects": [
                {
                    "ipv6": {
                        "name": ""
                        ,
                        "zone": ""

                        , "network": {
                            "subnet": "::"
                            , "mask": ""
                        }
                    }
                }
            ]
        }
        self.initial_ipv6_range_json = {
            "address_objects": [{"ipv6": {"name": None, "zone": None, "range": {"begin": None, "end": None}}}]}

    # Get the modified url based on the object type passed.
    def modified_url(self, object_type, object_path=None, object_name_uuid=None, ip_type=None):
        if object_type.lower() in ['range', 'host', 'network']:
            url = self.address_object_url + ip_type.lower() + "/" + object_path + "/" + object_name_uuid
            logger.info(url)
        elif object_type in ['mac', 'fqdn']:
            url = self.address_object_url + object_type.lower() + "/" + object_path + "/" + object_name_uuid
        return url

    def get_all_addressobject_ipv4(self):
        output = self.fw.api_get(self.ao_ipv4)
        return output

    def get_all_addressobject_ipv6(self):
        output = self.fw.api_get(self.ao_ipv6)
        return output

    # Build the json depending on the objects values that are passed
    def build_json_address_object(self, **address_object):
        '''
        address_object = {
        "object_type":"host",
        "name":"drres_host",
        "zone":"LAN",
        "value":  "10.0.0.200"
        }
        '''
        json_input = {}
        object_type = address_object['object_type'].lower()
        ipv_type = None
        obj_type = None
        if object_type == "fqdn":
            try:
                json_input = copy.deepcopy(self.initial_fqdn_json)
                logger.info("FQDN json obtained")
                logger.info(json_input)
                json_input['address_objects'][0][object_type]['domain'] = address_object['value']
                json_input['address_objects'][0][object_type]['dns_ttl'] = address_object['dns_ttl']
            except KeyError as e:
                logger.info("Error: In creating json for FQDN object : {}".format(e))
        elif object_type == "mac":
            try:
                json_input = copy.deepcopy(self.initial_mac_json)
                logger.info("MAC json obtained")
                logger.info(json_input)
                json_input['address_objects'][0][object_type]['address'] = address_object['value']
                json_input['address_objects'][0][object_type]['multi_homed'] = address_object['multi_homed']
            except KeyError as e:
                logger.info("Error: In creating json for MAC object : {}".format(e))
        elif object_type == "host":
            try:
                value = address_object['value']
                ipaddress.ip_address(value)
                ipv_type = "ipv" + str(ipaddress.ip_address(value).version)
                logger.info("The IP types is as follows:" + ipv_type)
                try:
                    json_input = copy.deepcopy(self.initial_host_json)
                    json_input['address_objects'][0]['ipv4']['host']['ip'] = value
                except KeyError as e:
                    logger.info("Error: In creating json for Host object : {}".format(e))
            except ValueError:
                logger.info("Error: IP address provided is invalid")
        elif object_type == "range":
            value = address_object['value']
            if "," not in value:
                logger.info("Error:  IP address range is not separated by comma ")
            else:
                start_ip = value.split(",")[0]
                logger.info("start ip is : {}".format(start_ip))
                end_ip = value.split(",")[1]
                logger.info("end ip is : {}".format(end_ip))
                try:
                    ipaddress.ip_address(start_ip)
                    ipaddress.ip_address(end_ip)
                    if ipaddress.ip_address(start_ip).version != ipaddress.ip_address(end_ip).version:
                        logger.info("Difference in IP version")
                    else:
                        ipv_type = "ipv" + str(ipaddress.ip_address(start_ip).version)
                        logger.info("The final ip types is as : {}".format(ipv_type))

                        try:
                            json_input = copy.deepcopy(self.initial_range_json)
                            json_input['address_objects'][0]['ipv4']['range']['begin'] = start_ip
                            json_input['address_objects'][0]['ipv4']['range']['end'] = end_ip
                        except KeyError as e:
                            logger.info("Error: In creating json for Range address object : {}".format(e))

                except ValueError:
                    logger.info("Error: Invalid IP address")
        elif object_type == "network":
            value = address_object['value']
            if "," not in value:
                logger.info("Error : IP Address is not separated by comma")
            else:
                subnet_ip = value.split(",")[0]
                logger.info("subnet ip is : {}".format(subnet_ip))
                netmask_ip = value.split(",")[1]
                logger.info("Netmask ip is : {}".format(netmask_ip))
                try:
                    ipaddress.ip_address(subnet_ip)
                    version = ipaddress.ip_address(subnet_ip).version
                    logger.info(version)
                    ipaddress.ip_address(netmask_ip)
                    if ipaddress.ip_address(subnet_ip) == ipaddress.ip_address(netmask_ip):
                        logger.info("Error: Difference in IP address")
                    else:
                        ipv_type = "ipv" + str(ipaddress.ip_address(subnet_ip).version)
                        logger.info("The final ip types is as below : {}".format(ipv_type))
                    if ipv_type == "ipv4":
                        try:
                            json_input = copy.deepcopy(self.initial_network_json)
                            json_input['address_objects'][0]['ipv4']['network']['subnet'] = subnet_ip
                            json_input['address_objects'][0]['ipv4']['network']['mask'] = netmask_ip
                        except KeyError as e:
                            logger.info("Error: In creating json for Network object : {}".format(e))
                    else:
                        try:
                            netmask_ip1 = IPAddress(netmask_ip).netmask_bits()
                            json_input = copy.deepcopy(self.initial_network_json)
                            logger.info(json_input)
                            json_input['address_objects'][0]['ipv4']['network']['subnet'] = subnet_ip
                            json_input['address_objects'][0]['ipv4']['network']['mask'] = str(netmask_ip1)
                        except KeyError:
                            logger.info("Error: Network address object json failed")
                except:
                    logger.info("Error: Invalid IP versioning used")
        else:
            logger.info("Error: Invalid address object type entered")
        if ipv_type == "ipv6":
            try:
                json_input['address_objects'][0]['ipv6'] = json_input['address_objects'][0]['ipv4']
                del (json_input['address_objects'][0]['ipv4'])
            except KeyError:
                pass
        if object_type in ['range', 'host', 'network']:
            try:
                obj_type = ipv_type
                object_type = ipv_type
                logger.info("The object type defined as " + obj_type)
                json_input['address_objects'][0][obj_type]['name'] = address_object['name']
                json_input['address_objects'][0][obj_type]['zone'] = address_object['zone']
            except KeyError as e:
                logger.info("Error: In creating json for object type range, host, network  object : {}".format(e))
        else:
            try:
                obj_type = object_type
                logger.info("The object type defined as : {}".format(obj_type))
                json_input['address_objects'][0][object_type]['name'] = address_object['name']
                json_input['address_objects'][0][object_type]['zone'] = address_object['zone']
            except KeyError:
                logger.info("Error:Json input assignment failed")
        return json_input, object_type

    def build_json_ipv6_address_object(self, **kwargs):
        # address_opt = {
        #     'name': 'test1',
        #     'zone': 'LAN',
        #     'object_type': 'network',
        #     'subnet': '2000:1111::',
        #     'mask': '/64',
        # }
        json_input = {}
        if 'object_type' not in kwargs.keys() and 'name' not in kwargs.keys() and 'zone' not in kwargs.keys():
            logger.info("missing importain keys.. name,zone,obj_type! ")
            return json_input
        if kwargs['object_type'] == 'network':
            json_input = copy.deepcopy(self.initial_ipv6_network_json)
            if 'subnet' not in kwargs.keys() and 'mask' not in kwargs.keys():
                logger.info("missing importain keys.. subnet and mask! ")
            json_input['address_objects'][0]['ipv6']['name'] = kwargs['name']
            json_input['address_objects'][0]['ipv6']['zone'] = kwargs['zone']
            json_input['address_objects'][0]['ipv6']['network']['subnet'] = kwargs['subnet']
            json_input['address_objects'][0]['ipv6']['network']['mask'] = kwargs['mask']
            return json_input
        if kwargs['object_type'] == 'host':
            json_input = copy.deepcopy(self.initial_ipv6_host_json)
            if 'ip' not in kwargs.keys():
                logger.info("missing importain keys.. ip! ")
            json_input['address_objects'][0]['ipv6']['name'] = kwargs['name']
            json_input['address_objects'][0]['ipv6']['zone'] = kwargs['zone']
            json_input['address_objects'][0]['ipv6']['host']['ip'] = kwargs['ip']
            return json_input
        if kwargs['object_type'] == 'range':
            json_input = copy.deepcopy(self.initial_ipv6_range_json)
            if 'begin' not in kwargs.keys() and 'end' not in kwargs.keys():
                logger.info("missing importain keys.. subnet and mask! ")
            json_input['address_objects'][0]['ipv6']['name'] = kwargs['name']
            json_input['address_objects'][0]['ipv6']['zone'] = kwargs['zone']
            json_input['address_objects'][0]['ipv6']['range']['begin'] = kwargs['begin']
            json_input['address_objects'][0]['ipv6']['range']['end'] = kwargs['end']
            return json_input
        logger.info("In creating JSON error!")
        return json_input

    def config_addressobject(self, msg=False, **kwargs):
        json_input, object_type, = self.build_json_address_object(**kwargs)
        obj_url = self.address_object_url + object_type
        addrobj_resp = self.fw.api_post(obj_url, msg, data=json_input)
        return addrobj_resp

    def config_ipv6_addressobject(self, msg=False, **kwargs):
        json_input = self.build_json_ipv6_address_object(**kwargs)
        obj_url = self.address_object_url + 'ipv6'
        addrobj_resp = self.fw.api_post(obj_url, msg, data=json_input)
        return addrobj_resp

    def get_addressobject_by_name(self, name=None, version=None):
        if not name or not version:
            logger.info('Please specify ao name and version')
            return False
        name = name.replace(' ', '+')
        get_response = self.fw.api_get(self.address_object_url + f'{version}/name/{name}')
        return get_response

    def get_addressobject(self, object_type, object_path=None, object_name_uuid=None, ip_type=None):
        url = self.modified_url(object_type, object_path, object_name_uuid, ip_type)
        get_response = self.fw.api_get(url)
        return get_response

    def edit_addressobject(self, object_type, object_path, obj_name_uuid, json_put, ip_type=None, url=None, msg=False):
        url = self.modified_url(object_type, object_path, obj_name_uuid, ip_type)
        putaddrobj_resp = self.fw.api_put(url, msg, data=json_put)
        return putaddrobj_resp

    def delete_addressobject(self, object_type, object_path, object_name_uuid, ip_type, url=None, msg=False):
        url = self.modified_url(object_type, object_path, object_name_uuid, ip_type)
        addrobject_resp = self.fw.api_delete(url, msg)
        return addrobject_resp

    def del_addressobject(self, msg=False, **kwargs):
        # addressobj_del = {
        #     'ip_type': 'ipv6',/'ipv4'
        #     'name': 'test2',
        # }
        url = self.address_object_url + kwargs['ip_type'].lower() + '/name/' + kwargs['name']
        logger.info("Delete from {}".format(url))
        addrobject_resp = self.fw.api_delete(url, msg)
        return addrobject_resp

    def get_DAO_info(self, name):
        url = 'api/sonicos/dynamic-file/getDAOInfo.json?name=' + name
        get_response = self.fw.api_get(url)
        return get_response

    def del_ao_by_name(self, name=None, version=None, msg=False):
        if not name or not version:
            logger.info('Please specify ao name and version')
            return False
        url = self.address_object_url + f'{version}/name/{name}'
        logger.info("Delete from {}".format(url))
        if msg:
            resp, mesg = self.fw.api_delete(url, msg=True)
            return resp, mesg
        addrobject_resp = self.fw.api_delete(url)
        return addrobject_resp

    def purge_ao_by_name(self, name=None, version=None, msg=False):
        if not name or not version:
            logger.info('Please specify ao name and version')
            return False
        obj_url = self.base_url + f'purge/{version}/{name}'
        addrobj_resp = self.fw.api_post(obj_url, msg)
        return addrobj_resp

    def resolve_ao_by_name(self, name=None, version=None, msg=False, ):
        if not name or not version:
            logger.info('Please specify ao name and version')
            return False
        obj_url = self.base_url + f'resolve/{version}/{name}'
        addrobj_resp = self.fw.api_post(obj_url, msg)
        return addrobj_resp

    def purge_all(self, msg=False):
        obj_url = self.base_url + 'purge'
        addrobj_resp = self.fw.api_post(obj_url, msg)
        return addrobj_resp

    def resolve_all(self, msg=False):
        obj_url = self.base_url + 'resolve'
        addrobj_resp = self.fw.api_post(obj_url, msg)
        return addrobj_resp

    def edit_addressobject_by_name(self, oldname, msg=False, **kwargs):
        json_input, object_type = self.build_json_address_object(**kwargs)
        obj_url = self.address_object_url + object_type + '/name/' + oldname
        addrobj_resp = self.fw.api_put(obj_url, msg, data=json_input)
        return addrobj_resp

    def del_all_aos_by_type(self, object_type, name_list, msg=False):
        ao_list = []
        for name in name_list:
            ao_dict = {object_type: {'name': name}}
            ao_list.append(ao_dict)
        json_input = {"address_objects": ao_list}
        obj_url = self.address_object_url + object_type
        addrobject_resp = self.fw.api_delete(obj_url, msg, data=json_input)
        return addrobject_resp

    def del_all_address_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = 'api/sonicos/address-objects/ipv4'
        resp = self.fw.api_delete(url, msg, data=json_input)
        return resp

    def get_object_timestamps(self):
        url = 'api/sonicos/dynamic-file/getObjectTimestamps.json'
        resp = self.fw.api_get(url)
        return resp

    def get_object_list(self):
        url = 'api/sonicos/dynamic-file/getObjectList.json'
        resp = self.fw.api_get(url)
        return resp


class AddressgroupsApi():

    def __init__(self, fw):
        self.fw = fw
        self.address_group_url = 'api/sonicos/address-groups/'
        self.initial_group_json = {
            "address_group": {
                "ipv4": {
                    "name": None,
                    "address_object": {
                        "ipv4": None
                    },
                    # "mac": None,
                    # "fqdn": None,
                    "address_group": {
                        "ipv4": None
                    }
                }
            }
        }
        self.initial_ipv4to6_group_json = {
            "address_groups": [{
                "ipv6": {
                    "name": None,
                    "address_object": {
                        "ipv4": [{
                            "name": None
                        }]
                        , "ipv6": [{
                            "name": None
                        }]
                    }
                }
            }]
        }

    # Get the modified url based on the group type passed.
    def modified_group_url(self, group_type, group_path=None, group_value=None):
        group_url = self.address_group_url + group_type.lower()
        if group_path in ['name', 'uuid']:
            if group_value == '' or group_value is None:
                logger.info("Error: Value is expected")
            else:
                group_url = group_url + "/" + group_path + "/" + group_value

        return group_url

    # Build the address group json based on the group_type = ipv4/ipv6 , group name and value in the form of list of address object/groups
    def build_json_address_group(self, group_type=None, mac_fqdn_type=None, **address_group):
        '''
        address_group = {
            "ipv4": {
                "name": "Address_grpnew",
                "address_object": {
                    "ipv4": ["IPv4_Range_LAN"]
                },
                "address_group": {
                    "ipv4": None
                }
            }
        }
        '''
        json_input = {}
        ao_list = []
        ag_list = []
        if group_type == "":
            logger.info("Address group requires a object type")
        elif group_type in ['mac', 'fqdn']:
            group_type = "ipv6"
        elif group_type not in ['ipv4', 'ipv6', 'mac', 'fgdn']:
            logger.info("Group type expected is either ipv4 or ipv6")

        else:
            json_input = copy.deepcopy(self.initial_group_json)
            logger.info("The initial json formed is {}".format(json_input))
            if group_type == "ipv6":
                json_input['address_group']['ipv6'] = json_input['address_group']['ipv4']
                json_input['address_group']['ipv6']['address_object']['ipv6'] = \
                json_input['address_group']['ipv6']['address_object']['ipv4']
                json_input['address_group']['ipv6']['address_group']['ipv6'] = \
                json_input['address_group']['ipv6']['address_group']['ipv4']

                del (json_input['address_group']['ipv4'])
                del (json_input['address_group']['ipv6']['address_object']['ipv4'])
                del (json_input['address_group']['ipv6']['address_group']['ipv4'])
                if (mac_fqdn_type == "mac"):
                    if (address_group[group_type]["address_object"]["mac"] != None):
                        for ao_name in address_group["ipv6"]["address_object"]["mac"]:
                            mac_obj = {"name": ao_name}
                            logger.info(ao_list.append(mac_obj))
                        json_input["address_group"]["ipv6"]["address_object"]["mac"] = ao_list
                    else:
                        del (address_group[group_type]["address_object"]["mac"])

                if (mac_fqdn_type == "fqdn"):
                    if (address_group[group_type]["address_object"]["fqdn"] != None):
                        for ao_name in address_group["ipv6"]["address_object"]["fqdn"]:
                            fqdn_obj = {"name": ao_name}
                            logger.info(ao_list.append(fqdn_obj))
                        json_input["address_group"]["ipv6"]["address_object"]["fqdn"] = ao_list
                    else:
                        del (address_group[group_type]["address_object"]["fqdn"])
                if (address_group[group_type]["address_group"][group_type] == None):
                    del (json_input["address_group"][group_type]["address_group"])
                    if (json_input["address_group"][group_type]["address_object"][group_type] == None):
                        del (json_input["address_group"][group_type]["address_object"][group_type])
        try:

            json_input["address_group"][group_type]['name'] = address_group[group_type]['name']
            logger.info("After assignemnt is {}".format(json_input))
            for ao_name in address_group[group_type]["address_object"][group_type]:
                address_obj = {"name": ao_name}
                logger.info(ao_list.append(address_obj))
            json_input["address_group"][group_type]["address_object"][group_type] = ao_list
            if (address_group[group_type]["address_group"][group_type] != None):
                for ag_name in address_group[group_type]["address_group"][group_type]:
                    address_grp = {"name": ag_name}
                    ag_list.append(address_grp)
                json_input["address_group"][group_type]["address_group"][group_type] = ag_list
            else:
                del (json_input["address_group"][group_type]["address_group"])

            # if(group_type == "ipv4"):
            #     del (json_input["address_group"][group_type]["address_object"]["fqdn"])
            #     del (json_input["address_group"][group_type]["address_object"]["mac"])
        except KeyError as ke:
            logger.info("Error: In creating json for address group : {}".format(e))

        return json_input

    def build_4to6_address_group_json(self, **kwargs):
        # addressgroup_opt = {
        #     'name': 'test',
        #     'group_type': 'ipv6',
        #     'addr_obj': {
        #         'ipv4': 'test1',
        #         'ipv6': 'test2'
        #     }
        # }
        json_input = {}
        if 'name' not in kwargs:
            logger.info("missing key : name")
        else:
            json_input = copy.deepcopy(self.initial_ipv4to6_group_json)
            json_input['address_groups'][0]['ipv6']['name'] = kwargs['name']
            json_input['address_groups'][0]['ipv6']['address_object']['ipv4'][0]['name'] = kwargs['addr_obj']['ipv4']
            json_input['address_groups'][0]['ipv6']['address_object']['ipv6'][0]['name'] = kwargs['addr_obj']['ipv6']
            logger.info(json_input)
            return json_input
        logger.info("KeyError!")
        return json_input

    def config_addressgroup(self, msg=False, url=None, group_type=None, mac_fqdn_type=None, **kwargs):
        json_input = self.build_json_address_group(group_type, mac_fqdn_type, **kwargs)
        obj_url = url + '/' + group_type
        addrobj_resp = self.fw.api_post(obj_url, msg, data=json_input)
        return addrobj_resp

    def config_ipv4to6_addressgroup(self, msg=False, **kwargs):
        json_input = self.build_4to6_address_group_json(**kwargs)
        obj_url = self.address_group_url + kwargs['group_type']
        addrobj_resp = self.fw.api_post(obj_url, msg, data=json_input)
        return addrobj_resp

    # group_type, group_path = None, group_value = None
    def get_addressgroup(self, group_type, group_path=None, group_name_uuid=None):
        url = self.modified_group_url(group_type, group_path, group_name_uuid)
        get_response = self.fw.api_get(url)
        return get_response

    # Modify the address group parameter values
    def edit_addressgroup(self, group_type, group_path, group_name_uuid, **kwargs):
        json_put = self.build_json_address_group(group_type, **kwargs)
        url = self.modified_group_url(group_type, group_path, group_name_uuid)
        putaddrgrp_resp = self.fw.api_put(url, data=json_put)
        return putaddrgrp_resp

    # Delete address group by name/uuid.
    def delete_addressgroup(self, group_type, group_path=None, group_name_uuid=None):
        url = self.modified_group_url(group_type, group_path, group_name_uuid)
        addrgroup_resp = self.fw.api_delete(url)
        return addrgroup_resp


class InterfaceIPv6Api:
    '''InterfaceIPv6Api class'''
    default_options = {
        # 'name': 'x1',
        # 'zone': 'WAN',
        # 'mode': 'static',
        # 'comment': '',
        "dhcpv6": {
            "prefix_delegation": False,
            "rapid_commit": False,
            # "send_hints": False,
            "mode": "auto",  # manual
            "aftr_name_option": False
        },
        "static": {
            "ip": "::",
            "prefix_length": 64,
            "gateway": "::",
            "advertise_subnet_prefix": False,
            "router_advertisement": {
                "enable": False,
                "interval_min": 200,
                "interval_max": 600,
                "link_mtu": 0,
                "reachable_time": 0,
                "retransmit_timer": 0,
                "current_hop_limit": 64,
                "router_lifetime": 1800,
                "router_preference": "medium",
                "managed": False,
                "other_config": False
            }},
        'pppoe6': {
            ####auto
            'inactivity': {},
            'lcp_echo_packets': False,
            'ncp_neg_retrans': 5,
            'reconnect': {},
            ##dhcpv6
            'prefix_delegation': False,
            'rapid_commit': False,
            'dhcp_mode': 'manual',
            ##staitc
            'advertise_subnet_prefix': False,
            'dns1': '::',
            'dns2': '::',
            'dns3': '::',
            'ip': '::',
            'gateway': '',
            'prefix_length': 10,
            'router_advertisement': {
                "enable": False,
                "interval_min": 200,
                "interval_max": 600,
                "link_mtu": 0,
                "reachable_time": 0,
                "retransmit_timer": 0,
                "current_hop_limit": 64,
                "router_lifetime": 1800,
                "router_preference": "medium",
                "managed": False,
                "other_config": False
            }

        },
        'ipv6_traffic': True,
        'listen_router_advertisement': False,
        # 'stateless_address_autoconfig': False,
        'duplicate_address_detection_transmits': 1,
        'reachable_time': 30,
        # 'max_ndp_size': 128,
        'mgmt_https': False,
        'mgmt_ping': False,
        'mgmt_ssh': False,
        'mgmt_snmp': False,
        # 'https_redirect': False, # only can set is True when mgmt_https is True
        'user_http': False,
        'user_https': False,
    }

    default_tunnel_options = {
        'zone': '',
        'type': '',
        'mtu': 1280,
        'mgmt_https': False,
        'mgmt_ping': False,
        'mgmt_ssh': False,
        'mgmt_snmp': False,
        # 'https_redirect': False, # only can set is True when mgmt_https is True
        'user_http': False,
        'user_https': False,
        'comment': '',
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/interfaces/ipv6/base'
        self.url_prefix = 'api/sonicos/interfaces/ipv6/prefixes'
        self.url_tunnel = 'api/sonicos/tunnel-interfaces/ipv6'
        self.initial_ipv6_interface_json = {
            "interfaces": [{
                "ipv6": {
                    "name": "",
                    "ip_assignment": {
                        "mode": {
                        }
                    },
                    "ipv6_traffic": True,
                    "listen_router_advertisement": False,
                    # "stateless_address_autoconfig":False,
                    "duplicate_address_detection_transmits": 1,
                    "reachable_time": 30,
                    # "max": {
                    #     "ndp_size": 128
                    # },
                    "management": {
                        "https": False,
                        "ping": False,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                    # "https_redirect": True
                }
            }
            ]
        }
        self.initial_ipv6_auto_interface_json = {
            "interfaces": [{
                "ipv6": {
                    "name": "X1",
                    "ip_assignment": {
                        "mode": {
                        }
                    },
                    "ipv6_traffic": True,
                    "duplicate_address_detection_transmits": 1,
                    "reachable_time": 30,
                    "management": {
                        "https": False,
                        "ping": False,
                        "snmp": False,
                        "ssh": False
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                }
            }
            ]
        }
        self.initial_ipv6_prefix_static_json = {
            "interfaces": [{
                "ipv6": {
                    "name": "",
                    "ip_assignment": {
                        "mode": {
                            "static": {
                                "router_advertisement": {
                                    "prefix": [{
                                        "prefix": "::",
                                        "valid_lifetime": 500,
                                        "preferred": {
                                            "lifetime": 400
                                        },
                                        "on_link": True,
                                        "autonomous": True
                                    }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
            ]
        }

        self.initial_ipv6_unassign_json = {
            "interfaces": [{
                "ipv6": {
                    "name": "",
                    "ip_assignment": {
                    }
                }
            }]
        }

        self.initial_ipv6_unassign_x0_x1_json = {
            "interfaces": [{
                "ipv6": {
                    "name": "",
                    "ip_assignment": {
                        "mode": {
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
                    },
                    "ipv6_traffic": True,
                    "listen_router_advertisement": False,
                    "duplicate_address_detection_transmits": 1,
                    "reachable_time": 30,
                    "management": {
                        "https": False,
                        "ping": False,
                        "snmp": False,
                        "ssh": False,
                    },
                    "user_login": {
                        "http": False,
                        "https": False
                    },
                }
            }]
        }

        self.initial_ipv6_extra_ip_json = {
            "interfaces": [
                {
                    "ipv6": {
                        "name": None
                        , "ip_assignment": {
                            "mode": {
                                "static": {
                                    "extra_ip": [
                                    ]
                                }
                            }
                        }
                    }
                }]
        }

        self.initial_ipv6_tunnel_json = {
            "tunnel_interfaces": [
                {
                    "ipv6": {
                        "name": "",
                        "zone": "",
                        "type": {},  # manual,6rd, gre, 6to4
                        "comment": "",
                        "management": {
                            "http": False,
                            "https": False,
                            "ping": False,
                            "snmp": False,
                            "ssh": False
                        },
                        "user_login": {
                            "http": False,
                            "https": False
                        },
                        # "https_redirect": False
                    }
                }
            ]
        }

    def config_ipv6_static_prefix(self, msg=False, **kwargs):
        print(kwargs)
        json_input = copy.deepcopy(self.initial_ipv6_prefix_static_json)
        try:
            json_input['interfaces'][0]['ipv6']['name'] = kwargs['name'].upper()
            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement']['prefix'][0][
                'prefix'] = kwargs['prefix'].upper()
            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement']['prefix'][0][
                'valid_lifetime'] = kwargs['valid_lt']
            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement']['prefix'][0][
                'preferred']['lifetime'] = kwargs['prefer_lt']
            if 'autonomous' in kwargs:
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                    'prefix'][0]['autonomous'] = kwargs['autonomous']
            if 'on_link' in kwargs:
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['static']['router_advertisement'][
                    'prefix'][0]['on_link'] = kwargs['on_link']
        except Exception as e:
            print(e)
            print("prefix json obtained")
            print(json_input)
        url = self.url_prefix
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def config_interface_ipv6(self, msg=False, **kwargs):
        self.options = dict(InterfaceIPv6Api.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_ipv6_interface(**kwargs)
        url = self.url + '/name/' + kwargs['name']
        if 'vlan' in kwargs:
            url += '/vlan/' + str(kwargs['vlan'])
        interface_resp = self.fw.api_put(url, msg, data=json_input)
        return interface_resp

    def config_interface_ipv6_new_json(self, msg=False, **kwargs):
        """
        Example:
        x0_json = {
          "interfaces": [
            {
              "ipv6": {
                "one_arm_mode": False,
                "one_arm_peer": "",
                "management": {
                  "https": True,
                  "https_source": {
                    "any": True
                  },
                  "ping": True,
                  "ping_source": {
                    "any": True
                  },
                  "snmp": True,
                  "snmp_source": {
                    "any": True
                  },
                  "ssh": True,
                  "ssh_source": {
                    "any": True
                  }
                },
                "user_login": {
                  "http": True,
                  "https": True
                },
                "ipv6_traffic": True,
                "listen_router_advertisement": False,
                "duplicate_address_detection_transmits": 1,
                "reachable_time": 30,
                "name": "X0",
                "ip_assignment": {
                  "mode": {
                    "static": {
                      "ip": "2000::168",
                      "prefix_length": 64,
                      "advertise_subnet_prefix": False,
                      "router_advertisement": {
                        "enable": False,
                        "interval": {
                          "min": 200,
                          "max": 600
                        },
                        "link_mtu": {},
                        "reachable_time": {},
                        "retransmit_timer": {},
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
                }
              }
            }
          ]
        }
        """
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def show_interface(self, name=None):
        if name:
            url = self.url + '/name/' + name
        else:
            url = self.url
        interface_resp = self.fw.api_get(url)
        return interface_resp

    def build_json_ipv6_interface(self, **kwargs):
        json_input = {}
        print(kwargs)
        ipv6_dhcpv6_json = {
            "prefix_delegation": False,
            "rapid_commit": False,
            #    "send_hints": False,
            #    "mode": "auto",
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
                json_input['interfaces'][0]['ipv6']['listen_router_advertisement'] = kwargs[
                    'listen_router_advertisement']
                if kwargs['listen_router_advertisement']:
                    dict = {"stateless_address_autoconfig": False, }
                    json_input['interfaces'][0]['ipv6'].update(dict)
                    if 'stateless_address_autoconfig' in kwargs.keys():
                        json_input['interfaces'][0]['ipv6']['stateless_address_autoconfig'] = kwargs[
                            'stateless_address_autoconfig']
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
                if 'mgmt_https' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['https'] = kwargs['mgmt_https']
                if 'mgmt_ssh' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['ssh'] = kwargs['mgmt_ssh']
                if 'mgmt_ping' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['ping'] = kwargs['mgmt_ping']
                if 'mgmt_snmp' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['management']['snmp'] = kwargs['mgmt_snmp']

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
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['rapid_commit'] = \
                kwargs['dhcpv6']['rapid_commit']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['send_hints'] = kwargs['dhcpv6'][
                    'send_hints']

                if 'mode' in kwargs['dhcpv6'].keys() and kwargs['dhcpv6']['mode'] == 'manual':
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['mode'] = 'manual'
                    if 'info_only' in kwargs['dhcpv6'] and kwargs['dhcpv6']['info_only']:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['info_only'] = True
                    else:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['info_only'] = False
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['aftr_name_option'] = \
                kwargs['dhcpv6']['aftr_name_option']
            elif kwargs['mode'] == 'pppoe6':
                if 'listen_router_advertisement' in kwargs.keys():
                    json_input['interfaces'][0]['ipv6']['listen_router_advertisement'] = kwargs[
                        'listen_router_advertisement']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6'] = {}
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['inactivity'] = {}
                if kwargs['pppoe6']['inactivity']:
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['inactivity']['value'] = \
                    kwargs['pppoe6']['inactivity']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['reconnect'] = {}
                if kwargs['pppoe6']['reconnect']:
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['reconnect']['value'] = \
                    kwargs['pppoe6']['reconnect']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['lcp_echo_packets'] = \
                kwargs['pppoe6']['lcp_echo_packets']
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['ncp_neg_retrans'] = \
                kwargs['pppoe6']['ncp_neg_retrans']
                if 'mode_assign' not in kwargs['pppoe6']:
                    logger.error('Please specify mode_assign to one of auto, dhcpv6, static')
                    return False
                json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['mode_assignment'] = \
                kwargs['pppoe6']['mode_assign']
                if kwargs['pppoe6']['mode_assign'] == 'auto':

                    json_input['interfaces'][0]['ipv6'].pop('listen_router_advertisement')

                elif kwargs['pppoe6']['mode_assign'] == 'dhcpv6':
                    print('11111******dhcpv6*********')
                    print(json_input)
                    if 'dhcp_mode' in kwargs['pppoe6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['mode'] = \
                            kwargs['pppoe6']['dhcp_mode']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['prefix_delegation'] = \
                    kwargs['pppoe6']['prefix_delegation']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['rapid_commit'] = \
                    kwargs['pppoe6']['rapid_commit']

                    print('22222******dhcpv6*********')
                    print(json_input)

                elif kwargs['pppoe6']['mode_assign'] == 'static':

                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['gateway'] = \
                        kwargs['pppoe6']['gateway']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['ip'] = kwargs['pppoe6'][
                        'ip']
                    json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['prefix_length'] = \
                        kwargs['pppoe6']['prefix_length']

                    if 'advertise_subnet_prefix' in kwargs['pppoe6']:
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6'][
                            'advertise_subnet_prefix'] = kwargs['pppoe6']['advertise_subnet_prefix']
                    if 'dns' in str(kwargs['pppoe6'].keys()):
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['primary'] = \
                        kwargs['pppoe6']['dns1']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['secondary'] = \
                        kwargs['pppoe6']['dns2']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['dns']['tertiary'] = \
                        kwargs['pppoe6']['dns3']

                    if 'router_advertisement' in kwargs['pppoe6'].keys():
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'enable'] = kwargs['pppoe6']['router_advertisement']['enable']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'interval'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'interval']['min'] = kwargs['pppoe6']['router_advertisement']['interval_min']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'interval']['max'] = kwargs['pppoe6']['router_advertisement']['interval_max']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'link_mtu'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['link_mtu']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                                'link_mtu']['value'] = kwargs['pppoe6']['router_advertisement']['link_mtu']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'reachable_time'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['reachable_time']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                                'reachable_time']['value'] = kwargs['pppoe6']['router_advertisement']['reachable_time']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'retransmit_timer'] = {}
                        if not kwargs['pppoe6']['router_advertisement']['retransmit_timer']:
                            json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                                'retransmit_timer']['value'] = kwargs['pppoe6']['router_advertisement']['retransmit_timer']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'current_hop_limit'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'current_hop_limit']['value'] = kwargs['pppoe6']['router_advertisement']['current_hop_limit']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'router'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'router']['lifetime'] = {}
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'router']['lifetime']['value'] = kwargs['pppoe6']['router_advertisement']['router_lifetime']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'router']['preference'] = kwargs['pppoe6']['router_advertisement']['router_preference']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'managed'] = kwargs['pppoe6']['router_advertisement']['managed']
                        json_input['interfaces'][0]['ipv6']['ip_assignment']['mode']['pppoe6']['router_advertisement'][
                            'other_config'] = kwargs['pppoe6']['router_advertisement']['other_config']

                print('3333******pppoe6********')
                print(json_input)

            elif kwargs['mode'] == 'static':
                # if kwargs['zone'] == 'DMZ' or kwargs['zone'] == 'WLAN':
                #     json_input['interfaces'][0]['ipv6']['ip_assignment']['mode'] = {
                #         "static": {
                #         "ip": "::",
                #         "prefix_length": 64,
                #         "advertise_subnet_prefix": False,
                #         "router_advertisement": {
                #             "enable": False,
                #             "interval": {
                #                 "min": 200,
                #                 "max": 600
                #             },
                #         "link_mtu": {},
                #         "reachable_time": {},
                #         "retransmit_timer": {},
                #         "current_hop_limit": {
                #             "value": 64
                #         },
                #         "router": {
                #             "lifetime": {
                #                 "value": 1800
                #             },
                #         "preference": "medium"
                #         },
                #         "managed": False,
                #         "other_config": False
                #         }
                #     }
                # }
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
        except Exception as e:
            print(e)
        print("interface json obtained")
        print(json_input)
        return json_input

    def add_tunnel_interface(self, msg=False, **kwargs):
        self.options = dict(InterfaceIPv6Api.default_tunnel_options)
        self.options.update(kwargs)
        kwargs = self.options
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of manual,6rd, gre, 6to4')
            return False
        json_input = self.build_json_ipv6_tunnel_interface(**kwargs)
        rc = self.fw.api_post(self.url_tunnel, msg, data=json_input)
        return rc

    def edit_tunnel_interface(self, tunnel_name=None, msg=False, **kwargs):
        self.options = dict(InterfaceIPv6Api.default_tunnel_options)
        self.options.update(kwargs)
        kwargs = self.options

        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of manual,6rd, gre, 6to4')
            return False
        json_input = self.build_json_ipv6_tunnel_interface(**kwargs)
        if not tunnel_name:
            tunnel_name = json_input['tunnel_interfaces'][0]['ipv6']['name']
        url = self.url_tunnel + '/name/' + tunnel_name
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def delete_tunnel_interface(self, name=None, msg=False, ):
        if not name:
            logger.error('Please specify the tunnel name.')
            return False
        rc = self.fw.api_delete(self.url_tunnel + '/name/' + name, msg, data=None)
        return rc

    def get_tunnel_interface(self, name=None, msg=False, ):
        if not name:
            logger.error('Please specify the tunnel name.')
            return False
        rc = self.fw.api_get(self.url_tunnel + '/name/' + name)
        return rc

    def get_6rd_protocal(self):
        url = 'api/sonicos/dynamic-file/getIPv6TunnelInterface6rdProtocolInfo.json?id=1073742212'
        rc = self.fw.api_get(url)
        return rc

    def build_json_ipv6_tunnel_interface(self, **kwargs):
        json_input = {}
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of manual,6rd, gre, 6to4')
            return None
        json_input = copy.deepcopy(self.initial_ipv6_tunnel_json)
        try:
            json_input['tunnel_interfaces'][0]['ipv6']['name'] = kwargs['name']
            json_input['tunnel_interfaces'][0]['ipv6']['type'] = {kwargs['type']: {}}
            json_input['tunnel_interfaces'][0]['ipv6']['zone'] = kwargs['zone']
            json_input['tunnel_interfaces'][0]['ipv6']['comment'] = kwargs['comment']
            json_input['tunnel_interfaces'][0]['ipv6']['management'] = {}
            json_input['tunnel_interfaces'][0]['ipv6']['management']['https'] = kwargs['mgmt_https']
            json_input['tunnel_interfaces'][0]['ipv6']['management']['ping'] = kwargs['mgmt_ping']
            json_input['tunnel_interfaces'][0]['ipv6']['management']['ssh'] = kwargs['mgmt_ssh']
            json_input['tunnel_interfaces'][0]['ipv6']['management']['snmp'] = kwargs['mgmt_snmp']
            json_input['tunnel_interfaces'][0]['ipv6']['user_login'] = {}
            json_input['tunnel_interfaces'][0]['ipv6']['user_login']['https'] = kwargs['user_https']
            json_input['tunnel_interfaces'][0]['ipv6']['user_login']['http'] = kwargs['user_http']
            if kwargs['type'] == 'manual':
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['ip'] = kwargs['ip']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['prefix_length'] = int(
                    kwargs['prefix_length'])
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['bound_to'] = kwargs['bound_to']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['remote'] = {}
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['remote']['ipv4_address'] = kwargs[
                    'ipv4_address']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['remote']['ipv6_network'] = kwargs[
                    'ipv6_network']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['manual']['remote']['link_mtu'] = kwargs['mtu']
            elif kwargs['type'] == '6rd':
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['ip'] = kwargs['ip']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['prefix_length'] = int(
                    kwargs['prefix_length'])
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['dynamic'] = kwargs['dynamic']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['bound_to'] = kwargs['bound_to']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['6rd'] = {}
                if not kwargs['dynamic']:
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['6rd']['prefix'] = kwargs['6rd_prefix']
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['6rd']['prefix_length'] = kwargs[
                        '6rd_prefix_length']
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['border_relay_ipv4_address'] = kwargs[
                        'border_relay_ipv4_address']
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['mask_length'] = kwargs['mask_length']
                else:
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['6rd']['prefix'] = '::'
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['6rd']['prefix_length'] = 0
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['border_relay_ipv4_address'] = '0.0.0.0'
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['mask_length'] = 0
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['link_mtu'] = kwargs['mtu']
                try:
                    json_input['tunnel_interfaces'][0]['ipv6']['type']['6rd']['default_route'] = kwargs['default_route']
                except:
                    pass
            elif kwargs['type'] == '6to4':
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['ip'] = kwargs['ip']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['prefix_length'] = kwargs['prefix_length']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['bound_to'] = kwargs['bound_to']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['enable'] = kwargs['enable']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['ip'] = kwargs['ip']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['6to4']['link_mtu'] = kwargs['mtu']
            elif kwargs['type'] == 'gre':
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['ip'] = kwargs['ip']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['prefix_length'] = int(
                    kwargs['prefix_length'])
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['bound_to'] = kwargs['bound_to']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['remote'] = {}
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['remote']['ipv4_address'] = kwargs[
                    'ipv4_address']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['gre']['remote']['ipv6_network'] = kwargs[
                    'ipv6_network']
            elif kwargs['type'] == 'isatap':
                json_input['tunnel_interfaces'][0]['ipv6']['type']['isatap']['bound_to'] = kwargs['bound_to']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['isatap']['prefix'] = kwargs['prefix']
                json_input['tunnel_interfaces'][0]['ipv6']['type']['isatap']['link_mtu'] = kwargs['link_mtu']

            else:
                logger.error('Please specify type to one of manual,6rd, gre, 6to4')
                return False
        except Exception as e:
            logger.error("Error: In creating JSON for tunnel interface {}".format(e))
        return json_input

    def build_ipv6_json_unassign(self, interface):
        json_input = {}
        json_input = copy.deepcopy(self.initial_ipv6_unassign_json)
        json_input['interfaces'][0]['ipv6']['name'] = interface
        logger.info(json_input)
        return json_input

    def unassign_ipv6_interface(self, msg=False, interface=None):
        if interface.upper() == 'X0' or interface.upper() == 'X1':
            json_input = self.initial_ipv6_unassign_x0_x1_json
            json_input['interfaces'][0]['ipv6']['name'] = interface
            interface_resp = self.fw.api_put(self.url, msg, data=json_input)
            return interface_resp
        json_input = self.build_ipv6_json_unassign(interface.upper())
        interface_resp = self.fw.api_put(self.url, msg, data=json_input)
        return interface_resp

    def get_interface_address(self, name=None):
        url_tmp = 'api/sonicos/reporting/interfaces/ipv6/status'
        if name:
            url_tmp = url_tmp + '/name/' + name.lower()
        resp = self.fw.api_get(url_tmp)
        return resp


    def get_ipv6_interface_base(self, name=None):
        url_tmp = 'api/sonicos/interfaces/ipv6/base'
        if name:
            url_tmp = url_tmp + '/name/' + name.lower()
        resp = self.fw.api_get(url_tmp)
        return resp

    def add_ipv6_extra_ip(self, msg=False, **kwargs):
        # x0_opt = {
        #     'name': 'X0',
        #     'mode': 'static',
        #     'ip': '2000:2222::1',
        #     'subnet_prefix_adv': False
        # }
        url = 'api/sonicos/interfaces/ipv6/extra-ip'
        json_input = self.fw.api_get(url)
        if json_input == {}:
            json_input = copy.deepcopy(self.initial_ipv6_extra_ip_json)
        logger.info(json_input)
        extra_ip_json = {
            "type": {
                "static": {
                    "ip": "::"
                    , "prefix_length": 64
                    , "advertise_subnet_prefix": True
                }
            }
        }
        extra_ip_6rd_json = {
            "type": {
                "6rd": {
                    "preferred_ip": "::",
                    "preferred_prefix_length": 64,
                    "advertise_subnet_prefix": True
                }
            }
        }
        extra_ip_pd_json = {
            "type": {
                "prefix_delegation": {
                    "preferred_ip": "::",
                    "preferred_prefix_length": 64,
                    "delegated_prefix": "",  # 'X3 Delegated Prefix'
                    "advertise_subnet_prefix": True
                }
            }
        }
        if 'name' in kwargs.keys():
            json_input['interfaces'][0]['ipv6']['name'] = kwargs['name'].upper()
        if 'type' not in kwargs:
            logger.error('Please specify type to one of: static, 6rd, pd')
            return False
        if kwargs['type'] == 'static':
            if 'ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['ip'] = kwargs['ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['prefix_length'] = kwargs['prefix_length']
        elif kwargs['type'] == 'prefix_delegation':
            extra_ip_json = extra_ip_pd_json
            if 'delegated_prefix' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['delegated_prefix'] = kwargs['delegated_prefix']
            if 'preferred_ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_ip'] = kwargs['preferred_ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_prefix_length'] = kwargs['prefix_length']
        else:
            extra_ip_json = extra_ip_6rd_json
            if 'preferred_ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_ip'] = kwargs['preferred_ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_prefix_length'] = kwargs['prefix_length']
        if 'subnet_prefix_adv' in kwargs.keys():
            extra_ip_json['type'][kwargs['type']]['advertise_subnet_prefix'] = kwargs['subnet_prefix_adv']
        json_input["interfaces"][0]['ipv6']['ip_assignment']['mode']['static']['extra_ip'].append(extra_ip_json)
        logger.info(extra_ip_json)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def delete_ipv6_extra_ip(self, msg=False, **kwargs):
        # x0_opt = {
        #     'name': 'X0',
        #     'mode': 'static',
        #     'ip': '2000:2222::1',
        #     'subnet_prefix_adv': False
        # }
        url = 'api/sonicos/interfaces/ipv6/extra-ip'
        json_input = self.fw.api_get(url)
        if json_input == {}:
            json_input = copy.deepcopy(self.initial_ipv6_extra_ip_json)
        logger.info(json_input)
        extra_ip_json = {
            "type": {
                "static": {
                    "ip": "::"
                    , "prefix_length": 64
                    , "advertise_subnet_prefix": True
                }
            }
        }
        extra_ip_6rd_json = {
            "type": {
                "6rd": {
                    "preferred_ip": "::",
                    "preferred_prefix_length": 64,
                    "advertise_subnet_prefix": True
                }
            }
        }
        extra_ip_pd_json = {
            "type": {
                "prefix_delegation": {
                    "preferred_ip": "::",
                    "preferred_prefix_length": 64,
                    "delegated_prefix": "",  # 'X3 Delegated Prefix'
                    "advertise_subnet_prefix": True
                }
            }
        }
        if 'name' in kwargs.keys():
            json_input['interfaces'][0]['ipv6']['name'] = kwargs['name'].upper()
        if 'type' not in kwargs:
            logger.error('Please specify type to one of: static, 6rd, pd')
            return False
        if 'subnet_prefix_adv' in kwargs.keys():
            extra_ip_json['type'][kwargs['type']]['advertise_subnet_prefix'] = kwargs['subnet_prefix_adv']
        if kwargs['type'] == 'static':
            if 'ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['ip'] = kwargs['ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['prefix_length'] = kwargs['prefix_length']
        elif kwargs['type'] == 'prefix_delegation':
            extra_ip_json = extra_ip_pd_json
            if 'delegated_prefix' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['delegated_prefix'] = kwargs['delegated_prefix']
            if 'preferred_ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_ip'] = kwargs['preferred_ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_prefix_length'] = kwargs['prefix_length']
        else:
            extra_ip_json = extra_ip_6rd_json
            if 'preferred_ip' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_ip'] = kwargs['preferred_ip']
            if 'prefix_length' in kwargs.keys():
                extra_ip_json['type'][kwargs['type']]['preferred_prefix_length'] = kwargs['prefix_length']
        json_input["interfaces"][0]['ipv6']['ip_assignment']['mode']['static']['extra_ip'].append(extra_ip_json)
        logger.info(extra_ip_json)
        rc = self.fw.api_delete(url, msg, data=json_input)
        return rc

    def get_default_route_policy_v6(uuid=None):
        """get default ipv6 route rule"""
        url_v6 = 'api/sonicos/reporting/route-policies/ipv6/system'
        if uuid:
            url_v6 += '/uuid' + uuid
        resp = fw.api_get(url_v6)
        return resp

    def get_ipv6_extra_ip(self):
        """ get static ipv6 extra ip address """
        url_tmp = 'api/sonicos/interfaces/ipv6/extra-ip'
        resp = self.fw.api_get(url_tmp)
        return resp

    def get_ipv6_prefixes(self):
        """ get ipv6 interface prefixes """
        url = 'api/sonicos/interfaces/ipv6/prefixes'
        resp = self.fw.api_get(url)
        return resp


class ZoneObjectsApi:

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/zones'

    def add_zone_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        zone_resp = self.fw.api_post(self.url, msg, data=json_input)
        return zone_resp

    def edit_zone_object(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name should be specified for edit zone object.')
            return False
        zone_resp = self.fw.api_put(url, msg, data=json_input)
        return zone_resp

    def show_zone_object(self, name=None):
        self.url = 'api/sonicos/zones'
        if name:
            url = self.url + '/name/' + name
        else:
            url = self.url
        zone_resp = self.fw.api_get(url)
        return zone_resp

    def show_zone_objects(self):
        url = 'api/sonicos/zones'
        zone_resp = self.fw.api_get(url)
        return zone_resp

    def get_reporting_zones_objects(self):
        url = 'api/sonicos/reporting/zones'
        zone_resp = self.fw.api_get(url)
        return zone_resp

    def delete_zone_object(self, name=None, msg=False):
        if name:
            url = self.url + '/name/' + name
        else:
            logger.error('name should be specified for delete zone object.')
            if msg:
                return [False, {}]
            return False
        zone_resp = self.fw.api_delete(url, msg)
        return zone_resp

    def switch_app_control_on_zone(self, name=None, enable=False):
        base_dict = {
            'name': name,
            "app_control": enable,
        }
        zone_dict = {"zones": [base_dict]}
        res = self.edit_zone_object(name, **zone_dict)
        return res


class DHCPServerApi:
    '''DHCPServerApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_dhcp_server_base = 'api/sonicos/dhcp-server'
        self.initial_ipv4_dhcp_option_group_json = {
            "dhcp_server": {
                "ipv4": {
                    "option": {
                        "group": [
                            {
                                "name": '',
                                "option": {
                                    "object": [
                                        {
                                            "name": "option_230"
                                        },
                                        {
                                            "name": "option_150"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }
        self.initial_ipv6_dhcp_option_group_json = {
            "dhcp_server": {
                "ipv6": {
                    "option": {
                        "group": [
                            {
                                "name": '',
                                "option": {
                                    "object": [
                                        {
                                            "name": "option_230"
                                        },
                                        {
                                            "name": "option_150"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        }

    def config_dhcp_server_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['dhcp_server'].keys():
            url = 'api/sonicos/dhcp-server/ipv6/base'
        else:
            url = 'api/sonicos/dhcp-server/ipv4/base'
        dhcp_resp = self.fw.api_put(url, msg, data=json_input)
        return dhcp_resp

    def get_dhcp_server_settings(self, version=4):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/base'
        else:
            url = 'api/sonicos/dhcp-server/ipv6/base'
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def add_dhcp_server_option_object(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['dhcp_server'].keys():
            url = 'api/sonicos/dhcp-server/ipv6/option/objects'
        else:
            url = 'api/sonicos/dhcp-server/ipv4/option/objects'
        dhcp_resp = self.fw.api_post(url, msg, data=json_input)
        return dhcp_resp

    def config_dhcp_server_option_object(self, msg=False, **kwargs):
        ''' Example:
            kwargs = {
                'ipv4': {
                    "name":"test",
                    "number":4,
                    "value":[{"ip":"1.1.1.1"}],
                    "array":True
                }
            }
        '''
        version = 'ipv6' if 'ipv6' in kwargs.keys() else 'ipv4'
        keys = kwargs[version].keys()
        if 'name' not in keys or 'number' not in keys or 'value' not in keys or 'array' not in keys:
            logger.info("Please follow the json example in function define.")
            return False, {}
        json_input = {
            "dhcp_server": {
                version: {
                    "option": {
                        "object": []
                    }
                }
            }
        }
        json_input['dhcp_server'][version]['option']['object'].append(kwargs[version])
        url = f'api/sonicos/dhcp-server/{version}/option/objects'
        dhcp_resp = self.fw.api_post(url, msg, data=json_input)
        return dhcp_resp

    def get_dhcp_server_option_object(self, version=4, name=None):
        if version == 4:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv4/option/objects'
            else:
                url = 'api/sonicos/dhcp-server/ipv4/option/objects/name/' + name
        elif version == 6:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv6/option/objects'
            else:
                url = 'api/sonicos/dhcp-server/ipv6/option/objects/name/' + name
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def edit_dhcp_server_option_object(self, name, version=4, msg=False, **kwargs):
        ''' Example:
            dhcp_option = {
                "dhcp_server": {
                    "ipv6": {
                        "option": {
                            "object": [
                                {
                                    "name": "test_2",
                                    "number": 22,
                                    "value": [
                                        {
                                            "ip": "2005::4"
                                        }
                                    ],
                                    "array":False ### Can bt omitted
                                }
                            ]
                        }
                    }
                }
            }
        '''
        url_name = name.replace(' ', '%20')
        ip_version = f'ipv{version}'
        url = f'api/sonicos/dhcp-server/{ip_version}/option/objects/name/{url_name}'
        dhcp_resp = self.fw.api_put(url, msg, data=kwargs)
        return dhcp_resp

    def delete_dhcp_server_option_object(self, name, version=4, ):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/option/objects/name/' + name
        elif version == 6:
            url = 'api/sonicos/dhcp-server/ipv6/option/objects/name/' + name
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def delete_dhcp_server_option_object_msg(self, name, version=4, msg=True):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/option/objects/name/' + name
        elif version == 6:
            url = 'api/sonicos/dhcp-server/ipv6/option/objects/name/' + name
        dhcp_resp = self.fw.api_delete(url, msg)
        return dhcp_resp

    def delete_all_dhcp_server_option_object(self, version=4, msg=False, **kwargs):
        ''' Example:
            option = {
                "dhcp_server": {
                    "ipv6": {
                        "option": {
                            "object": [
                                {
                                    "name": "test4"
                                },
                                {
                                    "name": "test5"
                                },
                                {
                                    "name": "test6"
                                }
                            ]
                        }
                    }
                }
            }
        '''
        ip_version = f'ipv{version}'
        url = f'api/sonicos/dhcp-server/{ip_version}/option/objects'
        dhcp_resp = self.fw.api_delete(url, msg, data=kwargs)
        return dhcp_resp

    def add_dhcp_server_option_group(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['dhcp_server'].keys():
            url = 'api/sonicos/dhcp-server/ipv6/option/groups'
        else:
            url = 'api/sonicos/dhcp-server/ipv4/option/groups'
        dhcp_resp = self.fw.api_post(url, msg, data=json_input)
        return dhcp_resp

    def edit_ipv4_dhcp_server_option_group(self, group_name, msg=False, **kwargs):
        # {
        #     "group_name_new": "option_group_test",
        #     "option_object": [{"name": "option_43"},{"name": "option_230"}]
        # }
        json_input = self.initial_ipv4_dhcp_option_group_json
        logger.info(f'group name is:{group_name}')
        if not group_name:
            logger.error('Please specify ipv4 group name when edit ipv4 dhcp server option group.')
            return False if not msg else (False, dict)
        if 'group_name_new' in kwargs.keys():
            json_input["dhcp_server"]["ipv4"]["option"]["group"][0]["name"] = kwargs["name_new"]
        else:
            json_input["dhcp_server"]["ipv4"]["option"]["group"][0]["name"] = group_name
        if 'option_object' in kwargs.keys():
            json_input["dhcp_server"]["ipv4"]["option"]["group"][0]["option"]["object"] = kwargs["option_object"]
        url = self.url_dhcp_server_base + '/ipv4/option/groups/name/' + group_name
        logger.info(f'edit_ipv4_dhcp_server_option_group put url: {url}')
        logger.info(json_input)
        return self.fw.api_put(url, msg, data=json_input)

    def edit_ipv6_dhcp_server_option_group(self, group_name: str, msg=False, **kwargs):
        # {
        #     "group_name_new": "option_group_test",
        #     "option_object": [{"name": "option_43"},{"name": "option_230"}]
        # }
        json_input = self.initial_ipv6_dhcp_option_group_json
        if not group_name:
            logger.error('Please specify ipv6 group name when edit ipv6 dhcp server option group.')
            return False if not msg else (False, dict)
        if 'group_name_new' in kwargs.keys():
            json_input["dhcp_server"]["ipv6"]["option"]["group"][0]["name"] = kwargs["name_new"]
        else:
            json_input["dhcp_server"]["ipv6"]["option"]["group"][0]["name"] = group_name
        if 'option_object' in kwargs.keys():
            json_input["dhcp_server"]["ipv6"]["option"]["group"][0]["option"]["object"] = kwargs["option_object"]
        url = self.url_dhcp_server_base + '/ipv6/option/groups/name/' + group_name
        logger.info(f'edit_ipv6_dhcp_server_option_group put url: {url}')
        logger.info(json_input)
        return self.fw.api_put(url, msg, data=json_input)

    def get_dhcp_server_option_group(self, version=4, name=None):
        if version == 4:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv4/option/groups'
            else:
                url = 'api/sonicos/dhcp-server/ipv4/option/groups/name/' + name
        elif version == 6:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv6/option/groups'
            else:
                url = 'api/sonicos/dhcp-server/ipv6/option/groups/name/' + name
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def delete_dhcp_server_option_group(self, name, version=4, ):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/option/groups/name/' + name
        elif version == 6:
            url = 'api/sonicos/dhcp-server/ipv6/option/groups/name/' + name
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def add_dhcp_server_scope_static(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['dhcp_server'].keys():
            url = 'api/sonicos/dhcp-server/ipv6/scopes/static'
        else:
            url = 'api/sonicos/dhcp-server/ipv4/scopes/static'
        dhcp_resp = self.fw.api_post(url, msg, data=json_input)
        return dhcp_resp

    def get_dhcp_server_scope_static(self, version=4, name=None):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/scopes/static'
        elif version == 6:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv6/scopes/static'
            else:
                url = 'api/sonicos/dhcp-server/ipv6/scopes/static/name/' + name
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def delete_dhcp_server_scope_v4(self, scope, p1, p2):
        if scope == 'static':
            url = 'api/sonicos/dhcp-server/ipv4/scopes/static' + '/ip/' + p1 + '/mac/' + p2
        elif scope == 'dynamic':
            url = 'api/sonicos/dhcp-server/ipv4/scopes/dynamic' + '/start/' + p1 + '/end/' + p2
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def add_dhcp_server_scope_dynamic(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        print(json_input)
        if 'ipv6' in kwargs['dhcp_server'].keys():
            url = 'api/sonicos/dhcp-server/ipv6/scopes/dynamic'
        else:
            url = 'api/sonicos/dhcp-server/ipv4/scopes/dynamic'
        dhcp_resp = self.fw.api_post(url, msg, data=json_input)
        print(dhcp_resp)
        return dhcp_resp

    def get_dhcp_server_scope_dynamic(self, version=4, name=None):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/scopes/dynamic'
        elif version == 6:
            if name is None:
                url = 'api/sonicos/dhcp-server/ipv6/scopes/dynamic'
            else:
                url = 'api/sonicos/dhcp-server/ipv6/scopes/dynamic/name/' + name
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def del_dhcp_server_scope_dynamic(self, name, version=4):
        if version == 4:
            url = 'api/sonicos/dhcp-server/ipv4/scopes/dynamic'
        elif version == 6:
            url = 'api/sonicos/dhcp-server/ipv6/scopes/dynamic'
        if not name:
            logger.error('name should be specified when delete')
        url = url + '/name/' + name
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def delete_dhcp_server_scope_v6(self, scope, name):
        url = 'api/sonicos/dhcp-server/ipv6/scopes/' + scope + '/name/' + name
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def get_dhcp_server_leases_statistic(self, version=4):
        if version == 4:
            url = 'api/sonicos/reporting/dhcp-server/ipv4/leases/statistic'
        elif version == 6:
            url = 'api/sonicos/reporting/dhcp-server/ipv6/leases/statistic'
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def get_dhcp_server_leases(self, version=4):
        if version == 4:
            url = 'api/sonicos/reporting/dhcp-server/ipv4/leases/status'
        elif version == 6:
            url = 'api/sonicos/reporting/dhcp-server/ipv6/leases/status'
        dhcp_resp = self.fw.api_get(url)
        return dhcp_resp

    def delete_target_dhcp_server_lease(self, ip, version=4):
        if not ip:
            logger.info("the value of ip should not be empty...")
            return False
        if version == 4:
            url = 'api/sonicos/reporting/dhcp-server/ipv4/leases/status/ip/' + ip
        elif version == 6:
            url = 'api/sonicos/reporting/dhcp-server/ipv6/leases/status/ip/' + ip
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def edit_dhcp_server_scope_v4(self, scope, p1, p2, **kwargs):
        if scope == 'static':
            url = 'api/sonicos/dhcp-server/ipv4/scopes/static' + '/ip/' + p1 + '/mac/' + p2
        elif scope == 'dynamic':
            url = 'api/sonicos/dhcp-server/ipv4/scopes/dynamic' + '/start/' + p1 + '/end/' + p2
        json_input = copy.deepcopy(kwargs)
        dhcp_resp = self.fw.api_put(url, data=json_input)
        return dhcp_resp

    def edit_dhcp_server_scope_v6(self, scope, name, **kwargs):
        if scope == 'static':
            url = 'api/sonicos/dhcp-server/ipv6/scopes/static' + '/name/' + name
        elif scope == 'dynamic':
            url = 'api/sonicos/dhcp-server/ipv6/scopes/dynamic' + '/name/' + name
        json_input = copy.deepcopy(kwargs)
        dhcp_resp = self.fw.api_put(url, data=json_input)
        return dhcp_resp


class NatpolicyApi:
    '''NatpolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.init_ipv6_nat = {
            "nat_policies": [{
                "ipv6": {
                    'name': "",
                    "comment": "",
                    "destination": {"any": True},
                    "enable": True,
                    # "high_availability": {
                    # "probing": {"probe_every": 5, "reply_timeout": 1, "deactivate_after": 3, "reactivate_after": 3}},
                    'inbound': "any",
                    'outbound': "any",
                    # 'nat_method': "round-robin",
                    'priority': {'auto': True},
                    'service': {'any': True},
                    'source': {'any': True},
                    'ticket': {'tag1': "", 'tag2': "", 'tag3': ""},
                    'translated_destination': {'original': True},
                    'translated_service': {'original': True},
                    'translated_source': {'original': True}
                }
            }]
        }

    def add_ipv6_nat_rule(self, msg=False, **kwargs):
        url = 'api/sonicos/nat-policies/ipv6'
        json_input = copy.deepcopy(self.init_ipv6_nat)
        json_input["nat_policies"][0]["ipv6"].update(kwargs)
        return self.fw.api_post(url, msg, data=json_input)

    def get_nat_policy(self, version='ipv4', name=None):
        if version == 'ipv4':
            url = 'api/sonicos/nat-policies/ipv4/'
        else:
            url = 'api/sonicos/nat-policies/ipv6/'
        resp = self.fw.api_get(url)
        if name:
            for rule in resp['nat_policies']:
                if rule[version]['name'] == name:
                    uuid = rule[version]['uuid']
                    url_tmp = url + 'uuid/' + uuid
                    resp = self.fw.api_get(url_tmp)
        return resp

    def check_nat_policy_exists(self, version, **kwd):
        url1 = f'api/sonicos/nat-policies/{version}/'
        nat_policys = self.fw.api_get(url1)
        kwd_len = len(kwd)
        logger.info(kwd_len)
        rc = False
        for nat_policy in nat_policys['nat_policies']:
            flag = 0
            for key in kwd.keys():
                if nat_policy[version][key] != kwd[key]:
                    logger.info('The key is')
                    break
                elif nat_policy[version][key] == kwd[key]:
                    flag += 1
            if flag == kwd_len:
                logger.info("The nat policy is exited")
                logger.info(nat_policy)
                logger.info('--**--' * 20)
                rc = True
                break

        return rc

    def get_nat_policy_statistics(self, version=None, original_destination=None):
        if version == 'ipv4':
            url = 'api/sonicos/reporting/nat-policies/ipv4/'
        else:
            url = 'api/sonicos/reporting/nat-policies/ipv6/'
        resp = self.fw.api_get(url)
        if original_destination:
            for rule in resp:
                if rule['original_destination'] == original_destination:
                    uuid = rule['uuid']
                    logger.info(uuid)
                    url_tmp = url + 'uuid/' + uuid
                    resp = self.fw.api_get(url_tmp)
        return resp

    def edit_nat_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = 'api/sonicos/nat-policies/ipv4'
        nat_resp = self.fw.api_put(url, msg, data=json_input)
        return nat_resp

    def edit_nat_policy_v6(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = 'api/sonicos/nat-policies/ipv6'
        nat_resp = self.fw.api_put(url, msg, data=json_input)
        return nat_resp

    def add_nat_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['nat_policies'][0].keys():
            url = 'api/sonicos/nat-policies/ipv6'
        else:
            url = 'api/sonicos/nat-policies/ipv4'
        nat_resp = self.fw.api_post(url, msg, data=json_input)
        return nat_resp

    def del_nat_policy(self, name, version=4):
        if version == 4:
            url = 'api/sonicos/nat-policies/ipv4'
        else:
            url = 'api/sonicos/nat-policies/ipv6'
        url = url + '/name/' + name
        nat_resp = self.fw.api_delete(url)
        return nat_resp

    def del_nat_policy_by_name(self, name, version='ipv4', msg=False, data=None):
        if version == 'ipv4':
            url = 'api/sonicos/nat-policies/ipv4/'
        else:
            url = 'api/sonicos/nat-policies/ipv6/'
        ret = self.fw.api_get(url)
        for rule in ret['nat_policies']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                url_tmp = url + 'uuid/' + uuid
                resp = self.fw.api_delete(url_tmp)
        return resp

    def edit_nat_policy_by_name(self, name, version='ipv4', msg=False, **kwargs):
        if version == 'ipv4':
            url = 'api/sonicos/nat-policies/ipv4/'
        else:
            url = 'api/sonicos/nat-policies/ipv6/'
        nat_rules = self.get_nat_policy(version)
        try:
            for rule in nat_rules['nat_policies']:
                if rule[version]['name'] == name:
                    uuid = rule[version]['uuid']
                    logger.info(uuid)
                    url_tmp = url + 'uuid/' + uuid
                    resp = self.fw.api_get(url_tmp)
                    nat_json = copy.deepcopy(resp)
                    nat_json['nat_policies'][0][version].update(kwargs)
                    if "nat_method" in kwargs and kwargs['nat_method'] == 'symmetrical-remap':
                        if 'high_availability' in nat_json['nat_policies'][0][version].keys():
                            nat_json['nat_policies'][0][version].pop('high_availability')
                    logger.info(nat_json)
                    return self.fw.api_put(url_tmp, msg, data=nat_json)
        except Exception as e:
            logger.error(repr(e))
            return False


class NetworkMonitorApi:
    '''NetworkMonitorApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_nm_policy_base = 'api/sonicos/network-monitor/policies'
        self.url_nm_statistics = 'api/sonicos/network-monitor/statistics'
        self.initial_ipv4_nm_policy_json = {
            "network_monitors": [
                {
                    "policy": {
                        "ipv4": {
                            "name": "test",
                            "probe": {
                                "target": {
                                    # "name": "pc2_eth1"
                                },
                                "type": {
                                    # "ping": "non-explicit"
                                },
                                "interval": 5
                            },
                            "reply_timeout": 1,
                            "interval": {
                                "missed": 3,
                                "successful": 3
                            },
                            "must_respond": False,
                            "comment": ""
                        }
                    }
                }
            ]
        }

    def get_network_monitor(self, version=4, name=None):
        if version == 4:
            if name is None:
                url = 'api/sonicos/network-monitor/policies/ipv4'
            else:
                url = 'api/sonicos/network-monitor/policies/ipv4/name/' + name
        elif version == 6:
            if name is None:
                url = 'api/sonicos/network-monitor/policies/ipv6'
            else:
                url = 'api/sonicos/network-monitor/policies/ipv6/name/' + name
        monitor_resp = self.fw.api_get(url)
        return monitor_resp

    def get_network_monitor_status(self):
        url = 'api/sonicos/dynamic-file/getStatsData.json?restype=17\&datatype=1'
        monitor_resp = self.fw.api_get(url)
        return monitor_resp

    def get_network_monitor_status_by_name(self, name):
        monitor_resp = self.get_network_monitor_status()
        output = ''
        try:
            nmlist = monitor_resp['data']['netMonArray']
            if nmlist:
                for nm in nmlist:
                    if nm['policy_name'] == name:
                        output = nm
                        break
            else:
                logger.info('network monitor list is none')
        except Exception as e:
            logger.info(f'get nm status by name failed: {repr(e)}')
        return output

    def add_network_monitor(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['network_monitors'][0]['policy'].keys():
            url = 'api/sonicos/network-monitor/policies/ipv6'
        else:
            url = 'api/sonicos/network-monitor/policies/ipv4'
        monitor_resp = self.fw.api_post(url, msg, data=json_input)
        return monitor_resp

    def edit_network_monitor(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['network_monitors'][0]['policy'].keys():
            url = 'api/sonicos/network-monitor/policies/ipv6'
        else:
            url = 'api/sonicos/network-monitor/policies/ipv4'
        monitor_resp = self.fw.api_put(url, msg, data=json_input)
        return monitor_resp

    # add by JLian
    def edit_network_monitor_ipv4(self, msg=False, **kwargs):
        # ping_non_explicit = {
        #     "nm_name": "test",
        #     "nm_name_new": "test_1",
        #     "probe_type": "ping_non_explicit",
        #     "probe_target": {"name": "pc2_eth1"},
        # }
        # ping_explicit = {
        #     "nm_name": "test",
        #     "nm_name_new": "test_1",
        #     "probe_type": "ping_explicit",
        #     "probe_target": {"name": "pc2_eth1"},
        #     "next_hop": "X1 Default Gateway",
        #     "outbound_interface": "X1",
        #     "local_ip": ""       # when select tunnel interface as outbond interface,need "local_ip" but doesn't need "next_hop"
        # }
        # tcp_non_explicit = {
        #     "nm_name": "test",
        #     "nm_name_new": "test_1",
        #     "probe_type": "tcp_non_explicit",
        #     "probe_target": {"name" : "pc2_eth1"},
        #     "tcp_port": 80
        # }
        # tcp_explicit = {
        #     "nm_name": "test",
        #     "nm_name_new": "test_1",
        #     "probe_type": "tcp_explicit",
        #     "probe_target": {"name" : "pc2_eth1"},
        #     "next_hop": "X1 Default Gateway",
        #     "tcp_port": 80,
        #     "outbound_interface": "X1",
        #     "local_ip": ""       # when select tunnel interface as outbond interface,need "local_ip" but doesn't need "next_hop"
        # }
        # json_input = self.initial_ipv4_nm_policy_json
        json_input = copy.deepcopy(self.initial_ipv4_nm_policy_json)
        if "nm_name" not in kwargs.keys() and "probe_type" not in kwargs.keys() and "probe_target_name" not in kwargs.keys():
            logger.error('Please specify ipv4 nm name,probe_type and probe_target_name when edit nm policy')
            return False if not msg else (False, dict)
        if "nm_name_new" in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["name"] = kwargs["nm_name_new"]
        else:
            logger.info(f'nm name is :{kwargs["nm_name"]}')
            json_input["network_monitors"][0]["policy"]["ipv4"]["name"] = kwargs["nm_name"]
        if "probe_target" in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["target"] = kwargs["probe_target"]

        if kwargs["probe_type"] == "ping_non_explicit":
            json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"].update({"ping": "non-explicit"})

        elif kwargs["probe_type"] == "tcp_non_explicit":
            json_input["network_monitors"][0]["policy"]["ipv4"].update({"rst_as_miss": False})
            if "tcp_port" not in kwargs.keys():
                logger.error('Please specify tcp port when edit probe type to tcp_non_explicit')
            else:
                json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"].update(
                    {"tcp": {"port": kwargs["tcp_port"], "non_explicit": True}})
            if "rst_as_miss" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"]["rst_as_miss"] = kwargs["rst_as_miss"]
        elif kwargs["probe_type"] == "ping_explicit":
            json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"].update({"ping": "explicit"})
            if "outbound_interface" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"].update(
                    {"outbound_interface": kwargs["outbound_interface"]})
            else:
                logger.error('Please specify outbound interface when edit probe type to ping_explicit mode')

            if "local_ip" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"].update(
                    {"local_ip": {"name": kwargs["local_ip"]}})
            else:
                if "next_hop" in kwargs.keys():
                    json_input["network_monitors"][0]["policy"]["ipv4"].update(
                        {"next_hop": {"name": kwargs["next_hop"]}})
                logger.error(
                    'Please specify next hop when edit probe type to ping_explicit mode')
        elif kwargs["probe_type"] == "tcp_explicit":
            json_input["network_monitors"][0]["policy"]["ipv4"].update({"rst_as_miss": False})
            if "outbound_interface" in kwargs.keys() and "tcp_port" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"].update(
                    {"outbound_interface": kwargs["outbound_interface"]})
                json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["type"].update(
                    {"tcp": {"port": kwargs["tcp_port"], "explicit": True}})
            else:
                logger.error(
                    'Please specify outbound interface and tcp_port when edit probe type to ping_explicit mode')
            if "local_ip" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"].update(
                    {"local_ip": {"name": kwargs["local_ip"]}})
            else:
                if "next_hop" in kwargs.keys():
                    json_input["network_monitors"][0]["policy"]["ipv4"].update(
                        {"next_hop": {"name": kwargs["next_hop"]}})
                else:
                    logger.error(
                        'Please specify next_hop when edit probe type to tcp_explicit mode')
            if "rst_as_miss" in kwargs.keys():
                json_input["network_monitors"][0]["policy"]["ipv4"]["rst_as_miss"] = kwargs["rst_as_miss"]
        if 'probe_interval' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["probe"]["interval"] = kwargs["probe_interval"]
        if 'reply_timeout' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["reply_timeout"] = kwargs["reply_timeout"]
        if 'interval_missed' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["interval"]["missed"] = kwargs["interval_missed"]
        if 'interval_successful' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["interval"]["successful"] = kwargs[
                "interval_successful"]
        if 'must_respond' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["must_respond"] = kwargs["must_respond"]
        if 'comment' in kwargs.keys():
            json_input["network_monitors"][0]["policy"]["ipv4"]["comment"] = kwargs["comment"]
        url = self.url_nm_policy_base + '/ipv4/name/' + kwargs['nm_name']
        logger.info(f'edit_network_monitor_policy put url: {url}')
        logger.info(json_input)
        return self.fw.api_put(url, msg, data=json_input)

    def del_network_monitor(self, name, version=4, msg=False):
        if version == 4:
            url = 'api/sonicos/network-monitor/policies/ipv4'
        else:
            url = 'api/sonicos/network-monitor/policies/ipv6'
        url = url + '/name/' + name
        monitor_resp = self.fw.api_delete(url, msg)
        return monitor_resp

    def edit_network_monitor_ipv6(self, msg=False, **kwargs):
        '''
        key <name> must be in kwargs, and any other params you want to update can be included.
        param exp:
        opt = {
            "name": "test_v6_new",
            "new_name": "test_v6",
            "probe": {
                "target": {"name": "probe_wan_host"},
                "type": {"ping": "explicit"},
                "interval": 5},
            "next_hop": {"name": "probe_wan_host"},
            "outbound_interface": "X1"
        }
        # opt2 = {
        #     "name": "test_v6",
        #     "probe": {
        #         "target": {"name": "probe_wan_host"},
        #         "type": {"tcp": {"non_explicit": True, 'port': 22}},
        #         "interval": 5}
        # }
        # opt3 = {
        #     "name": "test_v6",
        #     "probe": {
        #         "target": {"name": "probe_wan_host"},
        #         "type": {"tcp": {"non_explicit": True, 'port': 22}},
        #         "interval": 5},
        #     "next_hop": {"name": "probe_wan_host"},
        #     "outbound_interface": "X1"
        # }
        # opt4 = {
        #     "name": "test_v6",
        #     "probe": {
        #         "target": {"name": "probe_wan_host"},
        #         "type": {"ping": "non-explicit"},
        #         "interval": 5}
        # }
        '''
        if "name" not in kwargs:
            logger.error('param <name> must be specified!!')
            return False
        url = self.url_nm_policy_base + '/ipv6/name/' + kwargs['name']
        json_input = self.get_network_monitor(version=6, name=kwargs['name'])
        try:
            json_input["network_monitors"][0]["policy"]["ipv6"].update(kwargs)
            if 'new_name' in kwargs:
                json_input["network_monitors"][0]["policy"]["ipv6"].pop("new_name")
                json_input["network_monitors"][0]["policy"]["ipv6"]['name'] = kwargs['new_name']
            print('*' * 20)
            print(json_input)
            print('*' * 20)
            #### note: if probe type is ping-icmp, it should be non-explicit
            # if probe type is type, it should be non_explicit
            if 'probe' in kwargs:
                if 'tcp' in kwargs['probe']['type']:
                    if 'rst_as_miss' not in json_input["network_monitors"][0]["policy"]["ipv6"]:
                        json_input["network_monitors"][0]["policy"]["ipv6"]['rst_as_miss'] = False
                        if 'rst_as_miss' in kwargs:
                            json_input["network_monitors"][0]["policy"]["ipv6"]['rst_as_miss'] = kwargs['rst_as_miss']
                    if 'non_explicit' in kwargs['probe']['type']['tcp']:
                        json_input["network_monitors"][0]["policy"]["ipv6"].pop('outbound_interface', 'no this key')
                        json_input["network_monitors"][0]["policy"]["ipv6"].pop('next_hop', 'no this key')
                if 'ping' in kwargs['probe']['type']:
                    json_input["network_monitors"][0]["policy"]["ipv6"].pop('rst_as_miss', 'no this key')
                    if 'non-explicit' in kwargs['probe']['type']['ping']:
                        json_input["network_monitors"][0]["policy"]["ipv6"].pop('outbound_interface', 'no this key')
                        json_input["network_monitors"][0]["policy"]["ipv6"].pop('next_hop', 'no this key')
            print('*' * 20)
            print(json_input)
            print('*' * 20)
            return self.fw.api_put(url, msg, data=json_input)
        except Exception as e:
            logger.error(repr(e))
            return False

    # add by JLian
    def clear_network_monitor_statistics(self):
        url = self.url_nm_statistics
        logger.info(f'clear network monitor_statistics delete url:{url}')
        monitor_resp = self.fw.api_delete(url)
        return monitor_resp


class DnsSettingsApi:
    '''DnsSettingsApi class'''
    dns_options = {
        'primary': '10.190.202.200',
        'secondary': '10.9.1.40',
        'tertiary': '144.144.144.144',
        # "inherit"   : True,
        # "preferred" : False
    }
    split_dns_default_options = {
        'domain': '',
        'ipv4': {
            'primary': '',
            'secondary': '',
            'tertiary': ''
        },
        'ipv6': {
            'primary': '',
            'secondary': '',
            'tertiary': ''
        },
        'local_interface': '',
        "manual_ttl": 0
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dns/base'
        self.split_dns_url = 'api/sonicos/dns/split-entries'
        self.initial_split_dns_json = {
            "dns": {
                "split_entry": [
                    {
                        "domain": "string",
                        "server": {
                            "ipv4": {
                                "primary": {},
                                "secondary": {},
                                "tertiary": {}
                            },
                            "ipv6": {
                                "primary": {},
                                "secondary": {},
                                "tertiary": {}
                            }
                        },
                        "local_interface": {
                            "value": "X1"
                        },
                        "manual_ttl": {
                            "value": 20
                        },
                    }
                ]
            }
        }

    def set_dns(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def set_dns_msg(self, msg=True, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def get_dns(self):
        dns_resp = self.fw.api_get(self.url)
        return dns_resp

    def edit_ipv4_dns(self, msg=False, **kwargs):
        '''Arno Hu'''
        self.options = dict(DnsSettingsApi.dns_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_ipv4_dns_json(**kwargs)
        resp = self.fw.api_put(self.url, msg, data=json_input)
        return resp

    def build_ipv4_dns_json(self, **kwargs):
        '''Arno Hu'''
        json_input = self.get_dns()
        path = json_input['dns']['server']
        path['static']['primary'] = kwargs['primary']
        path['static']['secondary'] = kwargs['secondary']
        path['static']['tertiary'] = kwargs['tertiary']
        # path['ipv6']['inherit'] = kwargs['inherit']
        # path['ipv6']['preferred'] = kwargs['preferred']
        return json_input

    def add_split_dns(self, msg=False, **kwargs):
        self.options = dict(DnsSettingsApi.split_dns_default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_split_dns(**kwargs)
        split_dns_resp = self.fw.api_post(self.split_dns_url, msg, data=json_input)
        return split_dns_resp

    def edit_split_dns(self, msg=False, **kwargs):
        url = self.split_dns_url + '/domain/' + kwargs['domain']
        self.options = dict(DnsSettingsApi.split_dns_default_options)
        self.options.update(kwargs)
        # kwargs = self.options
        json_input = self.build_json_split_dns(**self.options)
        split_dns_resp = self.fw.api_put(url, msg, data=json_input)
        return split_dns_resp

    def show_dns_proxy_entry(self, domain=None):
        url = self.split_dns_url
        if domain:
            url = self.split_dns_url + '/domain/' + domain
        show_resp = self.fw.api_get(url)
        return show_resp

    def delete_split_dns(self, domain=None):
        if not domain:
            logger.error('Please specify domain to delete.')
            return False
        del_resp = self.fw.api_delete(self.split_dns_url + '/domain/' + domain)
        return del_resp

    def show_dns_proxy_entries(self):
        url = self.split_dns_url
        show_resp = self.fw.api_get(url)
        return show_resp

    def delete_all_split_dns(self, msg=False, domain_list=None):
        split_dns_dict = {"dns": {"split_entry": []}}
        if domain_list:
            for domain in domain_list:
                split_dns_dict["dns"]["split_entry"].append({"domain": domain})
            del_resp = self.fw.api_delete(self.split_dns_url, msg, data=split_dns_dict)
            return del_resp
        else:
            logger.error('Please specify domain to delete.')
            return False

    def build_json_split_dns(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_split_dns_json)

            if 'domain' in kwargs.keys() and kwargs['domain']:
                json_input['dns']['split_entry'][0]['domain'] = kwargs['domain']
            else:
                logger.error('Please specify domain')
                return False

            if 'manual_ttl' in kwargs.keys() and kwargs['manual_ttl']:
                json_input['dns']['split_entry'][0]['manual_ttl']['value'] = kwargs['manual_ttl']

            if 'primary' in kwargs['ipv4'].keys() and kwargs['ipv4']['primary']:
                json_input['dns']['split_entry'][0]['server']['ipv4']['primary']['value'] = kwargs['ipv4']['primary']
            if 'secondary' in kwargs['ipv4'].keys() and kwargs['ipv4']['secondary']:
                json_input['dns']['split_entry'][0]['server']['ipv4']['secondary']['value'] = kwargs['ipv4'][
                    'secondary']
            if 'tertiary' in kwargs['ipv4'].keys() and kwargs['ipv4']['tertiary']:
                json_input['dns']['split_entry'][0]['server']['ipv4']['tertiary']['value'] = kwargs['ipv4']['tertiary']

            if 'primary' in kwargs['ipv6'].keys() and kwargs['ipv6']['primary']:
                json_input['dns']['split_entry'][0]['server']['ipv6']['primary']['value'] = kwargs['ipv6']['primary']
            if 'secondary' in kwargs['ipv6'].keys() and kwargs['ipv6']['secondary']:
                json_input['dns']['split_entry'][0]['server']['ipv6']['secondary']['value'] = kwargs['ipv6'][
                    'secondary']
            if 'tertiary' in kwargs['ipv6'].keys() and kwargs['ipv6']['tertiary']:
                json_input['dns']['split_entry'][0]['server']['ipv6']['tertiary']['value'] = kwargs['ipv6']['tertiary']

            if 'local_interface' in kwargs.keys() and kwargs['local_interface']:
                json_input['dns']['split_entry'][0]['local_interface']['value'] = kwargs['local_interface']

        except KeyError:
            logger.info("Error: In creating JSON for split dns")
        return json_input


class DnsProxyApi:
    '''DnsProxyApi class'''

    default_options = {
        'enable': False,
        'mode': 'ipv4-to-ipv4',
        # 'protocol': 'udp-only',
        'enforce_all_dns_requests': False,
        'dns_cache': True
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/dns-proxy/base'
        self.url_entry = 'api/sonicos/dns-proxy/cache-entries'
        self.url_cache = 'api/sonicos/dns-proxy/cache-entries'
        self.url_flush_cache = 'api/sonicos/dns-proxy/flush/cache-entries'
        self.url_report = 'api/sonicos/reporting/dns-proxy/caches'
        self.initial_dnsproxy_json = {
            "dns_proxy": {
                "enable": False,
                "mode": "ipv4-to-ipv4",
                # "protocol": "udp-only",
                "enforce_all_dns_requests": False,
                "dns_cache": True
            }
        }

        self.initial_dnsproxy_entry_json = {
            "dns_proxy": {
                "cache_entry": [
                    {
                        "domain": "string",
                        "address": {
                            "ipv4": {
                                #        "primary": {
                                #            "value": "string"
                                #         },
                                #        "secondary": {
                                #            "value": "string"
                                #         }
                            },
                            "ipv6": {
                                # "primary": {
                                #     "value": "string"
                                # },
                                # "secondary": {
                                #    "value": "string"
                                # }
                            }
                        }
                    }
                ]
            }
        }
        self.initial_delete_dnsproxy_entry_json = {
            "dns_proxy":
                {
                    "cache_entry":
                        [
                            # {"domain":"tessss"},
                            # {"domain":"teee"}
                        ]
                }
        }

    def config_dnsproxy(self, msg=False, **kwargs):
        self.options = dict(DnsProxyApi.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_dnsproxy(**kwargs)
        dns_proxy_resp = self.fw.api_put(self.url, msg, data=json_input)
        return dns_proxy_resp

    def get_dnsproxy(self, msg=False, **kwargs):
        dns_proxy_resp = self.fw.api_get(self.url)
        return dns_proxy_resp

    def build_json_dnsproxy(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_dnsproxy_json)
            if kwargs['enable']:
                json_input['dns_proxy']['enable'] = True
                json_input['dns_proxy']['mode'] = kwargs['mode']
                # json_input['dns_proxy']['protocol'] = kwargs['protocol']
                json_input['dns_proxy']['enforce_all_dns_requests'] = kwargs['enforce_all_dns_requests']
                json_input['dns_proxy']['dns_cache'] = kwargs['dns_cache']
        except KeyError:
            logger.info("Error: In creating JSON for dnsproxy")
        return json_input

    def show_dns_proxy_caches(self, domain=None):
        if domain:
            url = self.url_cache + '/domain/' + domain
        else:
            url = self.url_cache
        dnsproxy_resp = self.fw.api_get(url)
        return dnsproxy_resp

    def flush_caches(self, ip_version, msg=False, cache=None):
        if ip_version == 'ipv4' or ip_version == 'ipv6':
            url = self.url_flush_cache + '/' + ip_version
        else:
            logger.error('Please specify ip_version to ipv4 or ipv6.')
            return False
        if cache:
            url += '/' + cache
        cache_resp = self.fw.api_post(url, msg, data={})
        return cache_resp

    def add_dns_proxy_entry(self, msg=False, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_dnsproxy_entry_json)
            json_input['dns_proxy']['cache_entry'][0]['domain'] = kwargs['domain']
            if 'ipv4_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['primary'] = {}
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['primary']['value'] = kwargs[
                    'ipv4_primary']
            if 'ipv4_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['secondary'] = {}
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['secondary']['value'] = kwargs[
                    'ipv4_secondary']
            if 'ipv6_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['primary'] = {}
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['primary']['value'] = kwargs[
                    'ipv6_primary']
            if 'ipv6_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['secondary'] = {}
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['secondary']['value'] = kwargs[
                    'ipv6_secondary']
        except KeyError as reason:
            logger.info("Error: In creating JSON for webporxy")
        entry_resp = self.fw.api_post(self.url_entry, msg, data=json_input)
        return entry_resp

    def add_dns_proxy_static_entry(self, msg=False, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_dnsproxy_entry_json)
            json_input['dns_proxy']['cache_entry'][0]['domain'] = kwargs['domain']
            json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['primary'] = {}
            if 'ipv4_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['primary']['value'] = kwargs[
                    'ipv4_primary']
            json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['secondary'] = {}
            if 'ipv4_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['secondary']['value'] = kwargs[
                    'ipv4_secondary']
            json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['primary'] = {}
            if 'ipv6_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['primary']['value'] = kwargs[
                    'ipv6_primary']
            json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['secondary'] = {}
            if 'ipv6_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['secondary']['value'] = kwargs[
                    'ipv6_secondary']
        except KeyError as reason:
            logger.info("Error: In creating JSON for webporxy")
        entry_resp = self.fw.api_post(self.url_entry, msg, data=json_input)
        return entry_resp

    def edit_dns_proxy_entry(self):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_dnsproxy_entry_json)
            json_input['dns_proxy']['cache_entry'][0]['domain'] = kwargs['domain']
            if 'ipv4_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['primary']['value'] = kwargs[
                    'ipv4_primary']
            if 'ipv4_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv4']['secondary']['value'] = kwargs[
                    'ipv4_secondary']
            if 'ipv6_primary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['primary']['value'] = kwargs[
                    'ipv6_primary']
            if 'ipv6_secondary' in kwargs:
                json_input['dns_proxy']['cache_entry'][0]['address']['ipv6']['secondary']['value'] = kwargs[
                    'ipv6_secondary']
        except KeyError as reason:
            logger.info("Error: In creating JSON for webporxy")
        entry_resp = self.fw.api_put(self.url_entry, msg, data=json_input)
        return entry_resp

    def delete_dns_proxy_entry(self, domain=None):
        if not domain:
            logger.error('Please specify domain to delete.')
            return False
        del_resp = self.fw.api_delete(self.url_entry + '/' + domain)
        return del_resp

    def delete_static_dns_cache_entry(self, domain=[], msg=False):
        json_input = copy.deepcopy(self.initial_delete_dnsproxy_entry_json)
        for domain_name in domain:
            json_input['dns_proxy']['cache_entry'].append({"domain": domain_name})
        resp = self.fw.api_delete(self.url_entry, msg, data=json_input)
        return resp

    def show_dns_proxy_entry(self, domain=None):
        show_resp = self.fw.api_get(self.url_entry)
        return show_resp

    # added by Celia
    def show_dns_proxy_caches_report(self, version='ipv4'):
        if version != 'ipv4' and version != 'ipv6':
            logger.error("Version must be 'ipv4' or 'ipv6'!!")
            return False
        url = self.url_report + f'/{version}'
        report_resp = self.fw.api_get(url)
        return report_resp


class RoutePolicyApi:
    '''RoutePolicyApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_v4 = 'api/sonicos/route-policies/ipv4'
        self.url_v6 = 'api/sonicos/route-policies/ipv6'

    def show_route_policy(self, version=None, uuid=None):
        if version.lower() == 'ipv4':
            url = self.url_v4
        elif version.lower() == 'ipv6':
            url = self.url_v6
        else:
            logger.error('Please specified version to ipv4 or ipv6.')
            return False
        if uuid:
            url += '/uuid' + uuid
        show_resp = self.fw.api_get(url)
        return show_resp

    def show_route_policy_by_name(self, name, version='ipv4'):
        if version.lower() == 'ipv4':
            url = self.url_v4
        elif version.lower() == 'ipv6':
            url = self.url_v6
        else:
            logger.error('Please specified version to ipv4 or ipv6.')
            return False
        ret = self.fw.api_get(url)
        for rule in ret['route_policies']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                url_tmp = url + '/uuid/' + uuid
                resp = self.fw.api_get(url_tmp)
        return resp

    def show_route_policy_system(self, version='ipv4'):
        if version.lower() == 'ipv4':
            url = 'api/sonicos/reporting/route-policies/ipv4/system'
        elif version.lower() == 'ipv6':
            url = 'api/sonicos/reporting/route-policies/ipv6/system'
        else:
            logger.error('Please specified version to ipv4 or ipv6.')
            return False
        resp = self.fw.api_get(url)
        return resp

    def show_route_policy_status(self, name, version='ipv4'):
        if version.lower() == 'ipv4':
            url = self.url_v4
        elif version.lower() == 'ipv6':
            url = self.url_v6
        else:
            logger.error('Please specified version to ipv4 or ipv6.')
            return False
        ret = self.fw.api_get(url)
        uuid = None
        for rule in ret['route_policies']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                break

        self.fw.headers = OrderedDict([('Accept', 'application/json'),
                                       ('Content-Type', 'application/json'),
                                       ('Accept-Encoding', 'application/json'),
                                       ('charset', 'UTF-8'),
                                       ('X-SNWL-API-Scope', 'extended')])
        if uuid:
            url = 'api/sonicos/dynamic-file/getPolicyStats.json?type=4'
            resp = self.fw.api_get(url)
            try:
                policies = re.split('\|', resp['entries'])
                pattern = uuid + '.*,(\d)'
                for policy in policies:
                    match = re.search(pattern, policy)
                    if match:
                        status = match.group(1)
                        if status == '1':
                            status = 'active'
                        elif status == '0':
                            status = 'inactive'
                            break
            except:
                logger.error(f'Fail to get status for policy with name {name} and uuid {uuid}')
                status = 'Not-get'
        else:
            logger.error('Fail to get status for policy with name {name}')
            status = 'Not-get'
        return status

    def add_route_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if 'ipv6' in kwargs['route_policies'][0].keys():
            url = self.url_v6
        else:
            url = self.url_v4
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def del_route_policy_by_uuid(self, uuid, version='v4'):
        if version == 'v4':
            url = self.url_v4
            version = 'ipv4'
        else:
            url = self.url_v6
            version = 'ipv6'
        url_tmp = url + '/uuid/' + uuid
        resp = self.fw.api_delete(url_tmp)
        return resp

    def del_route_policy_by_name(self, name, version='ipv4', msg=False, data=None):
        if version.lower() == 'ipv4':
            url = self.url_v4
        elif version.lower() == 'ipv6':
            url = self.url_v6
        else:
            logger.error('Please specified version to ipv4 or ipv6.')
            return False
        ret = self.fw.api_get(url)
        resp = False
        for rule in ret['route_policies']:
            if rule[version]['name'] == name:
                uuid = rule[version]['uuid']
                url_tmp = url + '/uuid/' + uuid
                resp = self.fw.api_delete(url_tmp)
        if not resp:
            logger.error('No this route policy.')
        return resp

    def get_default_route_policy_v6(self, uuid=None):
        """get default ipv6 route rule"""
        url_v6 = 'api/sonicos/reporting/route-policies/ipv6/system'
        if uuid:
            url_v6 += '/uuid' + uuid
        resp = self.fw.api_get(url_v6)
        return resp


class IpHelperApi:
    '''IpHelperApi class   by: jxia'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/ip-helper/'
        self.initial_protocol_json = {
            "name": None
            , "enable": True

            , "port1": {
                "value": None
            }

            , "port2": {
                "value": None
            }

            , "timeout": None
            , "mode": "broadcast"
            , "source_translation": True
            , "raw": False
        }
        self.initial_iphelper_protocol_json = {
            "ip_helper": {
                "protocol": [
                    {
                        "enable": True,
                        "mode": "broadcast",
                        "name": None,
                        "port1": {
                            "value": None
                        },
                        "port2": {
                            "value": None
                        },
                        "raw": False,
                        "source_translation": True,
                        "timeout": None
                    }
                ]
            }
        }
        self.initial_iphelper_policy_json = {
            "protocol": None,
            "source": {
                # "name": None,
                "interface": None
            }

            , "destination": {
                "name": None,
                # "interface": None
            }

            , "enable": True
            , "comment": "test"
        }

    def enable_iphelper(self, msg=False):
        logger.info("***         Enable IP Helper        ***")
        url = self.url + 'base'
        iphelper_setting_json = {
            "ip_helper": {
                "enable": True
            }
        }
        rc = self.fw.api_put(url, msg, data=iphelper_setting_json)
        return rc

    def get_iphelper_settings(self):
        url = self.url + 'base'
        response = self.fw.api_get(url)
        return response

    def disable_iphelper(self, msg=False):
        logger.info("***         Disable IP Helper        ***")
        url = self.url + 'base'
        iphelper_setting_json = {
            "ip_helper": {
                "enable": False
            }
        }

        rc = self.fw.api_put(url, msg, data=iphelper_setting_json)
        return rc

    def add_protocol(self, msg=False, **kwargs):
        # usr_protocol = {
        #     'name': 'TEST',
        #     'port1': 959,
        #     'port2': 277,
        #     'timeout': 30,
        #     'enable': True/False
        # }
        url = self.url + 'protocols'
        json = copy.deepcopy(self.initial_iphelper_protocol_json)
        if 'name' not in kwargs.keys() and 'port1' not in kwargs.keys() and 'port2' not in kwargs.keys() and 'timeout' not in kwargs.keys():
            logger.info("Key Error! Please check json, which must contain: name, port1, port2, timeout")
        json['ip_helper']['protocol'][0]['name'] = kwargs['name']
        json['ip_helper']['protocol'][0]['port1']['value'] = kwargs['port1']
        json['ip_helper']['protocol'][0]['port2']['value'] = kwargs['port2']
        json['ip_helper']['protocol'][0]['timeout'] = kwargs['timeout']
        if 'enable' in kwargs.keys():
            json['ip_helper']['protocol'][0]['enable'] = kwargs['enable']
        logger.info(json)
        rc = self.fw.api_post(url, msg, data=json)
        return rc

    def edit_protocol(self, name, msg=False, **kwargs):
        url = self.url + 'protocols/name/' + name
        json_input = self.get_protocol(protocol=name)
        logger.info(json_input)

        if 'port1' in kwargs.keys():
            json_input["ip_helper"]['protocol'][0]['port1']['value'] = kwargs['port1']
        if 'port2' in kwargs.keys():
            json_input["ip_helper"]['protocol'][0]['port2']['value'] = kwargs['port2']
        if 'timeout' in kwargs.keys():
            json_input["ip_helper"]['protocol'][0]['timeout'] = kwargs['timeout']
        if 'enable' in kwargs.keys():
            json_input["ip_helper"]['protocol'][0]['enable'] = kwargs['enable']
        logger.info(json_input)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def del_protocol(self, name):
        del_url = self.url + 'protocols'
        data = {
            "ip_helper": {
                "protocol": [{
                    "name": name
                }]
            }
        }
        response = self.fw.api_delete(del_url, data=data)
        return response

    def get_protocol(self, protocol=None):
        # iphelper.get_protocol(protocol='DHCP')
        if protocol == 'All':  # show all protocols
            url = self.url + 'protocols'
            return self.fw.api_get(url)
        url = self.url + 'protocols/name/' + protocol.upper()
        logger.info("Get protocol from url: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output

    def get_policy(self):
        url = self.url + 'policies'
        logger.info("Get policy protocol from url: {}".format(url))
        json_output = self.fw.api_get(url)
        return json_output

    def add_iphelper_policy(self, msg=False, **kwargs):

        if 'protocol' not in kwargs.keys() and ('source' not in kwargs.keys() or 'src' not in kwargs.keys()) and (
                'destination' not in kwargs.keys() or 'dsn' not in kwargs.keys()):
            logger.info("Key Error! Please check json, which must contain: protocol, src as source, dsn as destination")
            return False
        url = self.url + 'policies'
        json_input = self.get_policy()
        json = copy.deepcopy(self.initial_iphelper_policy_json)
        json['protocol'] = kwargs['protocol']
        if "src" in kwargs.keys():
            # just for suite IP_Helper and IP_Helper_v3
            json['source']['interface'] = kwargs['src']
        elif 'source' in kwargs.keys():
            json['source'] = kwargs['source']
        if "dsn" in kwargs.keys():
            # just for suite IP_Helper and IP_Helper_v3
            json['destination']['name'] = kwargs['dsn']
        elif 'destination' in kwargs.keys():
            json['destination'] = kwargs['destination']
        if 'enable' in kwargs.keys():
            json['enable'] = kwargs['enable']
        if 'policy' not in json_input['ip_helper']:
            policy_json = {"policy": []}
            json_input['ip_helper'].update(policy_json)
            json_input["ip_helper"]["policy"].append(json)
        else:
            json_input["ip_helper"]["policy"].append(json)
        logger.info(json_input)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def edit_iphelper_policy(self, msg=False, **kwargs):
        # iphelper_dhcp_opt = {
        #     'policy': 'DHCP',
        #     'enable': False
        # }
        url = self.url + 'policies'
        if 'policy' not in kwargs.keys() and 'enable' not in kwargs.keys():
            logger.info("Key Error! Please check json, which must contain: policy, enable")
            return False
        json_input = self.get_policy()
        logger.info(json_input)
        for policy in json_input['ip_helper']['policy']:
            if policy['protocol'] == kwargs['policy'].upper():
                policy['enable'] = kwargs['enable']
                logger.info(policy)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def change_iphelper_policy(self, msg=False, **kwargs):
        # iphelper_dhcp_opt = {
        #     'policy': 'DHCP',
        #     'enable': False,
        #      'src': 'X0',
        #      'dst': 'test_ao'
        # }
        url = self.url + 'policies'
        if 'policy' not in kwargs.keys() and 'enable' not in kwargs.keys():
            logger.info("Key Error! Please check json, which must contain: policy, enable")
            return False
        json_input = self.get_policy()
        logger.info(json_input)
        for policy in json_input['ip_helper']['policy']:
            if policy['protocol'] == kwargs['policy'].upper():
                policy['enable'] = kwargs['enable']
                if kwargs['src']:
                    policy['source']['interface'] = kwargs['src'].upper()
                if kwargs['dst']:
                    policy['destination']['name'] = kwargs['dst']
                logger.info(policy)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def edit_iphelper_protocol(self, msg=False, **kwargs):
        # dhcp_protocol_opt = {
        #     'protocol': 'DHCP',
        #     'enable': True/False
        # }
        if 'protocol' not in kwargs.keys() and 'enable' not in kwargs.keys():
            logger.info("Key Error! Please check json, which must contain: protocol, enable")
            return False
        url = self.url + 'protocols/name/' + kwargs['protocol'].upper()
        json_input = {
            "ip_helper": {
                "protocol": [{
                    "enable": False,
                    "name": None
                }]
            }
        }
        json_input["ip_helper"]['protocol'][0]['name'] = kwargs['protocol'].upper()
        json_input["ip_helper"]['protocol'][0]['enable'] = kwargs['enable']
        logger.info(json_input)
        rc = self.fw.api_put(url, msg, data=json_input)
        return rc

    def delete_iphelper_policy(self, **kwargs):

        if 'protocol' not in kwargs.keys() and 'source' not in kwargs.keys():
            logger.info("Key Error! Json needs 'protocol' and 'source'")
            return False
        if isinstance(kwargs['source'], dict):
            if 'interface' in (kwargs['source']).keys():
                src_url = '/source/interface/' + kwargs['source']['interface']
            elif 'name' in (kwargs['source']).keys():
                src_url = '/source/name/' + kwargs['source']['name']
        else:
            ##just for suite IP_Helper and IP_Helper_v3
            src_url = '/source/interface/' + kwargs['source']
        url = 'api/sonicos/ip-helper/policies/protocol/' + kwargs['protocol'] + src_url
        rc = self.fw.api_delete(url)
        return rc

    def add_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = self.url + 'policies'
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def del_policy(self, **kwargs):
        if 'zone' in kwargs.keys():
            url = 'api/sonicos/ip-helper/policies/protocol/' + kwargs['protocol'].upper() + '/source/zone/' + kwargs[
                'zone'].upper()
        if 'interface' in kwargs.keys():
            url = 'api/sonicos/ip-helper/policies/protocol/' + kwargs['protocol'].upper() + '/source/interface/' + \
                  kwargs['interface'].upper()
        rc = self.fw.api_delete(url)
        return rc

    def get_dhcpv6_relay_lease(self):
        url = 'api/sonicos/reporting/ip-helper/dhcpv6-relay-leases'
        logger.info("Get dhcpv6 relay lease from url: {}".format(url))
        return self.fw.api_get(url)


class ArpApi:

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/'
        self.initial_arp_json = {
            "arp": {
                "entry": [
                    {
                        "ip": None,
                        "mac": None,
                        "interface": None,
                        "publish": False,
                        "bind_mac": False,
                        "dynamic": False
                    }
                ]
            }
        }

        self.default_add_options = {
            'ip': '',
            'mac': '',
            'interface': '',
            'publish': False,
            'bind_mac': False,
            "dynamic": False,
        }

        self.default_edit_options = {
            'raw_ip': '',
            'raw_mac': '',
            'raw_interface': '',
            'raw_publish': False,
            'raw_bind_mac': False,
            "raw_dynamic": False,
            'ip': '',
            'mac': '',
            'interface': '',
            'publish': False,
            'bind_mac': False,
            "dynamic": False
        }

    def get_arp_entries(self):
        url = 'api/sonicos/arp/entries'
        resp = self.fw.api_get(url)
        return resp

    def add_arp_entry(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        url = 'api/sonicos/arp/entries'
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def get_arp_entry(self, ip=None, mac=None, interface=None):
        if not ip or not mac or not interface:
            logger.info("Please specify ip, mac and interface to get.")
            return False
        url = 'api/sonicos/arp/entries/ip/' + ip + '/mac/' + mac + '/interface/' + interface
        get_resp = self.fw.api_get(url)
        return get_resp

    def delete_arp_entry(self, ip=None, mac=None, interface=None):
        if not ip or not mac or not interface:
            logger.info("Please specify ip, mac and interface to delete.")
            return False
        url = 'api/sonicos/arp/entries/ip/' + ip + '/mac/' + mac + '/interface/' + interface
        del_resp = self.fw.api_delete(url)
        return del_resp

    def add_static_arp(self, **kwargs):
        self.options = dict(self.default_add_options)
        self.options.update(kwargs)
        kwargs = self.options
        self.add_url = self.url + "arp/entries"
        json_input = self.build_json_arp(kwargs['ip'],
                                         kwargs['mac'],
                                         kwargs['interface'],
                                         kwargs['publish'],
                                         kwargs['bind_mac'],
                                         kwargs['dynamic'])
        arp_resp = self.fw.api_post(self.add_url, data=json_input)
        return arp_resp

    def del_static_arp(self, **kwargs):
        self.options = dict(self.default_add_options)
        self.options.update(kwargs)
        kwargs = self.options
        self.add_url = self.url + "arp/entries"
        json_input = self.build_json_arp(kwargs['ip'],
                                         kwargs['mac'],
                                         kwargs['interface'],
                                         kwargs['publish'],
                                         kwargs['bind_mac'],
                                         kwargs['dynamic'])
        arp_resp = self.fw.api_delete(self.add_url, data=json_input)
        return arp_resp

    def edit_static_arp(self, **kwargs):
        self.options = dict(self.default_edit_options)
        self.options.update(kwargs)
        kwargs = self.options
        self.edit_url = (self.url + "arp/entries/" + "ip/"
                         + kwargs['raw_ip']
                         + "/mac/"
                         + kwargs['raw_mac']
                         + "/interface/"
                         + kwargs['raw_interface'])
        json_input = self.build_json_arp(kwargs['ip'],
                                         kwargs['mac'],
                                         kwargs['interface'],
                                         kwargs['publish'],
                                         kwargs['bind_mac'],
                                         kwargs['dynamic'])
        arp_resp = self.fw.api_put(self.edit_url, data=json_input)
        return arp_resp

    def build_json_arp(self, ip, mac, interface, publish, bind_mac, dynamic):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_arp_json)
            json_input['arp']['entry'][0]['ip'] = ip
            json_input['arp']['entry'][0]['mac'] = mac
            json_input['arp']['entry'][0]['interface'] = interface
            json_input['arp']['entry'][0]['publish'] = publish
            json_input['arp']['entry'][0]['bind_mac'] = bind_mac
            json_input['arp']['entry'][0]['dynamic'] = dynamic
            logger.info("arp json obtained")
            logger.info(json_input)
        except KeyError:
            logger.info("Error: In creating JSON for ARP")
        return json_input

    def get_arp_base(self):
        arp_resp = self.fw.api_get(self.url + "arp/base")
        return arp_resp

    def show_static_arp_entries(self):
        self.entries_url = self.url + "arp/entries"
        entries_resp = self.fw.api_get(self.entries_url)
        return entries_resp

    def show_arp_caches(self):
        cache_resp = self.fw.api_get(self.url + "reporting/arp/caches")
        return cache_resp

    def show_arp_statistics(self):
        rc = self.fw.api_get(self.url + "reporting/arp/statistics")
        return rc

    def delete_arp_cache(self, ip, interface):
        url_delete = self.url + f"reporting/arp/cache/ip/{ip}/interface/{interface}"
        response = self.fw.api_delete(url_delete)
        return response

    def delete_arp_caches(self, nologin=False):
        cache_resp = self.fw.api_delete(self.url + "reporting/arp/caches", nologin=nologin)
        return cache_resp

    def arp_setting(self, msg=False, timeout=10, glean=True):
        json_input = {"arp": {"timeout": timeout, "glean": glean}}
        resp = self.fw.api_put(self.url + "arp/base", msg, data=json_input)
        return resp

    def get_arp_base(self):
        arp_resp = self.fw.api_get(self.url + "arp/base")
        return arp_resp


class MacIPAntiSpoofApi:

    def __init__(self, fw):
        self.fw = fw

    def edit_mac_anti_spoof_settings(self, msg=False, version=4, name=None, **kwargs):
        json_put = copy.deepcopy(kwargs)
        if version == 4:
            if name is None:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv4/interfaces'
            else:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv4/interfaces/name/' + name
        elif version == 6:
            if name is None:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv6/interfaces'
            else:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv6/interfaces/name/' + name
        resp = self.fw.api_put(url, msg, data=json_put)
        return resp

    def get_mac_anti_spoof_settings(self, version=4, name=None):
        if version == 4:
            if name is None:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv4/interfaces'
            else:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv4/interfaces/name/' + name
        elif version == 6:
            if name is None:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv6/interfaces'
            else:
                url = 'api/sonicos/mac-ip-anti-spoof/ipv6/interfaces/name/' + name
        resp = self.fw.api_get(url)
        return resp

    def get_reporting_cache(self, version=4):
        if version == 4:
            url = 'api/sonicos/reporting/mac-ip-anti-spoof/cache/ipv4'
        elif version == 6:
            url = 'api/sonicos/reporting/mac-ip-anti-spoof/cache/ipv6'
        resp = self.fw.api_get(url)
        return resp

    def add_anti_spoof_cache(self, msg=False, version=4, **kwargs):
        json_input = copy.deepcopy(kwargs)
        if version == 4:
            url = 'api/sonicos/mac-ip-anti-spoof/ipv4/cache/entries'
        elif version == 6:
            url = 'api/sonicos/mac-ip-anti-spoof/ipv6/cache/entries'
        resp = self.fw.api_post(url, msg, data=json_input)
        return resp

    def delete_anti_spoof_cache(self, ip=None, mac=None, interface=None, version='ipv4'):
        if not ip or not mac or not interface:
            logger.info("Please specify ip, mac and interface to delete.")
            return False
        url = 'api/sonicos/mac-ip-anti-spoof/' + version + '/cache/entries/ip/' \
              + ip + '/mac/' + mac + '/interface/' + interface
        del_resp = self.fw.api_delete(url)
        return del_resp


class NeighborDiscoveryApi:
    '''NeighborDiscoveryApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_setting = 'api/sonicos/ndp/base'
        self.url_cache = 'api/sonicos/reporting/ndp/cache'
        self.url_entry = 'api/sonicos/ndp/entries'
        self.url_cache_entry = 'api/sonicos/ndp/cache/entries'
        self.initial_ndp_entry_json = {"ndp":
            {"entry":
                [
                    {
                        "ip": "",
                        "mac": "",
                        "interface": ""
                    }
                ]
            }
        }

    def add_static_entry(self, msg=False, **kwargs):
        if 'ip' not in kwargs or 'mac' not in kwargs or 'interface' not in kwargs:
            logger.error('Please specify ip,mac,interface when add entry.')
            return False
        json_input = self.build_ndp_json(**kwargs)
        resp = self.fw.api_post(self.url_entry, msg, data=json_input)
        return resp

    def edit_static_entry(self, msg=False, **kwargs):
        if 'ip_old' not in kwargs or 'mac_old' not in kwargs or 'interface_old' not in kwargs:
            logger.error('Please specify ip_old,mac_old,interface_old when edit entry.')
            return False
        if 'ip' not in kwargs:
            kwargs['ip'] = kwargs['ip_old']
        if 'ip' not in kwargs:
            kwargs['ip'] = kwargs['ip_old']
        if 'ip' not in kwargs:
            kwargs['ip'] = kwargs['ip_old']
        json_input = self.build_ndp_json(**kwargs)

        url = f"{self.url_entry}/ip/{kwargs['ip_old']}/mac/{kwargs['mac_old']}/interface/{kwargs['interface_old']}"
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def delete_static_entry(self, msg=False, **kwargs):
        if 'ip' not in kwargs or 'mac' not in kwargs or 'interface' not in kwargs:
            logger.error('Please specify ip,mac,interface when add entry.')
            return False
        json_input = self.build_ndp_json(**kwargs)
        resp = self.fw.api_delete(self.url_entry, msg, data=json_input)
        return resp

    # add by JLian
    def del_static_ndp_entries_by_ip(self, ip_address_list, msg=False):
        output = self.show_static_entry()
        new_ndp_list = []
        try:
            fw_ndp_entries = output['ndp']['entry']
            logger.info(fw_ndp_entries)
            for ip_address in ip_address_list:
                if ip_address in str(fw_ndp_entries):
                    for fw_ndp_entry in fw_ndp_entries:
                        if fw_ndp_entry['ip'] == ip_address:
                            new_ndp_list.append(fw_ndp_entry)
                else:
                    logger.info(f'{ip_address} not in ndp table,please check...')
                    return False if not msg else (False, {})
            if not new_ndp_list:
                return False if not msg else (False, {})
            json_input = {'ndp': {'entry': new_ndp_list}}
            del_resp = self.fw.api_delete(self.url_entry, msg, data=json_input)
            return del_resp
        except Exception as e:
            logger.error(repr(e))
            return False if not msg else (False, {})

    def build_ndp_json(self, **kwargs):
        json_input = self.initial_ndp_entry_json
        json_input['ndp']['entry'][0]['ip'] = kwargs['ip']
        json_input['ndp']['entry'][0]['mac'] = kwargs['mac'].replace(':', '')
        json_input['ndp']['entry'][0]['interface'] = kwargs['interface']
        return json_input

    def show_static_entry(self):
        entry_resp = self.fw.api_get(self.url_entry)
        return entry_resp

    def show_NDP_cache(self):
        cache_resp = self.fw.api_get(self.url_cache)
        return cache_resp

    def NDP_setting(self, msg=False, time=30):
        json_input = {
            "ndp":
                {
                    "reachable_time": {"value": int(time)}
                }
        }
        resp = self.fw.api_put(self.url_setting, msg, data=json_input)
        return resp

    def flush_NDP_caches(self):
        resp = self.fw.api_delete(self.url_cache_entry)
        return resp


class DDNSApi:
    '''DDNSApi class'''
    default_options = {
        'profile_name': '',
        'enable': True,
        'use_online': True,
        'provider': 'dyn',
        'user_name': '',
        'password': '',
        'domain': '',
        # 'service_type':'dynamic',
        'bound_to': {'Any': True},
        'online_settings': {'detect': True},
        'offline_settings': {'do_nothing': True}
    }

    def __init__(self, fw):
        self.fw = fw
        self.url_ddns = 'api/sonicos/dynamic-dns/profiles'
        self.reporting_url = 'api/sonicos/reporting/dynamic-dns/profiles'
        self.initial_ddns_json_v4 = {
            "dynamic_dnss":
                [
                    {
                        "profile": {
                            "ipv4":
                                {
                                    "profile_name": "TEST",
                                    "enable": True,
                                    "use_online": True,
                                    "provider": "dyn",  # dyn,changeip,noip
                                    "user_name": "",
                                    "password": "",
                                    "domain": "",
                                    # "service_type":"dynamic",
                                    "bound_to": {"interface": "X1"},
                                    "online_settings": {},  # detect:true,set_to_wan:true,manual:1.1.1.1
                                    "offline_settings": {}
                                    # do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
                                }
                        }
                    }
                ]
        }
        self.initial_ddns_json_v6 = {
            "dynamic_dnss":
                [
                    {
                        "profile": {
                            "ipv6":
                                {
                                    "profile_name": "TEST",
                                    "enable": True,
                                    "use_online": True,
                                    "provider": "dyn",  # dyn,changeip,noip
                                    "user_name": "",
                                    "password": "",
                                    "domain": "",
                                    "service_type": "dynamic",
                                    "bound_to": {"interface": "X1"},
                                    "online_settings": {},  # detect:true,set_to_wan:true,manual:1.1.1.1
                                    "offline_settings": {}
                                    # do_nothing:true,use_previous:true,make_host_unknown:true,manual:1.1.1.1
                                }
                        }
                    }
                ]
        }

    def show_ddns_profiles_ipv4(self):
        url = self.url_ddns + '/' + 'ipv4'
        response = self.fw.api_get(url)
        return response

    def add_ddns_profile(self, msg=False, **kwargs):  # please use edit_ddns_profile_name below if change profile name
        self.options = dict(DDNSApi.default_options)
        self.options.update(kwargs)
        json_input = self.build_ddns_json(msg, **kwargs)
        resp = self.fw.api_post(self.url_ddns + '/' + kwargs['version'], msg, data=json_input)
        return resp

    def edit_ddns_profile(self, msg=False, **kwargs):
        url = self.url_ddns + '/' + kwargs['version'] + '/name/' + kwargs['profile_name']
        self.options = dict(DDNSApi.default_options)
        self.options.update(kwargs)
        json_input = self.build_ddns_json(msg, **kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def delete_all_ddns_profile(self, msg=False, version='ipv4', name_list=[]):
        url = self.url_ddns + '/' + version
        json_input = {
            "dynamic_dnss":
                [
                    #    {"profile":{"ipv4":{"profile_name":"test"}}},
                    #    {"profile":{"ipv4":{"profile_name":"test1"}}}
                ]
        }
        for name in name_list:
            json_input['dynamic_dnss'].append({"profile": {"ipv4": {"profile_name": name}}})
        resp = self.fw.api_delete(url, msg, data=json_input)
        return resp

    def delete_ddns_profile(self, msg=False, version='ipv4', name=None):
        url = self.url_ddns + '/' + version + '/name/' + name
        resp = self.fw.api_delete(url)
        return resp

    def build_ddns_json(self, msg=False, **kwargs):
        json_input = {}
        ver = kwargs['version']
        try:
            if ver == 'ipv4':
                json_input = copy.deepcopy(self.initial_ddns_json_v4)
            elif ver == 'ipv6':
                json_input = copy.deepcopy(self.initial_ddns_json_v6)
            else:
                logger.error('Please specify version to ipv4 or ipv6.')
                return {}
            json_input['dynamic_dnss'][0]['profile'][ver]['profile_name'] = kwargs['profile_name']
            json_input['dynamic_dnss'][0]['profile'][ver]['enable'] = kwargs['enable']
            json_input['dynamic_dnss'][0]['profile'][ver]['use_online'] = kwargs['use_online']
            json_input['dynamic_dnss'][0]['profile'][ver]['provider'] = kwargs['provider']
            json_input['dynamic_dnss'][0]['profile'][ver]['user_name'] = kwargs['user_name']
            json_input['dynamic_dnss'][0]['profile'][ver]['password'] = kwargs['password']
            json_input['dynamic_dnss'][0]['profile'][ver]['domain'] = kwargs['domain']
            json_input['dynamic_dnss'][0]['profile'][ver]['bound_to'] = kwargs['bound_to']
            json_input['dynamic_dnss'][0]['profile'][ver]['online_settings'] = kwargs['online_settings']
            json_input['dynamic_dnss'][0]['profile'][ver]['offline_settings'] = kwargs['offline_settings']
            if 'service_type' in kwargs:
                json_input['dynamic_dnss'][0]['profile'][ver]['service_type'] = kwargs['service_type']
            logger.info("ddns json obtained")
            logger.info(json_input)
        except KeyError as e:
            logger.error("Error: In creating JSON for ddns {}".format(e))
        return json_input

    def show_ddns_profile(self, version='ipv4', name=None):
        url = self.url_ddns + '/' + version + '/name/' + name
        resp = self.fw.api_get(url)
        return resp

    def get_ddns_profile_reporting(self, version='ipv4', name=None):
        url = self.reporting_url + '/' + version + '/name/' + name
        resp = self.fw.api_get(url)
        return resp

    def edit_ddns_profile_name(self, prof_name=[], msg=False, **kwargs):
        ver = kwargs['version']
        prof_name_old = self.show_ddns_profile(name=prof_name)['dynamic_dnss'][0]['profile'][ver]['profile_name']
        url = self.url_ddns + '/' + kwargs['version'] + '/name/' + str(prof_name_old)
        self.options = dict(DDNSApi.default_options)
        self.options.update(kwargs)
        json_input = self.build_ddns_json(msg, **kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp


class DNSSecurityApi:
    '''DNSSecurityApi class'''

    def __init__(self, fw):
        self.fw = fw
        self.url_dns_sinkhole = 'api/sonicos/dns-security/dns-sinkhole/base'
        self.url_dns_custom = 'api/sonicos/dns-security/dns-sinkhole/custom-malicious-entries'
        self.url_dns_white = 'api/sonicos/dns-security/dns-sinkhole/white-list-entries'
        self.url_dns_detect = 'api/sonicos/dns-security/dns-tunnel/base'
        self.url_dns_tunnel = 'api/sonicos/reporting/dns-security/tunnel-clients'
        self.url_dns_tunnel_white = 'api/sonicos/dns-security/dns-tunnel/white-list-entries'
        self.url_dns_custom_domains = 'api/sonicos/dns-security/dns-filtering/custom-domains'
        self.url_dns_tunnel_client = 'api/sonicos/dns-security/dns-tunnel/block'

    def add_dns_custom_domain(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.url_dns_custom_domains, msg, data=json_input)
        return resp

    def show_dns_custom_domain(self):
        resp = self.fw.api_get(self.url_dns_custom_domains)
        return resp

    def del_custom_domain(self, domainname, msg=False):
        if domainname:
            url = str(self.url_dns_custom_domains) + '/name/' + domainname
            resp = self.fw.api_delete(url, msg)
            return resp
        else:
            logger.error("Pls enter custom domain name")

    def delete_multiple_custom_domain(self, msg=False, domain_list=[]):
        """
        Args:
            domain_list (list, necessary): domain name list to be deleted. Example: ["a.com", "b.com", "tt.com"].  Defaults to null.
        """
        if domain_list:
            json_input = {"dns_security": {"dns_filtering": {"custom_domain": []}}}
            path = json_input['dns_security']["dns_filtering"]['custom_domain']
            for domain in domain_list:
                path.append({"domain": domain})
            json_input['dns_security']["dns_filtering"]['custom_domain'] = path
            if msg:
                (resp, msg) = self.fw.api_delete(self.url_dns_custom_domains, msg=True, data=json_input)
                return (resp, msg)
            resp = self.fw.api_delete(self.url_dns_custom_domains, data=json_input)
            return resp
        else:
            logger.error("Please enter valid custom domain name list!!")
        return False

    def edit_dns_custom_domain(self, msg=False, domain='', **kwargs):
        """
        Args:
            domain (string, necessary): Specific domain to edit. Defaults to null.
            kwargs (dict, necessary): Keys to edit. Include at least one key, 'new-name'(just for negative test), 'category'. Example: {"new-name":"adult.com", "category": "1. Adult"}
        """
        if domain and kwargs:
            url = f"{self.url_dns_custom_domains}/name/{domain}"
            json_input = self.fw.api_get(url)
            # json_example = {"dns_security":{"dns_filtering":{"custom_domain":[{"domain": "*.ea.com", "category": "1. Adult"}]}}}
            if json_input:
                try:
                    if 'new-name' in kwargs.keys():
                        json_input["dns_security"]["dns_filtering"]["custom_domain"][0]["domain"] = kwargs["new-name"]
                    if 'category' in kwargs.keys():
                        json_input["dns_security"]["dns_filtering"]["custom_domain"][0]["category"] = kwargs["category"]
                except KeyError as e:
                    logger.error(f"Key ERROR!! {e}")
                else:
                    if msg:
                        (resp, msg) = self.fw.api_put(url, msg=True, data=json_input)
                        return (resp, msg)
                    resp = self.fw.api_put(url, data=json_input)
                    return resp
            else:
                logger.error("Get DNS Custom Domain failed!!")
        else:
            logger.error("Please input valid domain and kwargs!!")
        return False

    def disable_dns_sinkhole(self, msg=False):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "enable": False,
                }
            }
        }
        resp = self.fw.api_put(self.url_dns_sinkhole, msg, data=json_input)
        return resp

    def enable_dns_sinkhole(self, msg=False, **kwargs):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "enable": True,
                    "action_type": {
                    }
                }
            }
        }
        try:
            if kwargs['action'] == 'dropping_with_logs' or kwargs[
                'action'] == 'dropping_with_negative_dns_reply_to_source':
                json_input['dns_security']['dns_sinkhole']['action_type'][kwargs['action']] = True
            elif kwargs['action'] == 'dropping_with_dns_reply_of_forged_ip':
                json_input['dns_security']['dns_sinkhole']['action_type'][kwargs['action']] = {}
                json_input['dns_security']['dns_sinkhole']['action_type'][kwargs['action']]['ipv4'] = kwargs['ipv4']
                json_input['dns_security']['dns_sinkhole']['action_type'][kwargs['action']]['ipv6'] = kwargs['ipv6']
            else:
                logger.error(
                    'Please specify action to one of dropping_with_logs,dropping_with_negative_dns_reply_to_source or dropping_with_dns_reply_of_forged_ip')
                return False
            if 'use_whitelist' in kwargs.keys():  # key 'use_whitelist' only support over 7.1.1 version
                json_input['dns_security']['dns_sinkhole']['use_whitelist'] = kwargs['use_whitelist']
        except KeyError as e:
            logger.error("Error: In creating JSON for dns sinkhole {}".format(e))
        resp = self.fw.api_put(self.url_dns_sinkhole, msg, data=json_input)
        return resp

    def show_dns_sinkhole(self):
        resp = self.fw.api_get(self.url_dns_sinkhole)
        return resp

    def add_dns_custom_list(self, msg=False, domain=None):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "custom_malicious_entry": []
                }
            }
        }
        json_input['dns_security']['dns_sinkhole']['custom_malicious_entry'].append({'name': domain})
        resp = self.fw.api_post(self.url_dns_custom, msg, data=json_input)
        return resp

    def delete_dns_custom_list(self, msg=False, domains=[]):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "custom_malicious_entry": []
                }
            }
        }
        for domain in domains:
            json_input['dns_security']['dns_sinkhole']['custom_malicious_entry'].append({'name': domain})
        resp = self.fw.api_delete(self.url_dns_custom, msg, data=json_input)
        return resp

    def show_dns_custom_list(self):
        resp = self.fw.api_get(self.url_dns_custom)
        return resp

        # after 7.1.1 version, to add/del/show dns security whitelist, please use DnsFilteringApi.add/del/show_dns_whitelist() methods

    def add_dns_white_list(self, msg=False, domain=None):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "white_list_entry": []
                }
            }
        }
        json_input['dns_security']['dns_sinkhole']['white_list_entry'].append({'name': domain})
        resp = self.fw.api_post(self.url_dns_white, msg, data=json_input)
        return resp

    def delete_dns_white_list(self, msg=False, domains=[]):
        json_input = {
            "dns_security": {
                "dns_sinkhole": {
                    "white_list_entry": []
                }
            }
        }
        for domain in domains:
            json_input['dns_security']['dns_sinkhole']['white_list_entry'].append({'name': domain})
        resp = self.fw.api_delete(self.url_dns_white, msg, data=json_input)
        return resp

    def show_dns_white_list(self):
        resp = self.fw.api_get(self.url_dns_white)
        return resp

    def set_dns_tunnel(self, msg=False, enable=False, block=False):
        json_input = {
            "dns_security": {
                "dns_tunnel": {
                    "enable": enable,
                    "block_all": block
                }
            }
        }
        resp = self.fw.api_put(self.url_dns_detect, msg, data=json_input)
        return resp

    def show_detected_client(self):
        resp = self.fw.api_get(self.url_dns_tunnel)
        return resp

    def add_dns_tunnel_white_list(self, msg=False, ip=None):
        json_input = {
            "dns_security": {
                "dns_tunnel": {
                    "white_list_entry": []
                }
            }
        }
        json_input['dns_security']['dns_tunnel']['white_list_entry'].append({'name': ip})
        resp = self.fw.api_post(self.url_dns_tunnel_white, msg, data=json_input)
        return resp

    def delete_dns_tunnel_white_list(self, msg=False, ips=[]):
        json_input = {
            "dns_security": {
                "dns_tunnel": {
                    "white_list_entry": []
                }
            }
        }
        for ip in ips:
            json_input['dns_security']['dns_tunnel']['white_list_entry'].append({'name': ip})
        resp = self.fw.api_delete(self.url_dns_tunnel_white, msg, data=json_input)
        return resp

    def show_dns_white_tunnel_list(self):
        resp = self.fw.api_get(self.url_dns_tunnel_white)
        return resp

    def disable_dns_tunnel_client_block_checkbox(self, ip='', msg=False):
        url = self.url_dns_tunnel_client + '/' + ip
        resp = self.fw.api_delete(url, msg)
        return resp

    def enable_dns_tunnel_client_block_checkbox(self, ip='', msg=False):
        url = self.url_dns_tunnel_client + '/' + ip
        resp = self.fw.api_post(url, msg)
        return resp


class DynamicRoutingApi:
    '''Arno Hu'''
    default_rip = {
        'interface': '',
        'mode': 'disable',
        'receive': '2',  # 0 rip1, 2 RIP2
        'send': '2',  # 0 RIPv1 ,1 RIPv2-v1 Compatible ,2 RIPv2
        'split_horizon': 'off',
        'poison_reverse': 'off',
        'password': '',
    }
    default_ospf2 = {
        'interface': '',
        'mode': 'disable',  # enable,disable,passive
        'dead_interval': '40',
        'hello_interval': '10',
        'auth': 'disable',  # disable,message digest,simple password
        'area': '112',
        'area_type': 'normal',  # normal, stub area, totally stubby area, not-so-stubby area,totally stubby nssa
        'auto': 'on',
        'priority': '1',
        'mtu': 'off',
    }
    ospf2_setting = {
        'route_metric': '110',
        'allow_ecmp_route': 'off',
        'router_id': '10.0.0.1',
        'abr_type': 'cisco',  # standard,cisco,ibm,shortcut
        'metric': '10',
        'bw': '100',
        'default_route': 'never',  # never,wan-up,always
        'metric': '10',
        'metric_type': '1',  # 1 means type-1,2 means type-2
        'static_route': 'off',
        'static_metric': '1',
        'static_tag': '1',
        'static_metric_type': '1',  # 1 means type-1,2 means type-2
        'connect_network': 'off',
        'connect_metric': '1',
        'connect_tag': '1',
        'connect_metric_type': '1',  # 1 means type-1,2 means type-2
        'rip_route': 'off',
        'rip_metric': '1',
        'rip_tag': '1',
        'rip_metric_type': '1',  # 1 means type-1,2 means type-2
        'vpn_network': 'off',
        'vpn_metric': '1',
        'vpn_tag': '1',
        'vpn_metric_type': '1',  # 1 means type-1,2 means type-2
    }
    rip_setting = {
        'DefaultMetric': '1',
        'OriginateDefaultRoute': 'off',
        'AdministrativeDistance': '120',
        'RedistributeStaticRoutes': 'off',
        'StaticsMetric': '1',
        'RedistributeConnectedNetworks': 'off',
        'ConnectedMetric': '1',
        'RedistributeOSPFRoutes': 'off',
        'OSPFMetric': '1',
        'RedistributeRemoteVPNNetworks': 'off',
        'VPNMetric': '1',
        'ZebosSyncEcmpToSonicOS': 'off',
        'DefaultRoutesMetric': '110'
    }

    ripng_setting = {
        'ZRipngSplitH': 'on',
        'ZRipngPoisonR': 'on',
        'zone': 'LAN'
    }

    default_ospf3 = {
        'interface': '',
        'mode': 'disable',  # enable,disable,passive
        'area': '0',
        'area_type': 'normal',
        'instid': '0',  # cannot change
        'dead_interval': '40',
        'hello_interval': 10,
        'cost': 9,  # cannot change
        'autocost': 'on',
        'priority': '1',
    }

    ospf3_setting = {
        'route_metric': '110',
        'allow_ecmp_route': 'off',
        'router_id': '10.0.0.1',
        'abr_type': 'cisco',  # standard,cisco,ibm,shortcut
        'bw': '100',
        'static_route': 'off',
        'static_metric': '1',
        'static_metric_type': '1',  # 1 means type-1,2 means type-2
        'connect_network': 'off',
        'connect_metric': '1',
        'connect_metric_type': '1',  # 1 means type-1,2 means type-2
        'rip_route': 'off',
        'rip_metric': '1',
        'rip_metric_type': '1',  # 1 means type-1,2 means type-2
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/raw'
        self.routing = 'api/sonicos/routing'
        self.url_ospfnb = 'api/sonicos/dynamic-file/getOspfIfNeighbors.json?id='
        self.url_bgp_summary = 'api/sonicos/dynamic-file/getBgpDisplaySummary.json'
        self.headers = OrderedDict([('Accept', 'application/json'),
                                    ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'),
                                    ('X-SNWL-API-Scope', 'extended'),
                                    ('charset', 'UTF-8')])
        self.default_cgi = {
            "stream": ""
        }
        self.cgi = "cgiaction=none&error_page=newRoutePolicies.html" \
                   "&refresh_page=newRoutePolicies.html" \
                   "&auditPath=Network+%2F+Routing&"

    def show_routing_settings(self):
        response = self.fw.api_get(self.routing)
        return response

    def edit_routing_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.routing, msg, data=json_input)
        return resp

    def set_advanced_routing_mode(self, msg=False, **kwargs):
        cgi = 'useAdvancedRouting='
        if kwargs['advanced']:
            cgi += 'on'
        else:
            cgi += 'off'
        self.default_cgi['stream'] = self.cgi + cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def set_BGP(self, msg=False, **kwargs):
        cgi = 'useBGP='
        if kwargs['BGP']:
            cgi += 'on'
        else:
            cgi += 'off'
        self.default_cgi['stream'] = self.cgi + cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    # def cal_vlan_interface(self, index):
    #     index = '0X10000A0' + str(index)
    #     return str(int(index, 16))

    def get_vlan_index(self, name, vlan):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('X-SNWL-API-Scope', 'extended'),
                               ('charset', 'UTF-8')])
        url = 'api/sonicos/interfaces/ipv4'
        resp = self.fw.api_get_header(url, headers=headers)
        vlan_index = 0
        try:
            for item in resp['interfaces']:
                if f'"name": "{name}"' in json.dumps(item) and f'"vlan": {vlan}' in json.dumps(item):
                    vlan_index = item['ipv4']['_properties']
                    logger.info(f"index of {name}:V{vlan}: {vlan_index}")
        except Exception:
            logger.error("can not find vlan interface index")
        return str(vlan_index)

    def set_rip(self, msg=False, **kwargs):
        rip_dict = copy.deepcopy(DynamicRoutingApi.default_rip)
        rip_dict.update(kwargs)
        kwargs = rip_dict

        if 'interface' not in kwargs:
            logger.error('Please specify interface when config rip.')
            return False
        elif 'V' in kwargs['interface'] or 'v' in kwargs['interface']:
            match = re.search('(\w+\d+):V(\d+)', kwargs['interface'], re.I)
            if match:
                name = match.group(1)
                vlan = match.group(2)
                index = self.get_vlan_index(name, vlan)
        elif 'type' in kwargs and kwargs['type'] == 'UnnumTI' and 'tunnel_id' in kwargs.keys():
            index = kwargs['tunnel_id']
        elif 'type' in kwargs and kwargs['type'] == 'TI' and 'num_id' in kwargs.keys():
            num = '0x60000{}01'.format(kwargs['num_id'])
            index = str(int(num, 16))
        else:
            index = kwargs['interface'].replace('X', '')
        cgi = 'cgiaction=undefined&tableIndex=' + index + '&refresh_page=newRoutePolicies.html&auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+' + \
              kwargs['interface'] + '+%28DMZ%29+RIP+Configuration&'
        mode = {
            'disable': '0',
            'send_and_receive': '1',
            'send': '2',
            'receive': '3',
            'passvie': '4',
        }
        rip_mode = mode[kwargs['mode']]
        if 'type' in kwargs and kwargs['type'] == 'UnnumTI':
            if 'UnnumBorrowedIf' in kwargs and kwargs['UnnumBorrowedIf']:
                if 'V' in kwargs['UnnumBorrowedIf'] or 'v' in kwargs['UnnumBorrowedIf']:
                    match = re.search('(X\d+):V(\d+)', kwargs['UnnumBorrowedIf'], re.I)
                    if match:
                        name = match.group(1)
                        vlan = match.group(2)
                        borrowedindex = self.get_vlan_index(name, vlan)
                        logger.info(borrowedindex)
                else:
                    borrowedindex = kwargs['UnnumBorrowedIf'].replace('X', '')
            cgi += 'ZRipUnnumBorrowedIf=' + borrowedindex + '&' + 'ZRipUnnumDstIp=' + kwargs['UnnumDstIp'] + '&'
        cgi += 'ZRipMode=' + rip_mode + '&'
        if rip_mode != '0' and rip_mode != 4:
            if rip_mode == '1' or rip_mode == '3':
                cgi += 'ZRipRMode=' + kwargs['receive'] + '&'
            if rip_mode == '1' or rip_mode == '2':
                cgi += 'ZRipSplitH=' + kwargs['split_horizon'] + '&ZRipPoisonR=' + kwargs[
                    'poison_reverse'] + '&ZRipSMode=' + kwargs['send'] + '&'
                cgi += 'cbox_ZRipSplitH=&cbox_ZRipPoisonR=&'
            if kwargs['password']:
                cgi += 'ZRipUsePassword=on&ZRipPassword=' + kwargs['password'] + '&'
            cgi += 'cbox_ZRipUsePassword='
        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def rip_config(self, msg=False, **kwargs):
        rip_setting_dict = copy.deepcopy(DynamicRoutingApi.rip_setting)
        rip_setting_dict.update(kwargs)
        kwargs = rip_setting_dict

        cgi = ' cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&'

        cgi += 'ZRipDefMetric=' + str(kwargs['DefaultMetric']) + '&'
        cgi += 'ZRipAdDist=' + str(kwargs['AdministrativeDistance']) + '&'
        cgi += 'ZRipOrigDef=' + str(kwargs['OriginateDefaultRoute']) + '&'

        cgi += f"ZRipRedistStatics={kwargs['RedistributeStaticRoutes']}&ZRipStaticsMetric={kwargs['StaticsMetric']}&"

        cgi += f"ZRipRedistConnected={kwargs['RedistributeConnectedNetworks']}&ZRipConnectedMetric={kwargs['ConnectedMetric']}&"

        cgi += f"ZRipRedistOspf={kwargs['RedistributeOSPFRoutes']}&ZRipOspfMetric={kwargs['OSPFMetric']}&"

        cgi += f"ZRipRedistVpn={kwargs['RedistributeRemoteVPNNetworks']}&ZRipVpnMetric={kwargs['VPNMetric']}&"

        cgi += 'ZebosDefRtPbrMetric=' + str(kwargs['DefaultRoutesMetric']) + '&'
        cgi += 'ZebosSyncEcmpToSonicOS=' + str(kwargs['ZebosSyncEcmpToSonicOS'])

        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def set_ripng(self, msg=False, **kwargs):
        ripng_dict = copy.deepcopy(DynamicRoutingApi.ripng_setting)
        ripng_dict.update(kwargs)
        kwargs = ripng_dict
        if 'interface' not in kwargs:
            logger.error('Please specify interface when config ripng.')
            return False
        elif 'V' in kwargs['interface'] or 'v' in kwargs['interface']:
            match = re.search('(\w+\d+):V(\d+)', kwargs['interface'], re.I)
            if match:
                name = match.group(1)
                vlan = match.group(2)
                index = self.get_vlan_index(name, vlan)
        elif 'type' in kwargs and kwargs['type'] == 'TI' and 'num_id' in kwargs.keys():
            num = '0x60000{}01'.format(kwargs['num_id'])
            index = str(int(num, 16))
        else:
            index = kwargs['interface'].replace('X', '')
        cgi = 'cgiaction=undefined&tableIndex=' + index + '&refresh_page=newRoutePolicies.html&'
        mode = {
            'disable': '0',
            'enable': '1',
            'passvie': '2',
        }
        ripng_mode = mode[kwargs['mode']]
        cgi += 'ZRipngMode=' + ripng_mode + '&'
        cgi += 'ZRipngSplitH=' + kwargs['ZRipngSplitH'] + '&ZRipngPoisonR=' + kwargs['ZRipngPoisonR'] + '&'
        cgi += f'auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+' + kwargs[
            'interface'] + f'+%28{kwargs["zone"]}%29+RIPng+Configuration'
        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def ospf2_config(self, msg=False, **kwargs):
        '''
        {"stream":"cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&ZOspfRouterId=10.0.0.1&ZOspfDefMetric=&ZOspfABRType=1&ZOspfRefBW=100&ZOspfOrigDef=1&ZOspfOrigMetric=12&ZOspfOrigMType=1&ZOspfRedistStatics=off&ZOspfStaticsTag=&ZOspfStaticsMetric=&ZOspfStaticsMType=2&ZOspfRedistConnected=off&ZOspfConnectedTag=&ZOspfConnectedMetric=&ZOspfConnectedMType=2&ZOspfRedistRip=off&ZOspfRipTag=&ZOspfRipMetric=&ZOspfRipMType=2&ZOspfRedistVpn=off&ZOspfVpnTag=&ZOspfVpnMetric=&ZOspfVpnMType=2&ZebosDefRtPbrMetric=110&ZebosSyncEcmpToSonicOS=off"}
        '''
        ospf2_setting_dict = copy.deepcopy(DynamicRoutingApi.ospf2_setting)
        ospf2_setting_dict.update(kwargs)
        kwargs = ospf2_setting_dict

        abr_type_dict = {
            'standard': '0',
            'cisco': '1',
            'ibm': '2',
            'shortcut': '3',
        }
        default_route_dict = {
            'never': '0',
            'wan-up': '1',
            'always': '2',
        }
        cgi = 'cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&'
        cgi += 'ZOspfRouterId=' + kwargs['router_id'] + '&'
        cgi += 'ZOspfDefMetric=&'
        cgi += 'ZOspfABRType=' + abr_type_dict[kwargs['abr_type']] + '&'
        cgi += 'ZOspfRefBW=' + str(kwargs['bw']) + '&'
        cgi += 'ZOspfOrigDef=' + default_route_dict[kwargs['default_route']] + '&'
        cgi += 'ZOspfOrigMetric=' + str(kwargs['metric']) + '&'
        cgi += 'ZOspfOrigMType=' + str(kwargs['metric_type']) + '&'

        cgi += 'ZOspfRedistStatics=' + kwargs['static_route'] + '&'
        if kwargs['static_route'] == 'on':
            cgi += f"ZOspfStaticsTag={kwargs['static_tag']}&ZOspfStaticsMetric={kwargs['static_metric']}&ZOspfStaticsMType={kwargs['static_metric_type']}&"
        else:
            cgi += 'ZOspfStaticsTag=&ZOspfStaticsMetric=&ZOspfStaticsMType=2&'

        cgi += 'ZOspfRedistConnected=' + kwargs['connect_network'] + '&'
        if kwargs['connect_network'] == 'on':
            cgi += f"ZOspfConnectedTag={kwargs['connect_tag']}&ZOspfConnectedMetric={kwargs['connect_metric']}&ZOspfConnectedMType={kwargs['connect_metric_type']}&"
        else:
            cgi += 'ZOspfConnectedTag=&ZOspfConnectedMetric=&ZOspfConnectedMType=2&'

        cgi += 'ZOspfRedistRip=' + kwargs['rip_route'] + '&'
        if kwargs['rip_route'] == 'on':
            cgi += f"ZOspfRipTag={kwargs['rip_tag']}&ZOspfRipMetric={kwargs['rip_metric']}&ZOspfRipMType={kwargs['rip_metric_type']}&"
        else:
            cgi += 'ZOspfRipTag=&ZOspfRipMetric=&ZOspfRipMType=2&'

        cgi += 'ZOspfRedistVpn=' + kwargs['vpn_network'] + '&'
        if kwargs['vpn_network'] == 'on':
            cgi += f"ZOspfVpnTag={kwargs['vpn_tag']}&ZOspfVpnMetric={kwargs['vpn_metric']}&ZOspfVpnMType={kwargs['vpn_metric_type']}&"
        else:
            cgi += 'ZOspfVpnTag=&ZOspfVpnMetric=&ZOspfVpnMType=2&'

        cgi += 'ZebosDefRtPbrMetric=' + kwargs['route_metric'] + '&'
        cgi += 'ZebosSyncEcmpToSonicOS=' + kwargs['allow_ecmp_route']
        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def set_ospf2(self, msg=False, **kwargs):
        '''
        {"stream":"cgiaction=undefined&tableIndex=1&refresh_page=newRoutePolicies.html&ZOspfMode=1&ZOspfDeadInterval=40&ZOspfHelloInterval=10&ZOspfAuthMode=1&ZOspfAuthText='ZOspfAuthText=
11&ZOspfArea=112&ZOspfAreaType=0&ZOspfIfAutoCost=on&ZOspfIfPriority=1&ZOspfIfIgnoreMtu=off&cbox_ZOspfIfIgnoreMtu=&cbox_ZOspfIfAutoCost=&auditPath=MONITOR
        '''
        ospf2_dict = copy.deepcopy(DynamicRoutingApi.default_ospf2)
        ospf2_dict.update(kwargs)
        kwargs = ospf2_dict

        if 'interface' not in kwargs:
            logger.error('Please specify interface when config rip.')
            return False
        elif 'V' in kwargs['interface'] or 'v' in kwargs['interface']:
            match = re.search('(X\d+):V(\d+)', kwargs['interface'], re.I)
            if match:
                name = match.group(1)
                vlan = match.group(2)
                index = self.get_vlan_index(name, vlan)
        elif 'type' in kwargs and kwargs['type'] == 'UnnumTI' and 'tunnel_id' in kwargs.keys():
            index = kwargs['tunnel_id']
        elif 'type' in kwargs and kwargs['type'] == 'TI' and 'num_id' in kwargs.keys():
            num = '0x60000{}01'.format(kwargs['num_id'])
            index = str(int(num, 16))
        else:
            index = kwargs['interface'].replace('X', '')
        cgi = 'cgiaction=undefined&tableIndex=' + index + '&refresh_page=newRoutePolicies.html&'
        mode = {
            'disable': '0',
            'enable': '1',
            'passive': '2'
        }
        auth_mode = {
            'disable': '0',
            'simple password': '1',
            'message digest': '2',
        }
        area_type = {
            'normal': '0',
            'stub area': '1',
            'totally stubby area': '2',
            'not-so-stubby area': '3',
            'totally stubby nssa': '4',

        }

        ospf2_mode = mode[kwargs['mode']]
        cgi += 'ZOspfMode=' + ospf2_mode + '&'
        if ospf2_mode == '2':
            cgi += 'ZOspfArea=' + str(kwargs['area']) + '&'
        else:
            cgi += 'ZOspfDeadInterval=' + str(kwargs['dead_interval']) + '&'
            cgi += 'ZOspfHelloInterval=' + str(kwargs['hello_interval']) + '&'
            cgi += 'ZOspfAuthMode=' + auth_mode[kwargs['auth']] + '&'
            if auth_mode[kwargs['auth']] != '0':
                cgi += 'ZOspfAuthText=' + kwargs['password'] + '&'
            cgi += 'ZOspfArea=' + str(kwargs['area']) + '&'
            cgi += 'ZOspfAreaType=' + area_type[kwargs['area_type']] + '&'
            if 'cost' in kwargs and kwargs['cost'] != 'on':
                cgi += 'ZOspfIfCost=' + kwargs['cost'] + '&'
            else:
                cgi += 'ZOspfIfAutoCost=on&'
            if 'router_priority' in kwargs and kwargs['router_priority'] != '1':
                cgi += f'ZOspfIfPriority={kwargs["router_priority"]}&'
            else:
                cgi += 'ZOspfIfPriority=1&'
            cgi += 'ZOspfIfIgnoreMtu=' + kwargs['mtu'] + '&'
        if 'type' in kwargs and kwargs['type'] == 'UnnumTI':
            if 'UnnumBorrowedIf' in kwargs and kwargs['UnnumBorrowedIf']:
                if 'V' in kwargs['UnnumBorrowedIf'] or 'v' in kwargs['UnnumBorrowedIf']:
                    match = re.search('(X\d+):V(\d+)', kwargs['UnnumBorrowedIf'], re.I)
                    if match:
                        name = match.group(1)
                        vlan = match.group(2)
                        borrowedindex = self.get_vlan_index(name, vlan)
                        logger.info(borrowedindex)
                else:
                    borrowedindex = kwargs['UnnumBorrowedIf'].replace('X', '')
            cgi += 'ZOspfUnnumBorrowedIf=' + borrowedindex + '&' + 'ZOspfUnnumDstIp=' + kwargs['UnnumDstIp'] + '&'
        cgi += 'auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+' + kwargs[
            'interface'] + '+%28WAN%29+OSPFv2+Configuration'
        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    # by JLian
    def ospf3_config(self, msg=False, **kwargs):
        '''
        {"stream":"cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&
        ZOspf3RouterId=10.10.10.10&
        ZOspf3DefMetric=&
        ZOspf3ABRType=1&
        ZOspf3RefBW=100&
        ZOspf3RedistStatics=off&
        ZOspf3StaticsMetric=&
        ZOspf3StaticsMType=2&
        ZOspf3RedistConnected=off&
        ZOspf3ConnectedMetric=&
        ZOspf3ConnectedMType=2&
        ZOspf3RedistRip=off&ZOspf3RipMetric=&
        ZOspf3RipMType=2&
        ZebosDefRtPbrMetric=110&
        ZebosSyncEcmpToSonicOS=off"}
        '''

        ospf3_setting_dict = copy.deepcopy(DynamicRoutingApi.ospf3_setting)
        ospf3_setting_dict.update(kwargs)
        ospf3_dict = ospf3_setting_dict

        abr_type_dict = {
            'standard': '0',
            'cisco': '1',
            'ibm': '2',
            'shortcut': '3',
        }
        logger.info(ospf3_dict)
        cgi = 'cgiaction=none&error_page=newRoutePolicies.html&refresh_page=newRoutePolicies.html&auditPath=Network+%2F+Routing&'
        cgi += 'ZOspf3RouterId=' + ospf3_dict['router_id'] + '&'
        cgi += 'ZOspf3DefMetric=&'
        cgi += 'ZOspf3ABRType=' + abr_type_dict[ospf3_dict['abr_type']] + '&'
        cgi += 'ZOspf3RefBW=' + str(ospf3_dict['bw']) + '&'

        cgi += 'ZOspf3RedistStatics=' + ospf3_dict['static_route'] + '&'
        if ospf3_dict['static_route'] == 'on':
            cgi += f"ZOspf3StaticsMetric={ospf3_dict['static_metric']}&ZOspf3StaticsMType={ospf3_dict['static_metric_type']}&"
        else:
            cgi += 'ZOspf3StaticsMetric=&ZOspf3StaticsMType=2&'

        cgi += 'ZOspf3RedistConnected=' + ospf3_dict['connect_network'] + '&'
        if ospf3_dict['connect_network'] == 'on':
            cgi += f"ZOspf3ConnectedMetric={ospf3_dict['connect_metric']}&ZOspf3ConnectedMType={ospf3_dict['connect_metric_type']}&"
        else:
            cgi += 'ZOspf3ConnectedMetric=&ZOspf3ConnectedMType=2&'

        cgi += 'ZOspf3RedistRip=' + ospf3_dict['rip_route'] + '&'
        if ospf3_dict['rip_route'] == 'on':
            cgi += f"ZOspf3RipMetric={ospf3_dict['rip_metric']}&ZOspf3RipMType={ospf3_dict['rip_metric_type']}&"
        else:
            cgi += 'ZOspf3RipTag=&ZOspf3RipMetric=&ZOspfRipMType=2&'

        cgi += 'ZebosDefRtPbrMetric=' + ospf3_dict['route_metric'] + '&'
        cgi += 'ZebosSyncEcmpToSonicOS=' + ospf3_dict['allow_ecmp_route']
        self.default_cgi['stream'] = cgi
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    # by JLian
    def set_ospf3(self, msg=False, **kwargs):
        '''
        {"stream":"&cgiaction=none&tableIndex=0&refresh_page=newRoutePolicies.html&ZOspf3Mode=1&ZOspf3Area=0&
        ZOspf3AreaType=0&ZOspf3InstId=0&ZOspf3DeadInterval=40&ZOspf3HelloInterval=10&ZOspf3IfCost=9&ZOspf3IfAutoCost=on
        &ZOspf3IfPriority=1&auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+X0+%28LAN%29+OSPFv3+Configuration
        }
        '''
        ospf3_setting_dict = copy.deepcopy(DynamicRoutingApi.default_ospf3)
        # ospf3_dict.update(kwargs)
        # kwargs = ospf3_dict
        ospf3_setting_dict.update(kwargs)
        ospf3_dict = ospf3_setting_dict
        if 'interface' not in ospf3_dict:
            logger.error('Please specify interface when config rip.')
            return False
        elif 'V' in ospf3_dict['interface'] or 'v' in ospf3_dict['interface']:
            match = re.search('(X\d+):V(\d+)', ospf3_dict['interface'], re.I)
            if match:
                name = match.group(1)
                vlan = match.group(2)
                index = self.get_vlan_index(name, vlan)
        else:
            index = ospf3_dict['interface'].replace('X', '')
        cgi = '&cgiaction=none&tableIndex=' + index + '&refresh_page=newRoutePolicies.html&'
        mode = {
            'disable': '0',
            'enable': '1',
            'passive': '2'
        }
        area_type = {
            'normal': '0',
            'stub area': '1',
            'totally stubby area': '2',
        }
        ospf3_mode = mode[ospf3_dict['mode']]
        cgi += 'ZOspf3Mode=' + ospf3_mode + '&'
        if ospf3_mode == '2':
            cgi += 'ZOspfArea=' + str(ospf3_dict['area']) + '&'
        else:
            cgi += 'ZOspf3Area=' + str(ospf3_dict['area']) + '&'
            cgi += 'ZOspf3AreaType=' + area_type[ospf3_dict['area_type']] + '&'
            cgi += 'ZOspf3InstId=0&'
            cgi += 'ZOspf3DeadInterval=' + str(ospf3_dict['dead_interval']) + '&'
            cgi += 'ZOspf3HelloInterval=' + str(ospf3_dict['hello_interval']) + '&'
            cgi += 'ZOspf3IfCost=9&'
            cgi += 'ZOspf3IfAutoCost=' + str(ospf3_dict['autocost']) + '&'
            cgi += 'ZOspf3IfPriority=' + str(ospf3_dict['priority']) + '&'
            # cgi += 'ZOspf3IfPriority=1'
        cgi += 'auditPath=MONITOR+%2F+Network+%2F+Routing+%2F+Interface+' + ospf3_dict[
            'interface'] + '+%28LAN%29+OSPFv3+Configuration'
        self.default_cgi['stream'] = cgi
        logger.info(f'cgi is:{cgi}')
        res = self.fw.api_post(self.url, msg, data=self.default_cgi, headers=self.headers)
        return res

    def get_route_advanced_data(self, msg=False):
        url = 'api/sonicos/dynamic-file/getAdvancedRoutingData.json'
        res = self.fw.api_get(url, msg)
        return res

    def get_route_list_in_type(self, rtype='rip'):
        route_list_url = 'api/sonicos/dynamic-file/getRouteList.json?reqType='
        if rtype == 'rip':
            url = route_list_url + '4096'
        elif rtype == 'ospfv2':
            url = route_list_url + '256'
        elif rtype == 'ospfv3':
            url = route_list_url + '65536'
        elif rtype == 'riping':
            url = route_list_url + '1048576'
        else:
            logger.info('Please input a vaild route type: rip/ospfv2/ospfv3/riping')
            return ''
        response = self.fw.api_get(url)
        return response

    def get_rip_list_data(self, msg=False):
        url = 'api/sonicos/dynamic-file/getRouteList.json?reqType=4096'
        res = self.fw.api_get(url, msg)
        return res

    def get_ospf_list_data(self, msg=False):
        url = 'api/sonicos/dynamic-file/getRouteList.json?reqType=256'
        res = self.fw.api_get(url, msg)
        return res

    # add by JLian
    def get_interface_ospfv2_status(self, **kwargs):
        # dict = {'interface': 'Ni',
        #         'type': 'TI',
        #         'num_id':
        #         }
        index = ''
        if 'interface' not in kwargs.keys():
            logger.error('Please specify interface when config ospfv2')
            return ''
        if 'V' in kwargs['interface'] or 'v' in kwargs['interface']:
            match = re.search('(X\d+):V(\d+)', kwargs['interface'], re.I)
            if match:
                name = match.group(1)
                vlan = match.group(2)
                index = self.get_vlan_index(name, vlan)
        elif 'type' in kwargs and kwargs['type'] == 'TI' and 'num_id' in kwargs.keys():
            num = '0x60000{}01'.format(kwargs['num_id'])
            index = str(int(num, 16))
        else:
            index = kwargs['interface'].replace('X', '')
        url_ospfnb_index = self.url_ospfnb + index
        logger.info(f'get ospf neighbor url is:{url_ospfnb_index}')
        rc = self.fw.api_get(url_ospfnb_index)
        return rc

    # add by JLian
    def get_bgp_summary(self):
        logger.info(f'get bgp summary url is:{self.url_bgp_summary}')
        rc = self.fw.api_get(self.url_bgp_summary)
        return rc


class FailoverLbApi:
    '''Arno Hu'''
    settings_options = {
        'enable': True,
        'probes': False,
        'syn': False,
        'port': 1,
    }
    groups_options = {
        'name': '+Default+LB+Group',
        'interface': 'X1',
        'probe_type': 'logical',
        'probe_option': 'both',
        'main_protocol': 'tcp',
        'main_value': 50000,  # tcp:50000;  ping:True;
        'main_host': "responder.global.sonicwall.com",
        'alter_protocol': 'tcp',
        'alter_value': 50000,  # tcp:50000;  ping:True;
        'alter_host': "responder.global.sonicwall.com",
        'default_value': '204.212.170.23',
    }

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/failover-lb/base'
        self.groups_url = 'api/sonicos/failover-lb/groups'
        self.report_url = 'api/sonicos/reporting/failover-lb'
        self.json = {
            "failover_lb": {
                "enable": True,
                "respond_to_probes": False,
                "any_tcp_syn": False,
                "port": 1
            }
        }
        self.failover_json = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 50000
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 50000
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "default_target": {
                                    "value": "204.212.170.23"
                                }
                            }
                        ]
                    }
                ]
            }
        }

    def config_failover_settings_deepcopy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        response = self.fw.api_put(self.base_url, msg, data=json_input)
        return response

    def config_failover_settings(self, msg=False, **kwargs):
        self.options = dict(FailoverLbApi.settings_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_failover_settings_json(**kwargs)
        res = self.fw.api_put(self.base_url, msg, data=json_input)
        return res

    def config_failover_groups(self, msg=False, **kwargs):
        self.options = dict(FailoverLbApi.groups_options)
        self.options.update(kwargs)
        kwargs = self.options
        name = kwargs['name'].replace('+', '%20')
        url = self.groups_url + '/name/{}'.format(name)
        json_input = self.build_failover_groups_json(url, **kwargs)
        res = self.fw.api_put(url, msg, data=json_input)
        return res

    # because the config_failover_groups can not support set the multi interfaces
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

    def check_failover_groups_status(self):
        url = 'api/sonicos/reporting/failover-lb/status/groups'
        res = self.fw.api_get(url)
        return res

    def check_failover_members_status(self):
        url = 'api/sonicos/reporting/failover-lb/status/members'
        res = self.fw.api_get(url)
        return res

    def check_failover_setting(self):
        res = self.fw.api_get(self.base_url)
        return res

    def reset_statistics(self, version='ipv4'):
        url = self.report_url + '/' + version
        res = self.fw.api_delete(url)
        return res

    def get_statistics_report(self):
        url = self.report_url + '/statistics'
        res = self.fw.api_get(url)
        return res

    def get_failover_groups_info(self):
        res = self.fw.api_get(self.groups_url)
        return res

    def build_failover_settings_json(self, **kwargs):
        json_input = self.fw.api_get(self.base_url)
        path = json_input['failover_lb']
        path['enable'] = kwargs['enable']
        path['respond_to_probes'] = kwargs['probes']
        path['any_tcp_syn'] = kwargs['syn']
        path['port'] = kwargs['port']
        return json_input

    def build_failover_groups_json(self, url, **kwargs):
        json_input = self.fw.api_get(url)
        path = json_input['failover_lb']['group'][0]
        # path['name'] = kwargs['name'].replace('+', ' ')

        if path['final_backup']:
            if kwargs['interface'] == 'X1':
                target = path['interface'][0]
            if kwargs['interface'] == 'X2':
                target = path['interface'][2]
            if kwargs['interface'] == 'X3':
                target = path['interface'][3]
            if kwargs['interface'] == 'X4':
                target = path['interface'][4]
            if kwargs['interface'] == path['final_backup']:
                target = path['interface'][1]
        else:
            if kwargs['interface'] == 'X1':
                target = path['interface'][0]
            if kwargs['interface'] == 'X2':
                target = path['interface'][1]
            if kwargs['interface'] == 'X3':
                target = path['interface'][2]
            if kwargs['interface'] == 'X4':
                target = path['interface'][3]
            if kwargs['interface'] == 'X5':
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
                target['main_target']['protocol']['ping'] = {}
                target['main_target']['protocol']['ping'] = kwargs['main_value']
                target['main_target']['host'] = kwargs['main_host']

            if kwargs['alter_protocol'] == 'tcp':
                target['alternate_target']['protocol']['tcp'] = {}
                target['alternate_target']['protocol']['tcp']['value'] = kwargs['alter_value']
                target['alternate_target']['host'] = kwargs['alter_host']
            elif kwargs['alter_protocol'] == 'ping':
                target['main_target']['protocol']['ping'] = {}
                target['main_target']['protocol']['ping'] = kwargs['alter_value']
                target['main_target']['host'] = kwargs['alter_host']

        return json_input


class DnsFilteringApi:

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/dns-security/dns-filtering/base'
        self.whitelist_url = 'api/sonicos/dns-security/white-list-entries'
        self.dns_filtering_profiles_url = 'api/sonicos/dns-security/dns-filtering/profiles'

        self.initial_dns_filtering_profiles_json = {
            "dns_security": {
                "dns_filtering": {
                    "profile": [
                        {
                            "name": "Default Profile",
                            "id": 0,
                            "_properties": 19,
                            # "actions": "{\"1\":0,\"2\":0,\"3\":0,\"4\":2,\"5\":0,\"6\":0,\"7\":2,\"8\":0,\
                            # \"9\":2,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":0,\"17\":0,\"18\":2,\"19\":0}"
                        }
                    ]
                }
            }
        }

    def get_dns_filtering_profile(self):
        out = self.fw.api_get(self.dns_filtering_profiles_url)
        return out

    def get_dns_filtering_profile_by_name(self, name=''):
        if not name:
            logger.error("Please enter profile's name!")
            return False
        url = f'{self.dns_filtering_profiles_url}/name/{name}'
        return self.fw.api_get(url)

    def add_dns_filtering_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        repu_resp = self.fw.api_post(self.dns_filtering_profiles_url, msg, data=json_input)
        return repu_resp

    def check_dns_filtering_global_settings(self):
        json_output = self.fw.api_get(self.base_url)
        return json_output

    def config_whitelist(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.base_url, msg, data=json_input)
        return resp

    def add_dns_whitelist(self, msg=False, name=None):
        json_input = {
            "dns_security": {
                "white_list_entry": [
                    {"name": ''}
                ]
            }
        }
        json_input['dns_security']['white_list_entry'][0]['name'] = name
        logger.info(json_input)
        resp = self.fw.api_post(self.whitelist_url, msg, data=json_input)
        return resp

    def del_dns_whitelist(self, msg=False, name_list=None):
        json_input = {
            "dns_security": {
                "white_list_entry": [
                    # {"name": ''}
                ]
            }
        }
        for name in name_list:
            json_input['dns_security']['white_list_entry'].append({"name": name})
        logger.info(json_input)
        resp = self.fw.api_delete(self.whitelist_url, msg, data=json_input)
        return resp

    def show_whitelist(self):
        json_output = self.fw.api_get(self.whitelist_url)
        return json_output

    def config_forged_ip(self, msg=False, ipv4='', ipv6=''):
        # example_json = {"dns_security":{"dns_filtering":{"use_whitelist":true,"forged_ip":{"ipv4":"192.168.100.100","ipv6":"::1"}}}}
        if not ipv4 and not ipv6:
            logger.error("Please enter at least one ipv4 or ipv6 address!")
            return False
        json_input = self.fw.api_get(self.base_url)
        if not json_input:
            logger.error("Get DNS Filtering base configs failed!")
            return False
        if ipv4:
            json_input["dns_security"]["dns_filtering"]["forged_ip"]["ipv4"] = ipv4
        if ipv6:
            json_input["dns_security"]["dns_filtering"]["forged_ip"]["ipv6"] = ipv6
        if msg:
            (resp, msg) = self.fw.api_put(self.base_url, msg=True, data=json_input)
            return (resp, msg)
        return self.fw.api_put(self.base_url, data=json_input)

    def edit_dns_profile_by_name(self, name, msg=True, **kwargs):
        if name:
            url = str(self.dns_filtering_profiles_url) + '/name/' + name
            json_input = copy.deepcopy(kwargs)
            resp = self.fw.api_put(url, msg, data=json_input)
            # output= json_input.loads(self.fw.api_post_pendingchanges())
            return resp
        else:
            logger.error("Pls enter profile's name")

    def config_dns_filtering_profile(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.dns_filtering_profiles_url, msg, data=json_input)
        return resp

    def del_dns_profile_by_name(self, name, msg=False):
        if name:
            url = str(self.dns_filtering_profiles_url) + '/name/' + name
            resp = self.fw.api_delete(url, msg)
            return resp

        else:
            logger.error("Pls enter profile's name")

    def get_dns_filtering_statistics(self):
        url = 'api/sonicos/reporting/dns-security/filtering-statistical'
        return self.fw.api_get(url)

    def export_dns_filtering_database_csv(self, filepath='/tmp/dnsfilterDB.csv'):
        if not filepath:
            logger.error('Please enter valid filepath!!')
            return False
        url = 'api/sonicos/export/dns-filter-db/csv'
        exp = self.fw.api_get(url, log_switch=False)
        with open(filepath, 'w+') as f:
            f.write(str(exp))
        logger.info(f'the exp file {filepath} has been exported.')
        f.close()
        return True


class DnsPolicyApi:

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/dns-policies'
        self.initial_DnsProxyPolicy_json = {
            "dns_policies": [
                {
                    "name": "dns_proxy",
                    "priority": {
                        "manual": 1
                    },
                    "enable": True,
                    "comment": "",
                    "source": {
                        "address": {
                            "name": "X2 Subnet"
                        }
                    },
                    "service": {
                        "group": "DNS (Name Service)"
                    },
                    "from": "any",
                    "schedule": {
                        "always_on": True
                    },
                    "action": {
                        "proxy": True
                    },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                    },
                    "max_connections": 100,
                    "connection_limit": {
                        "source": {
                            "enable": False,
                            "threshold": {
                                "value": 128
                            }
                        }
                    },
                    "proxy_mode": "ipv4-ipv4"
                }
            ]
        }

    def build_DnsProxyPolicy_json(self, **kwargs):
        '''
        dns_proxy_4to4 = {
            "name": "dns_proxy_4to4",
            "proxy_mode": "ipv4-ipv4"
        }
        '''
        json_input = copy.deepcopy(self.initial_DnsProxyPolicy_json)
        if 'name' in kwargs.keys():
            json_input['dns_policies'][0]['name'] = kwargs['name']
        if 'proxy_mode' in kwargs.keys():
            json_input['dns_policies'][0]['proxy_mode'] = kwargs['proxy_mode']
        if 'enable' in kwargs.keys():
            json_input['dns_policies'][0]['enable'] = kwargs['enable']
        if 'source' in kwargs.keys():
            json_input['dns_policies'][0]['source'] = kwargs['source']
        if 'from' in kwargs.keys():
            json_input['dns_policies'][0]['from'] = kwargs['from']
        if 'service' in kwargs.keys():
            json_input['dns_policies'][0]['service'] = kwargs['service']
        if 'action' in kwargs.keys():
            json_input['dns_policies'][0]['action'] = kwargs['action']

        return json_input

    def add_dns_policy(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_post(self.base_url, msg, data=json_input)
        return resp

    def add_dns_proxy_policy(self, msg=False, **kwargs):
        json_input = self.build_DnsProxyPolicy_json(**kwargs)
        response = self.fw.api_post(self.base_url, msg, data=json_input)
        return response

    def get_dns_policies(self):
        resp = self.fw.api_get(self.base_url)
        return resp

    def get_dns_policy_uuid(self, name):
        policies = self.fw.api_get(self.base_url)
        for dns_policy in policies['dns_policies']:
            if dns_policy['name'] == name:
                uuid = dns_policy['uuid']
        return uuid

    def del_dns_policy_uuid(self, uuid):
        url = self.base_url + '/uuid/' + uuid
        logger.info("URL for delete: {}".format(url))
        delete_response = self.fw.api_delete(url)
        return delete_response

    def edit_dns_policy_uuid(self, uuid, **kwargs):
        url = self.base_url + '/uuid/' + uuid
        print("PUT JSON to URL: {}".format(url))
        json_input = self.build_DnsProxyPolicy_json(**kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response

    def edit_dns_policy(self, **kwargs):
        uuid = self.get_dns_policy_uuid(kwargs['name'])
        url = self.base_url + '/uuid/' + uuid
        print("PUT JSON to URL: {}".format(url))
        json_input = self.build_DnsProxyPolicy_json(**kwargs)
        put_response = self.fw.api_put(url, data=json_input)
        return put_response


class FloodProtectionApi:
    def __init__(self, fw):
        self.fw = fw
        self.tcp_url = 'api/sonicos/tcp'
        self.reports_url = 'api/sonicos/reporting/tcp'
        self.inital_tcp_flood_protection_json = {
            "tcp": {
                "enforce_strict_compliance": False,
                "checksum_enforcement": False,
                "drop": {
                    "syn_with_data": False,
                    "invalid_urgent": True
                },
                "enable_handshake_timeout": True,
                "handshake_timeout": 30,
                "default_connection_timeout": 15,
                "maximum_segment_lifetime": 8,
                "half_open_threshold": False,
                "syn_flood_protection_mode": "watch-and-report",
                "syn_attack_threshold": 300,
                "syn_flood_blacklisting": False,
                "ddos": {
                    "on_wan_interfaces": False
                },
                # "blacklist_threshold": 1000,
                # "never_blacklist_wan": False,
                # "always_allow_management": False

            }
        }

    def build_tcp_flood_protection_json(self, **kwargs):
        json_input = copy.deepcopy(self.inital_tcp_flood_protection_json)
        if 'syn_flood_protection_mode' in kwargs.keys():
            json_input['tcp']['syn_flood_protection_mode'] = kwargs['syn_flood_protection_mode']
        if 'syn_flood_blacklisting' in kwargs.keys():
            json_input['tcp']['syn_flood_blacklisting'] = kwargs['syn_flood_blacklisting']
        if 'blacklist_threshold' in kwargs.keys():
            json_input['tcp']['blacklist_threshold'] = kwargs['blacklist_threshold']
        if 'never_blacklist_wan' in kwargs.keys():
            json_input['tcp']['never_blacklist_wan'] = kwargs['never_blacklist_wan']
        if 'always_allow_management' in kwargs.keys():
            json_input['tcp']['always_allow_management'] = kwargs['always_allow_management']
        if 'support_tcp_sack' in kwargs.keys():
            json_input['tcp']['support_tcp_sack'] = kwargs['support_tcp_sack']
        if 'enable_limit_mss' in kwargs.keys():
            json_input['tcp']['enable_limit_mss'] = kwargs['enable_limit_mss']
        if 'always_log_syn_packets' in kwargs.keys():
            json_input['tcp']['always_log_syn_packets'] = kwargs['always_log_syn_packets']

        return json_input

    def config_tcp_flood_protection(self, msg=False, **kwargs):
        json_input = self.build_tcp_flood_protection_json(**kwargs)
        resp = self.fw.api_put(self.tcp_url, msg, data=json_input)
        return resp

    def get_tcp_flood_protection(self, msg=False):
        resp = self.fw.api_get(self.tcp_url, msg)
        return resp

    def clear_tcp_reports(self, msg=False):
        resp = self.fw.api_delete(self.reports_url, msg)
        return resp

    def get_tcp_reports(self, msg=False):
        resp = self.fw.api_get(self.reports_url, msg)
        return resp


class VLANTranslationApi:

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/vlan-translations'
        self.initial_vlan_translation_json = {
            "vlan_translations": [{
                "ingress": {
                    "interface": "X2",
                    "vlan": 1
                },
                "egress": {
                    "interface": "X4",
                    "vlan": 2
                },
                "reverse": True}]
        }

    def build_vlan_translation(self, **kwargs):
        json_iput = copy.deepcopy(self.initial_vlan_translation_json)
        if 'ingress_interface' in kwargs.keys():
            json_iput['vlan_translations'][0]['ingress']['interface'] = kwargs['ingress_interface']
        if 'ingress_vlan' in kwargs.keys():
            json_iput['vlan_translations'][0]['ingress']['vlan'] = kwargs['ingress_vlan']
        if 'egress_interface' in kwargs.keys():
            json_iput['vlan_translations'][0]['egress']['interface'] = kwargs['egress_interface']
        if 'egress_vlan' in kwargs.keys():
            json_iput['vlan_translations'][0]['egress']['vlan'] = kwargs['egress_vlan']
        if 'reverse' in kwargs.keys():
            json_iput['vlan_translations'][0]['reverse'] = kwargs['reverse']
        return json_iput

    def add_vlan_translation(self, msg=False, **kwargs):
        json_input = self.build_vlan_translation(**kwargs)
        resp = self.fw.api_post(self.url, msg, data=json_input)
        return resp

    def edit_vlan_translation(self, msg=False, **kwargs):
        json_input = self.build_vlan_translation(**kwargs)
        url = self.url + '/ingress/interface/' + kwargs['old_ingress_interface'] + '/vlan/' + str(
            kwargs['old_ingress_vlan']) + '/egress/interface/' + kwargs['old_egress_interface'] + '/vlan/' + str(
            kwargs['old_egress_vlan'])
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp

    def del_vlan_translation(self, msg=False, **kwargs):
        # Just only for delete one vlan translation
        json_input = self.build_vlan_translation(**kwargs)
        resp = self.fw.api_delete(self.url, msg, data=json_input)
        return resp

    def del_multiple_vlan_translation(self, msg=False, **kwargs):
        #  delete one or more vlan translations
        resp = self.fw.api_delete(self.url, msg, data=kwargs)
        return resp


class MulticastApi:

    def __init__(self, fw):
        self.fw = fw
        self.multicast = 'api/sonicos/multicast/base'

    def show_multicast_settings(self):
        response = self.fw.api_get(self.multicast)
        return response

    def edit_multicast_settings(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.multicast, msg, data=json_input)
        return resp
