import copy
import json
import re
import time
from runner.settings import logger
from collections import OrderedDict

class VPNSitetoSiteAPI:
    '''VPNSitetoSiteAPI'''

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/vpn/policies/ipv4/site-to-site'
        self.url_ipv6 = 'api/sonicos/vpn/policies/ipv6/site-to-site'
        self.url2 = 'api/sonicos/vpn/policies/ipv4/group-vpn'

    def get_site_to_site_ipv4(self):
        out = self.fw.api_get(self.url)
        return out

    def add_site_to_site_ipv4(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        schedule_resp = self.fw.api_post(self.url, msg, data=json_input)
        return schedule_resp

    def delete_site_to_site_ipv4(self, name, msg=False):
        edit_url = self.url + '/name/' + name
        resp = self.fw.api_delete(edit_url, msg)
        return resp

    def edit_site_to_site_ipv4(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp
    
    def edit_default_group_vpn(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url2 + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def delete_site_to_site_ipv4(self, name, msg=False):
        edit_url = self.url + '/name/' + name
        resp = self.fw.api_delete(edit_url, msg)
        return resp

    def get_site_to_site_ipv6(self):
        out = self.fw.api_get(self.url_ipv6)
        return out

    def add_site_to_site_ipv6(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        schedule_resp = self.fw.api_post(self.url_ipv6, msg, data=json_input)
        return schedule_resp

    def edit_site_to_site_ipv6(self, name, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        edit_url = self.url_ipv6 + '/name/' + name
        resp = self.fw.api_put(edit_url, msg, data=json_input)
        return resp

    def delete_site_to_site_ipv6(self, name, msg=False):
        edit_url = self.url_ipv6 + '/name/' + name
        resp = self.fw.api_delete(edit_url, msg)
        return resp

class VpnbasesettingApi:
    '''VpnbasesettingApi class'''
    default_ipv4_options = {
        'ipversion': 'ipv4',
        'type': '',  # site_to_site, tunnel_interface
        'name': '',
        'enable': True,
        'auth_mode': '',  # certificate or shared_secret
        'local_cert': '',  # only for certificate auth
        'secret': '',  # only for shared_secret auth
        'local_ike_type': '', # arg can be:default-id; distinguished_name; domain_name; email_id; ip
        'local_ike_id': '',
        'peer_ike_type': '',  # arg can be:distinguished_name; domain_name; email_id; ip
        'peer_ike_id': '',
        'pri_gate': '0.0.0.0',
        'sec_gate': '0.0.0.0',
        'local_net_type': '',  # name, group, host, network, range, any
        'remote_net_type': '',  # name, group, host, network, range
        'local_network': '',  # X0 subnet,     add_group, hostip, add_network, add_range, none
        'remote_network': '',  # add_remote_net, add_group, hostip, add_network, add_range
        ### proposal setting ######
        'ike_exchange': 'ikev2',  # main, aggressive, ikev2
        'ike_dh_group': '2',
        'ike_encryption': 'aes-128',
        'ike_auth': 'sha-1',
        'ike_lifetime': 28800,
        'ipsec_protocol': 'esp',
        'ipsec_encryption': 'aes_128',
        'ipsec_auth': 'sha_1',
        'ipsec_lifetime': 28800,
        'ipsec_pfs': False,
        'ipsec_pfs_dhgroup': 2,
        ## advanced setting #####
        'netbios': False,
        'anti_replay': True,
        # 'wxa_group': '',
        'multicast': False,
        'ocsp_checking': False,
        'ocsp_resp_url': '',
        'send_hash': '',
        'management_https': False,
        'management_ssh': False,
        'management_snmp': False,
        'keep_alive': False,
        'allow_sonicpointn_layer3': False,
        'user_login_http': False,
        'user_login_https': False,
        # 'preempt_interval': 120,
        'default_lan_gateway': '0.0.0.0',        #arg=gw or none
        'bound_to': ['interface', 'X1'],     ##['zone', 'WAN']
        'suppress_trigger_packet': False,
        'accept_hash': False,
        'suppress_auto_add_rule': False,
        'edit_applynat': True,
        'apply_nat': False,
        'nat_local_type': '',  # name, group, host, network, range, original
        'nat_remote_type': '',
        'nat_local': '',  # name, group, host, network, range, original
        'nat_remote': '',
        'require_xauth': '',
        'advanced_routing': False,
        'transport_mode': False,    
        ## client setting###
        "cache_xauth": "never",#'always','single-session'
        "virtual_adaptor": "none", #'dhcp-and-manual','dhcp-only'
        "allow_connections_to": "split-tunnels",#'this-gateway-only','all-secured-gateways'
        "default_route": False,
        "access_list": False,
        "simple_provisioning": False,           
        ### manualkey auth proposal
        'in_spi': '0xa5ce265b',       ###  3-8 bit Hexa characters
        'out_spi': '0xed2fed7a',      ###  3-8 bit Hexa characters
        'encryption_key': '002ec148922d88453aa6e57da7e447b8',   ###  16 bit Hexa characters
        'authentication_key': '6e7ce00d48598dc0bf52279bddb8e41b5e805c70',    ### 40 bit Hexa characters     
    }

    default_wangroup_options = {
        'enable': False,
        'auth_mode': '',  # certificate or shared_secret
        'secret': '123456',  # only for shared_secret auth
        'local_cert': '',  # only for certificate auth
        'peer_ike_type': '',
        'peer_ike_id': '',
        
        ### proposal setting ######
        'ike_encryption': 'aes-128',
        'ike_auth': 'sha-1',
        'ike_dh_group': '2',
        'ike_lifetime': 28800,
        'ipsec_protocol': 'esp',
        'ipsec_pfs': False,
        'ipsec_pfs_dhgroup': 2,
        'ipsec_lifetime': 28800,
        'ipsec_encryption': 'aes_128',
        'ipsec_auth': 'sha_1',
        
        ## advanced setting #####
        'anti_replay': True,
        'permit_acceleration': False,
        'multicast': False,
        'management_https': False,
        'management_ssh': False,
        'management_snmp': False,
        'accept_multiple_proposals': False,
        'default_lan_gateway': '0.0.0.0',

         ## client setting###
        'cache_xauth': 'never',#'always','single-session'
        'virtual_adaptor': 'none', #'dhcp-and-manual','dhcp-only'
        'allow_connections_to': 'split-tunnels',#'this-gateway-only','all-secured-gateways'
        'default_route': False,
        'access_list': False,
        'simple_provisioning': False
    }
    
    default_ipv6_options = {
        'ipversion': 'ipv6',
        'type': 'site_to_site',   # only s2s type
        'name': '',
        'enable': True,
        'auth_mode': '',  # certificate or shared_secret
        'local_cert': '',  # only for certificate auth
        'secret': '',  # only for shared_secret auth
        'local_ike_type': '', # arg can be:default-id; distinguished_name; domain_name; email_id; ip
        'local_ike_id': '',
        'peer_ike_type': '',  # arg can be:distinguished_name; domain_name; email_id; ip
        'peer_ike_id': '',
        'pri_gate': '0.0.0.0',
        'sec_gate': '0.0.0.0',
        'local_net_type': '',  # name, group, host, network, range
        'remote_net_type': '',  # name, group, host, network, range
        'local_network': '',  # X0subnet, add_group, hostip, add_network, add_range
        'remote_network': '',  # add_remote_net, add_group, hostip, add_network, add_range
        ### proposal setting ######
        'ike_exchange': 'ikev2',  
        'ike_dh_group': '2',
        'ike_encryption': 'aes-128',
        'ike_auth': 'sha-1',
        'ike_lifetime': 28800,
        'ipsec_protocol': 'esp',
        'ipsec_encryption': 'aes_128',
        'ipsec_auth': 'sha_1',
        'ipsec_lifetime': 28800,
        'ipsec_pfs': False,
        'ipsec_pfs_dhgroup': 2,
        ## advanced setting #####
        'anti_replay': True,
        'ocsp_checking': False,
        'ocsp_resp_url': '',
        'management_https': False,
        'management_ssh': False,
        'management_snmp': False,
        'keep_alive': False,
        'allow_sonicpointn_layer3': False,
        'bound_to': ['interface', 'X1'],     ##['zone', 'WAN']
        'local_ip': ['primary', 'true'],       ##['primary', true]  or ['custom', '100.100.100.10']
        'suppress_trigger_packet': False,
        'accept_hash': False,
        'send_hash': '',
        ### manualkey auth proposal
        'in_spi': '0xa5ce265b',       ###  3-8 bit Hexa characters
        'out_spi': '0xed2fed7a',      ###  3-8 bit Hexa characters
        'in_encryption_key': '002ec148922d88453aa6e57da7e447b8',   ###  16 bit Hexa characters
        'in_authentication_key': '6e7ce00d48598dc0bf52279bddb8e41b5e805c70',    ### 40 bit Hexa characters     
        'out_encryption_key': '002ec148922d88453aa6e57da7e447b8',   ###  16 bit Hexa characters
        'out_authentication_key': '6e7ce00d48598dc0bf52279bddb8e41b5e805c70',    ### 40 bit Hexa characters     
    }

    default_edit_ipv4_options = {
        'ipversion': 'ipv4',
        'edit_auth': False,  
        'edit_network': False,  
        'edit_proposal': False,  
        'edit_advanced': False,
        'edit_applynat': False,    
    
    }

    default_edit_ipv6_options = {
        'ipversion': 'ipv6',
        'type': 'site_to_site',
        'ike_exchange': 'ikev2',  
        'edit_auth': False,  
        'edit_network': False,  
        'edit_proposal': False,  
        'edit_advanced': False,
        'edit_applynat': False,    
    
    }

    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/vpn/policies/ipv4/site-to-site'
        self.url_s2s = 'api/sonicos/vpn/policies/ipv4/site-to-site'
        self.url_group_vpn = 'api/sonicos/vpn/policies/ipv4/group-vpn'
        self.url_tunnel = 'api/sonicos/vpn/policies/ipv4/tunnel-interface'
        self.provision_server = 'api/sonicos/vpn/policies/ipv4/provision-server'
        self.provision_client = 'api/sonicos/vpn/policies/ipv4/provision-client'
        self.url_wangroup = 'api/sonicos/vpn/policies/ipv4/group-vpn/name/WAN%20GroupVPN'
        self.url_wlangroup = 'api/sonicos/vpn/policies/ipv4/group-vpn/name/WLAN%20GroupVPN'
        self.url_deleteall = 'api/sonicos/vpn/policies/ipv4/all'
        self.url_ipv6 = 'api/sonicos/vpn/policies/ipv6/site-to-site'
        self.url_raw = 'api/sonicos/raw'
        self.base = 'api/sonicos/vpn/base'
        self.url_cookie = 'api/sonicos/dynamic-file/getStatsData.json?restype=11&datatype=1'
        self.spi_url = "api/sonicos/dynamic-file/getStatsData.json?restype=11&datatype=1"
        self.stats_url = "api/sonicos/dynamic-file/getIpsecTunnelStats.json?spi=" 
        self.headers = OrderedDict([('Accept', 'application/json'),
                    ('Content-Type', 'application/json'),
                    ('Accept-Encoding', 'application/json'),
                    ('X-SNWL-API-Scope', 'extended'),
                    ('charset', 'UTF-8')])

        self.initial_s2svpn_json = {
            "vpn": {
                "policy": [{
                    "ipv4": {
                        "site_to_site": {
                            "name": "vpn1",
                            "enable": 'true',
                            "gateway": {
                                "primary": "0.0.0.0",
                                "secondary": ""
                            },
                            "auth_method": {
                                # "certificate": {
                                #     "certificate": "",
                                #     "ike_id": {
                                #         "local": "",
                                #         "peer": {
                                #             # "ip": ""
                                #         }
                                #     }
                                # }
                                # "shared_secret": {
                                #     "shared_secret": "password",
                                #     "ike_id": {
                                #         "local": {
                                #             "ipv4": "192.168.168.168"
                                #         },
                                #         "peer": {
                                #             "ipv4": "172.16.1.101"
                                #         }
                                #     }
                                # }
                            },
                            "network": {
                                "local": {
                                    # "": ""
                                },
                                "remote": {
                                    "destination_network": {
                                        # "": ""
                                    }
                                }
                            },
                            "proposal": {
                                "ike": {
                                    "exchange": "",
                                    "encryption": "",
                                    "authentication": "",
                                    "dh_group": "",
                                    "lifetime": ''
                                },
                                "ipsec": {
                                    "protocol": "esp",
                                    # "encryption": {
                                    #     "aes_128": True
                                    # },
                                    "authentication": {
                                        # "sha_1": True
                                    },
                                    "perfect_forward_secrecy": {
                                        # "dh_group": "19"
                                    },
                                    "lifetime": ''
                                }
                            },
                            "netbios": False,
                            "anti_replay": True,
                            "multicast": False,
                            # "ocsp_checking": {
                            #     # "responder_url": "http://www.sonicwall.com/ocsp"
                            # },

                            "management": {
                                "https": False,
                                "ssh": False,
                                "snmp": False
                            },
                            "user_login": {
                                "http": False,
                                "https": False
                            },
                            "default_lan_gateway": "0.0.0.0",
                            # "suppress_trigger_packet": False,     ### only for ikev2
                            # "accept_hash": False,                 ### only for ikev2
                            # "send_hash": "",                      ### only for ikev2
                            # "require_xauth": "Everyone",          ### only for main/aggressive
                            "apply_nat": False,
                            "keep_alive": False,
                            #"permit_acceleration": False,
                            #"allow_sonicpointn_layer3": False,
                            "bound_to": {
                                # "zone": "WAN"
                                "interface": "X1"
                            }
                        }
                    }
                }]
            }
}

        self.initial_s2svpn_manualauth_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "",
                                "enable": True,
                                "gateway": {
                                    "primary": ""
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        # "group": "All X0 Management IP"
                                    },
                                    "remote": {
                                        # "name": "IP Sec"
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "",
                                        # "encryption": {
                                        #     "aes_128": true
                                        # },
                                        "authentication": {
                                            # "sha_1": true
                                        },
                                        "in_spi": "aa1254cd",
                                        "out_spi": "acd",
                                        "encryption_key": "12345675678524521234567567852452",
                                        "authentication_key": "aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd"
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "bound_to": {
                                    "interface": "X1"
                                },
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                # "translated_network": {
                                #     "local": {
                                #         "name": "local_Tran"
                                #     },
                                #     "remote": {
                                #         "original": true
                                #     }
                                # },
                            }
                        }
                    }
                ]
            }
        }

        self.initial_tunnelvpn_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "tunnel_interface": {
                                "name": "",
                                "enable": 'true',
                                "gateway": {
                                    "primary": "0.0.0.0"
                                },
                                "auth_method": {
                                    # "certificate": {
                                    #     "certificate": "",
                                    #     "ike_id": {
                                    #         "local": "",
                                    #         "peer": {
                                    #             # "ip": ""
                                    #         }
                                    #     }
                                    # }
                                    # "shared_secret": {
                                    #     "shared_secret": "",
                                    #     "ike_id": {
                                    #         "local": {
                                    #             # "ipv4": "0.0.0.0"
                                    #         },
                                    #         "peer": {
                                    #             # "ipv4": "0.0.0.0"
                                    #         }
                                    #     }
                                    # }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "",
                                        "encryption": "",
                                        "authentication": "",
                                        "dh_group": "",
                                        "lifetime": ""
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        # "encryption": {
                                        #     # "aes_128": True,
                                        # },
                                        "authentication": {
                                            # "sha_1": True,
                                        },
                                        "perfect_forward_secrecy": {
                                            # "dh_group": "19"
                                        },
                                        "lifetime": ""
                                    }
                                },
                                "netbios": False,
                                "anti_replay": False,
                                # "wxa_group": "",
                                "multicast": False,
                                # "ocsp_checking": {
                                #     # "responder_url": "http://www.sonicwall.com/ocsp"
                                # },
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "keep_alive": False,
                                "allow_sonicpointn_layer3": False,
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "bound_to": {
                                    # "zone": "WAN"
                                    "interface": "X1"
                                },
                                # "suppress_trigger_packet": False,     ### only for ikev2
                                # "accept_hash": False,                 ### only for ikev2
                                # "send_hash": "",                      ### only for ikev2
                                "advanced_routing": False,
                                # "transport_mode": true                ### only for main/aggressive
                            }
                        }
                    }
                ]
            }
        }

        self.initial_tunnelvpn_manualauth_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "tunnel_interface": {
                                "name": "",
                                "enable": True,
                                "gateway": {
                                    "primary": ""
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "",
                                        # "encryption": {
                                        #     "aes_128": true
                                        # },
                                        "authentication": {
                                            # "sha_1": true
                                        },
                                        "in_spi": "aa1254cd",
                                        "out_spi": "acd",
                                        "encryption_key": "12345675678524521234567567852452",
                                        "authentication_key": "aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd"
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "bound_to": {
                                    "interface": "X1"
                                },
                            }
                        }
                    }
                ]
            }
        }

        self.initial_wangroup_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "group_vpn": {
                                "name": "WAN GroupVPN",
                                "enable": False,
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "526A8C405DAA9246"
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "encryption": "triple-des",
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800,
                                        "encryption": {
                                            # "aes_128": True
                                        },
                                        "authentication": {
                                            # "aes_xcbc": True
                                        }
                                    }
                                },
                                "anti_replay": True,
                                "permit_acceleration": False,
                                "multicast": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "accept_multiple_proposals": False,
                                "default_lan_gateway": "0.0.0.0",
                                "client": {
                                    "cache_xauth": "never",
                                    "virtual_adaptor": "none",
                                    "allow_connections_to": "split-tunnels",
                                    "default_route": False,
                                    "access_list": False,
                                    "simple_provisioning": False
                                },
                                "ike_mode_configuration": {},
                                "client_authentication": {
                                    "require_xauth": "Trusted Users"
                                }
                            }
                        }
                    }
                ]
            }
        }

        self.initial_ipv6_s2svpn_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "",
                                "enable": 'true',
                                "gateway": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "auth_method": {
                                    # "certificate": {
                                    #     "certificate": "",
                                    #     "ike_id": {
                                    #         "local": "",
                                    #         "peer": {
                                    #             # "ip": ""
                                    #         }
                                    #     }
                                    # }
                                    # "shared_secret": {
                                    #     "shared_secret": "",
                                    #     "ike_id": {
                                    #         "local": {
                                    #             # "ipv4": "0.0.0.0"
                                    #         },
                                    #         "peer": {
                                    #             # "ipv4": "0.0.0.0"
                                    #         }
                                    #     }
                                    # }
                                },
                                "network": {
                                    "local": {
                                        # "": ""
                                    },
                                    "remote": {
                                        # "": ""
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ike2",
                                        "encryption": "",
                                        "authentication": "",
                                        "dh_group": "",
                                        "lifetime": ""
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        # "encryption": {
                                        #     # "aes_128": True,
                                        # },
                                        "authentication": {
                                            # "sha_1": True,
                                        },
                                        "perfect_forward_secrecy": {
                                            # "dh_group": "19"
                                        },
                                        "lifetime": ""
                                    }
                                },
                                "anti_replay": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "keep_alive": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    # "zone": "WAN"
                                    "interface": "X1"
                                },
                                "local_ip": {
                                    # "primary": true
                                },
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                            #    "preempt_secondary_gateway": {
                                    # "interval": 120
                             #   }
                            },
                        }
                    }
                ]
            }
        }

        self.initial_ipv6_s2svpn_manualauth_json = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "",
                                "enable": True,
                                "gateway": {
                                    "primary": ""
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        # "group": "All X0 Management IP"
                                    },
                                    "remote": {
                                        # "name": "IP Sec"
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "",
                                        # "encryption": {
                                        #     "aes_128": true
                                        # },
                                        "authentication": {
                                            # "sha_1": true
                                        },
                                        "in_spi": "aa1254cd",
                                        "out_spi": "acd",
                                        "in_encryption_key": "12345675678524521234567567852452",
                                        "in_authentication_key": "aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd",
                                        "out_encryption_key": "12345675678524521234567567852452",
                                        "out_authentication_key": "aa1254cdaa1254cdaa1254cdaa1254cdaa1254cd"
                                    }
                                },
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                },
                            }
                        }
                    }
                ]
            }
        }

        self.renegotiateVpn_raw = {
            "stream": {
                "cgiaction": "ikeNegotiate",
                "ikeSrcAddrType": "4",
                "ikeSrcNet": "",
                "ikeSrcMask": "",
                "ikeDstAddrType": "",
                "ikeDstNet": "",
                "ikeDstMask": "",
                "ikeDstGw": "",
                "ikeDstGwPort": "500",
                "InitCookie": '3Ra1nzRdxX4%3D ',
                "ikeIsDhcpClient": "0",
                "ikeInSpi": '1'},
        }
        self.init_provision_server_json =  {
            "vpn":{
                "policy":[
                    {
                        "ipv4":{"provision_server":
                                {"name":"vpn_auto",
                                 "enable":True,
                                 "auth_method":{
                                    # "shared_secret":{
                                    #     "ap_client_id":"vpn_auto",
                                    #     "use_default_key":False,
                                    #     "shared_secret":"12345"
                                    #         }
                                        },
                                 "network":{
                                     "local":{
                                         "allow_unauthenticated":
                                         {
                                            #  "name":"X0 Subnet"
                                          }
                                         },
                                     "remote":{
                                        #  "destination_network":{
                                        #     #  "name":"remote_net"
                                        #      }
                                         }
                                        },
                                 "proposal":{
                                    "ike":{
                                        "exchange":"aggressive",
                                        "encryption":"aes-256",
                                        "authentication":"sha-1",
                                        "prf":"hmac-sha-256",
                                        "dh_group":"5",
                                        "lifetime":28800
                                        },
                                    "ipsec":{
                                        "protocol":"esp",
                                        "encryption":{
                                            "aes_gcm16_256":True
                                            },
                                        "authentication":{},
                                        "perfect_forward_secrecy":{},
                                        "lifetime":28800
                                        }
                                },
                                "anti_replay":True,
                                "multicast":False,
                                "management":{
                                    "https":False,
                                    "ssh":False,
                                    "snmp":False
                                    },
                                "user_login":{
                                    "http":False,
                                    "https":False
                                    },
                                "default_lan_gateway":"",
                                "permit_acceleration":False,
                                "allow_sonicpointn_layer3":False,
                                "bound_to":{"zone":"WAN"}
                                }
                            }
                        }
                    ]
                }
            }
        
        self.init_provision_client_json = {
            "vpn":{
                "policy":[
                    {
                        "ipv4":{
                            "provision_client":{
                                "name":"vpn_client",
                                "enable":True,
                                "gateway":{
                                    "primary":""
                                    },
                                "auth_method":{
                                    # "shared_secret":{
                                    #     "ap_client_id":"vpn_client",
                                    #     "use_default_key":False,
                                    #     "shared_secret":"12345"
                                    #     }
                                    },
                                "user_name":"",
                                "user_password":"12345"
                                }
                            }
                    }
                ]
            }
        }

    def add_vpn_policy(self, msg=False, **kwargs):
        self.options = dict(VpnbasesettingApi.default_ipv4_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = {}
        #  add site_to_site vpn policy
        if kwargs['type'] == 'site_to_site':
            self.url = self.url_s2s
            if kwargs['auth_mode'] in ['certificate', 'shared_secret']:
                json_input = self.build_json_s2svpn(**kwargs)
            elif kwargs['auth_mode'] == 'manual':
                json_input = self.build_json_s2svpn_manualauth(**kwargs)
        #  add tunnel_interface vpn policy
        elif kwargs['type'] == 'tunnel_interface':
            self.url = self.url_tunnel
            if kwargs['auth_mode'] in ['certificate', 'shared_secret']:
                json_input = self.build_json_tunnelvpn(**kwargs)
            elif kwargs['auth_mode'] == 'manual':
                json_input = self.build_json_tunnelvpn_manualauth(**kwargs)
        elif kwargs['type'] == 'provision_client':
            self.url = self.provision_client
            json_input =  self.build_json_provision_client(**kwargs)
        elif kwargs['type'] == 'provision_server':
            self.url = self.provision_server
            json_input =  self.build_json_provision_server(**kwargs)
        addvpnpolicy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return addvpnpolicy_resp

    def edit_vpn_policy(self, msg=False, **kwargs):
        self.options = dict(VpnbasesettingApi.default_edit_ipv4_options)
        self.options.update(kwargs)
        kwargs = self.options
        if 'type' in kwargs and 'name' in kwargs:
            json_input = self.build_json_editvpn(**kwargs)
            if kwargs['type'] == 'site_to_site':
                self.url = self.url_s2s + '/name/' + kwargs['name']
            elif kwargs['type'] == 'tunnel_interface':
                self.url = self.url_tunnel + '/name/' + kwargs['name']
            logger.info(self.url)
            editvpnpolicy_resp = self.fw.api_put(self.url, msg, data=json_input)
            return editvpnpolicy_resp
        else:
            logger.error('vpn type and vpn initial name must be specified')
            return False

    def edit_provision_vpn_policy(self, msg=False, **kwargs):
        if kwargs['type'] == 'provision_client':
            url = self.provision_client + '/name/' + kwargs['name']
            json_input =  self.build_json_provision_client(**kwargs)
        elif kwargs['type'] == 'provision_server':
            url = self.provision_server + '/name/' + kwargs['name']
            json_input =  self.build_json_provision_server(**kwargs)
        resp = self.fw.api_put(url, msg, data=json_input)
        return resp
        
    def config_vpn_base(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        app_setting_resp = self.fw.api_put(self.base, msg, data=json_input)
        return app_setting_resp

    def show_vpn_base(self):
        resp = self.fw.api_get(self.base)
        return resp
        
    def show_dhcp_over_vpn(self):
        url = 'api/sonicos/vpn/dhcp-over-vpn/base/global'
        resp = self.fw.api_get(url)
        return resp

    def show_L2TPServer_part(self):
        url = 'api/sonicos/reporting/l2tp-server/sessions'
        resp = self.fw.api_get(url)
        return resp

    def edit_wangroup_vpn_policy(self, msg=False, **kwargs):
        self.options = dict(VpnbasesettingApi.default_wangroup_options)
        self.options.update(kwargs)
        kwargs = self.options
        self.url = self.url_wangroup
        json_input = self.build_json_wangroup_vpn(**kwargs)
        edit_wangroup_resp = self.fw.api_put(self.url, msg, data=json_input)
        return edit_wangroup_resp

    def edit_wlangroup_vpn_policy(self, msg=False, **kwargs):
        wlangroup_dict = copy.deepcopy(self.default_wangroup_options)
        wlangroup_dict.update(kwargs)
        json_input = self.build_json_wangroup_vpn(**wlangroup_dict)
        edit_wlangroup_resp = self.fw.api_put(self.url_wlangroup, msg, data=json_input)
        return edit_wlangroup_resp   

    def add_ipv6_vpn_policy(self, msg=False, **kwargs):
        self.options = dict(VpnbasesettingApi.default_ipv6_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = {}
        ### add ipv6 site_to_site vpn policy
        self.url = self.url_ipv6
        if kwargs['auth_mode'] == 'certificate' or kwargs['auth_mode'] == 'shared_secret':
            json_input = self.build_json_ipv6_s2svpn(**kwargs)
        elif kwargs['auth_mode'] == 'manual':
            json_input = self.build_json_ipv6_s2svpn_manualauth(**kwargs)
        addipv6vpnpolicy_resp = self.fw.api_post(self.url, msg, data=json_input)
        return addipv6vpnpolicy_resp

    def edit_ipv6_vpn_policy(self, msg=False, **kwargs):
        self.options = dict(VpnbasesettingApi.default_edit_ipv6_options)
        self.options.update(kwargs)
        kwargs = self.options
        if 'type' in kwargs and 'name' in kwargs:
            json_input = self.build_json_ipv6_editvpn(**kwargs)
            self.url = self.url_ipv6 + '/name/' + kwargs['name']
            logger.info(self.url)
            ipv6_editvpnpolicy_resp = self.fw.api_put(self.url, msg, data=json_input)
            return ipv6_editvpnpolicy_resp
        else:
            logger.error('ipv6 vpn type and vpn initial name must be specified')
            return False
        
    def config_ipv6_vpn_policy(self, msg=False, name = None, **kwargs):
        url = self.url_ipv6 + '/name/' + name
        logger.info(url)
        json_output = self.fw.api_get(url)
        logger.info(json_output)
        if 'enable' in kwargs:
            json_output['vpn']['policy'][0]['ipv6']['site_to_site']['enable'] = kwargs['enable']
        resp = self.fw.api_put(url, msg, data=json_output)
        return resp
        

    def show_s2svpnpolicy(self):      
        s2svpnpolicy_output = self.fw.api_get(self.url_s2s)
        return s2svpnpolicy_output

    def show_tunnelvpnpolicy(self):      
        tunnelvpnpolicy_output = self.fw.api_get(self.url_tunnel)
        return tunnelvpnpolicy_output
        
    def show_all_vpn_policies(self, msg=False):
        output = self.fw.api_get(self.url_group_vpn, msg)
        return output

    def show_wangroup_vpn(self):      
        s2svpnpolicy_output = self.fw.api_get(self.url_wangroup)
        return s2svpnpolicy_output

    def show_ipv6vpnpolicy(self):      
        ipv6vpnpolicy_output = self.fw.api_get(self.url_ipv6)
        return ipv6vpnpolicy_output

    def del_s2svpn_policy(self, msg=False, **kwargs):
        logger.info("delete s2svpn policy")
        self.url = self.url_s2s
        json_input = {"vpn": {"policy": [{"ipv4": {"site_to_site": {"name": ""}}}]}}
        json_input['vpn']['policy'][0]['ipv4']['site_to_site']['name'] = kwargs['name']       
        dels2svpn_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return dels2svpn_resp

    def del_tunnelvpn_policy(self, msg=False, **kwargs):
        logger.info("delete tunnelvpn policy")
        self.url = self.url_tunnel
        json_input = {"vpn": {"policy": [{"ipv4": {"tunnel_interface": {"name": ""}}}]}}
        json_input['vpn']['policy'][0]['ipv4']['tunnel_interface']['name'] = kwargs['name']       
        deltunnelvpn_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return deltunnelvpn_resp

    def del_provision_server(self, msg=False, **kwargs):
        logger.info("delete provision server  vpn policy")
        url = self.provision_server + '/name/' + kwargs['name']
        resp = self.fw.api_delete(url, msg)
        return resp
    
    def del_provision_client(self, msg=False, **kwargs):
        logger.info("delete provision client  vpn policy")
        url = self.provision_client + '/name/' + kwargs['name']
        resp = self.fw.api_delete(url, msg)
        return resp

    def del_ipv6_vpn_policy(self, msg=False, **kwargs):
        logger.info("delete vpn policy")
        self.url = self.url_ipv6
        json_input = {"vpn": {"policy": [{"ipv6": {"site_to_site": {"name": ""}}}]}}
        json_input['vpn']['policy'][0]['ipv6']['site_to_site']['name'] = kwargs['name']       
        delipv6vpn_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return delipv6vpn_resp   

    def del_all_vpn_policies(self, msg=False):
        self.url = self.url_deleteall
        output = self.fw.api_delete(self.url, msg, data={})
        return output

    def del_all_ipv6_vpn_policies(self, msg=False):
        url = 'api/sonicos/vpn/policies/ipv6/all'
        output = self.fw.api_delete(url, msg, data={})
        return output

    def dis_tunnelvpn_policy(self, msg=False, **kwargs):
        logger.info("disable tunnelvpn policy")
        self.url = self.url_tunnel + '/name/' + kwargs['name']
        json_input={
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "tunnel_interface": {
                                "name": "",
                                "enable": False,
                                
                            }
                        }
                    }
                ]
            }
        }
        json_input['vpn']['policy'][0]['ipv4']['tunnel_interface']['name'] = kwargs['name']       
        json_input['vpn']['policy'][0]['ipv4']['tunnel_interface']['enable'] = False      
        distunnelvpn_resp = self.fw.api_put(self.url, msg, data=json_input)
        return distunnelvpn_resp

    def en_tunnelvpn_policy(self, msg=False, **kwargs):
        logger.info("enable tunnelvpn policy")
        self.url = self.url_tunnel + '/name/' + kwargs['name']
        json_input={
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "tunnel_interface": {
                                "name": "",
                                "enable": True,
                                
                            }
                        }
                    }
                ]
            }
        }
        json_input['vpn']['policy'][0]['ipv4']['tunnel_interface']['name'] = kwargs['name']       
        json_input['vpn']['policy'][0]['ipv4']['tunnel_interface']['enable'] = True      
        entunnelvpn_resp = self.fw.api_put(self.url, msg, data=json_input)
        return entunnelvpn_resp

    def dis_s2svpn_policy(self, msg=False, **kwargs):
        logger.info("disable s2s policy")
        self.url = self.url_s2s + '/name/' + kwargs['name']
        json_input={
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "",
                                "enable": False,
                                
                            }
                        }
                    }
                ]
            }
        }
        json_input['vpn']['policy'][0]['ipv4']['site_to_site']['name'] = kwargs['name']
        json_input['vpn']['policy'][0]['ipv4']['site_to_site']['enable'] = False
        dis_s2svpn_resp = self.fw.api_put(self.url, msg, data=json_input)
        return dis_s2svpn_resp

    def en_s2svpn_policy(self, msg=False, **kwargs):
        logger.info("enable s2s policy")
        self.url = self.url_s2s + '/name/' + kwargs['name']
        json_input={
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "",
                                "enable": True,
                                
                            }
                        }
                    }
                ]
            }
        }
        json_input['vpn']['policy'][0]['ipv4']['site_to_site']['name'] = kwargs['name']
        json_input['vpn']['policy'][0]['ipv4']['site_to_site']['enable'] = True
        en_s2svpn_resp = self.fw.api_put(self.url, msg, data=json_input)
        return en_s2svpn_resp

    def build_json_s2svpn(self, **kwargs):
        json_input = copy.deepcopy(self.initial_s2svpn_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            path['gateway']['secondary'] = kwargs['sec_gate']
            #### config certificate/shared_secret auth mode
            json_input = self._build_json_vpn_authmode(kwargs, json_input)
            ### config s2s local&remote network
            json_input = self._build_json_vpn_network(kwargs, json_input)
            ### config s2s proposal
            json_input = self._build_json_vpn_proposal(kwargs, json_input)
            ### config s2s advanced
            json_input = self._build_json_vpn_advanced(kwargs, json_input)
            if kwargs['remote_net_type'] == 'dhcp':
                del json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['keep_alive']
        except KeyError:
            logger.error("Error: In creating JSON for s2svpn")   
        logger.info("s2svpn json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_s2svpn_manualauth(self, **kwargs):
        json_input = copy.deepcopy(self.initial_s2svpn_manualauth_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            path= json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            #### config manualkey auth mode
            path['auth_method']['manual_key'] = True
            ### config s2s local&remote network
            json_input = self._build_json_vpn_network(kwargs, json_input)
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            ### config s2s proposal with manualkey auth
            path['proposal']['ipsec']['protocol'] = kwargs['ipsec_protocol']
            if kwargs['ipsec_protocol'] == 'esp':
                path['proposal']['ipsec']['encryption'] = {}
                path['proposal']['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            path['proposal']['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            path['proposal']['ipsec']['in_spi'] = kwargs['in_spi']
            path['proposal']['ipsec']['out_spi'] = kwargs['out_spi']
            path['proposal']['ipsec']['encryption_key'] = kwargs['encryption_key']
            path['proposal']['ipsec']['authentication_key'] = kwargs['authentication_key']
            ### config s2s advanced with manualkey auth
            path['netbios'] = kwargs['netbios']
            # path['wxa_group'] = kwargs['wxa_group']
            path['management']['https'] = kwargs['management_https']
            path['management']['ssh'] = kwargs['management_ssh']
            path['management']['snmp'] = kwargs['management_snmp']
            path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
            path['user_login']['http'] = kwargs['user_login_http']
            path['user_login']['https'] = kwargs['user_login_https']
            path['default_lan_gateway'] = kwargs['default_lan_gateway']
            if 'bound_to' in kwargs:
                path['bound_to'] = {}
                path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
            path['suppress_auto_add_rule'] = kwargs['suppress_auto_add_rule']
            json_input['vpn']['policy'][0]['ipv4'][kwargs['type']] = path
            ###config apply_nat
            path['apply_nat'] = kwargs['apply_nat']
            if kwargs['apply_nat']:
                logger.info("build json vpn applynat")
                json_input = self._build_json_vpn_applynat(kwargs, json_input)
        except KeyError:
            logger.error("Error: In creating JSON for s2svpn manualkey authmode")
        logger.info("s2svpn manualkey authmode json obtained")
        logger.info(json_input)      
        return json_input        

    def build_json_tunnelvpn(self, **kwargs):
        json_input = copy.deepcopy(self.initial_tunnelvpn_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            #### config certificate/shared_secret auth mode
            json_input = self._build_json_vpn_authmode(kwargs, json_input)
            ### config s2s proposal
            json_input = self._build_json_vpn_proposal(kwargs, json_input)
            ### config s2s advanced
            json_input = self._build_json_vpn_advanced(kwargs, json_input)
        except KeyError:
            logger.error("Error: In creating JSON for tunnelvpn")   
        logger.info("tunnelvpn json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_tunnelvpn_manualauth(self, **kwargs):
        json_input = copy.deepcopy(self.initial_tunnelvpn_manualauth_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            #### config manualkey auth mode
            path['auth_method']['manual_key'] = True
            ### config s2s proposal with manualkey auth 
            path['proposal']['ipsec']['protocol'] = kwargs['ipsec_protocol']
            if kwargs['ipsec_protocol'] == 'esp':
                path['proposal']['ipsec']['encryption'] = {}
                path['proposal']['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            path['proposal']['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            path['proposal']['ipsec']['in_spi'] = kwargs['in_spi']
            path['proposal']['ipsec']['out_spi'] = kwargs['out_spi']
            path['proposal']['ipsec']['encryption_key'] = kwargs['encryption_key']
            path['proposal']['ipsec']['authentication_key'] = kwargs['authentication_key']
            ### config s2s advanced with manualkey auth 
            path['netbios'] = kwargs['netbios']
            # path['wxa_group'] = kwargs['wxa_group']
            path['management']['https'] = kwargs['management_https']
            path['management']['ssh'] = kwargs['management_ssh']
            path['management']['snmp'] = kwargs['management_snmp']
            path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
            path['user_login']['http'] = kwargs['user_login_http']
            path['user_login']['https'] = kwargs['user_login_https']
            if 'bound_to' in kwargs:
                path['bound_to'] = {}
                path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
            path['apply_nat'] = kwargs['apply_nat']
        except KeyError:
            logger.error("Error: In creating JSON for tunnelvpn manualkey authmode")   
        logger.info("tunnelvpn manualkey authmode json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_ipv6_s2svpn(self, **kwargs):
        json_input = copy.deepcopy(self.initial_ipv6_s2svpn_json)
        logger.info(kwargs)
        try:
            ### ipv6 vpn base setting
            path = json_input['vpn']['policy'][0]['ipv6']['site_to_site']
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            path['gateway']['secondary'] = kwargs['sec_gate']
            #### config ipv6 certificate/shared_secret auth mode
            json_input = self._build_json_vpn_authmode(kwargs, json_input)
            ### config ipv6 s2s local&remote network
            json_input = self._build_json_vpn_network(kwargs, json_input)
            ### config ipv6 s2s proposal
            json_input = self._build_json_vpn_proposal(kwargs, json_input)
            ### config ipv6 s2s advanced
            t_path = json_input['vpn']['policy'][0]['ipv6'][kwargs['type']]
            t_path['anti_replay'] = kwargs['anti_replay']
            t_path['management']['https'] = kwargs['management_https']
            t_path['management']['ssh'] = kwargs['management_ssh']
            t_path['management']['snmp'] = kwargs['management_snmp']
            t_path['keep_alive'] = kwargs['keep_alive']
            t_path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
            if 'bound_to' in kwargs:
                t_path['bound_to'] = {}
                t_path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
            if kwargs['local_ip'][0] == 'primary':
                t_path['local_ip'][kwargs['local_ip'][0]] = True
            elif kwargs['local_ip'][0] == 'custom':
                t_path['local_ip'][kwargs['local_ip'][0]] = kwargs['local_ip'][-1]
            t_path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
            t_path['accept_hash'] = kwargs['accept_hash']
            t_path['send_hash'] = kwargs['send_hash']
        except KeyError:
            logger.error("Error: In creating JSON for ipv6 s2svpn")   
        logger.info("ipv6 s2svpn json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_ipv6_s2svpn_manualauth(self, **kwargs):
        json_input = copy.deepcopy(self.initial_ipv6_s2svpn_manualauth_json)
        logger.info(kwargs)
        try:
            ### ipv6 vpn base setting
            path = json_input['vpn']['policy'][0]['ipv6']['site_to_site']
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            #### config ipv6 vpn manualkey auth mode
            path['auth_method']['manual_key'] = True
            ### config ipv6vpn s2s local&remote network
            json_input = self._build_json_vpn_network(kwargs, json_input)
            ### config ipv6vpn s2s proposal with manualkey auth 
            path['proposal']['ipsec']['protocol'] = kwargs['ipsec_protocol']
            if kwargs['ipsec_protocol'] == 'esp':
                path['proposal']['ipsec']['encryption'] = {}
                path['proposal']['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            path['proposal']['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            path['proposal']['ipsec']['in_spi'] = kwargs['in_spi']
            path['proposal']['ipsec']['out_spi'] = kwargs['out_spi']
            path['proposal']['ipsec']['in_encryption_key'] = kwargs['in_encryption_key']
            path['proposal']['ipsec']['in_authentication_key'] = kwargs['in_authentication_key']
            path['proposal']['ipsec']['out_encryption_key'] = kwargs['out_encryption_key']
            path['proposal']['ipsec']['out_authentication_key'] = kwargs['out_authentication_key']
            ### config ipv6vpn s2s advanced with manualkey auth 
            path['management']['https'] = kwargs['management_https']
            path['management']['ssh'] = kwargs['management_ssh']
            path['management']['snmp'] = kwargs['management_snmp']
            path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
            if 'bound_to' in kwargs:
                path['bound_to'] = {}
                path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]

        except KeyError:
            logger.error("Error: In creating JSON for ipv6 s2svpn manualkey authmode")   
        logger.info("ipv6 s2svpn manualkey authmode json obtained")
        logger.info(json_input)      
        return json_input     

    def build_json_editvpn(self, **kwargs):
        json_input = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            # "tunnel/site_to_site": {
                            #     "name": ""
                            # }
                        }
                    }
                ]
            }
        }
        logger.info(kwargs)

        # try:
        json_input['vpn']['policy'][0]['ipv4'][kwargs['type']] = {}
        path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]

        path['name'] = kwargs['name']
        if kwargs['type'] == 'site_to_site':                ### edit sec gateway
            if 'enable' in kwargs:
                json_input['vpn']['policy'][0]['ipv4']['site_to_site']['enable'] = kwargs['enable']
            if 'pri_gate' in kwargs or 'sec_gate' in kwargs:
                json_input['vpn']['policy'][0]['ipv4']['site_to_site']['gateway'] = {}
                if 'sec_gate' in kwargs:
                    path['gateway']['secondary'] = kwargs['sec_gate']
            json_input['vpn']['policy'][0]['ipv4'][kwargs['type']] = path
            ### edit s2s local&remote network
            if kwargs['edit_network']:
                json_input = self._edit_json_vpn_network(kwargs, json_input)
        elif kwargs['type'] == 'tunnel_interface':
            if kwargs['auth_mode'] in ['certificate', 'shared_secret']:
                json_input = self.build_json_tunnelvpn(**kwargs)
            elif kwargs['auth_mode'] == 'manual':
                json_input = self.build_json_tunnelvpn_manualauth(**kwargs)

        path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
        ### vpn base setting
        if 'new_name' in kwargs:
            path['name'] = kwargs['new_name']
        if 'enable' in kwargs:
            path['enable'] = kwargs['enable']
        if 'pri_gate' in kwargs:
            path['gateway'] = {}
            path['gateway']['primary'] = kwargs['pri_gate']
        if 'netbios'  in kwargs:
            path['netbios'] = kwargs['netbios']
        logger.info(path)
        #### edit certificate/shared_secret auth mode
        if kwargs['edit_auth']:
            json_input = self._edit_json_vpn_authmode(kwargs, json_input)
        ### edit s2s proposal
        if kwargs['edit_proposal']:
            json_input = self._edit_json_vpn_proposal(kwargs, json_input)
        ### edit s2s advanced
        if kwargs['edit_advanced']:
            json_input = self._edit_json_vpn_advanced(kwargs, json_input)
        # except KeyError:
        #     logger.error("Error: In creating JSON for editvpn")
        logger.info("editvpn json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_wangroup_vpn(self, **kwargs):
        json_input = self.initial_wangroup_json
        path = json_input['vpn']['policy'][0]['ipv4']['group_vpn']
        try:
            path['enable'] = kwargs['enable']
            #### edit auth method
            path['auth_method'] = kwargs['auth_mode']
            if kwargs['auth_mode'] == 'shared_secret':
                path['auth_method']={}
                path['auth_method']['shared_secret']={}
                path['auth_method']['shared_secret']['shared_secret'] = kwargs['secret']
                logger.info('1111111')

            elif kwargs['auth_mode'] == 'certificate':
                path['certificate']['certificate'] = kwargs['local_cert']
                path['certificate']['ike_id']['peer'][kwargs['peer_ike_type']] = kwargs['peer_ike_id']
            else:
                logger.error('Pls enter correct auth_mode')
            #### edit proposal
            path['proposal']['ike']['encryption'] = kwargs['ike_encryption']
            path['proposal']['ike']['authentication'] = kwargs['ike_auth']
            path['proposal']['ike']['dh_group'] = kwargs['ike_dh_group']
            path['proposal']['ike']['lifetime'] = kwargs['ike_lifetime']

            path['proposal']['ipsec']['protocol'] = kwargs['ipsec_protocol']
            if kwargs['ipsec_pfs']:
                 path['proposal']['ipsec']['perfect_forward_secrecy'][
                 'dh_group'] = kwargs['ipsec_pfs_dhgroup']               
            path['proposal']['ipsec']['lifetime'] = kwargs['ipsec_lifetime']
            path['proposal']['ipsec']['encryption'] = {}
            path['proposal']['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            path['proposal']['ipsec']['authentication'] = {}
            path['proposal']['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            #### edit advanced
            path['anti_replay'] = kwargs['anti_replay']
            path['permit_acceleration'] = kwargs['permit_acceleration']
            path['multicast'] = kwargs['multicast']
            path['management']['https'] = kwargs['management_https']
            path['management']['ssh'] = kwargs['management_ssh']
            path['management']['snmp'] = kwargs['management_snmp']
            path['accept_multiple_proposals'] = kwargs['accept_multiple_proposals']
            path['default_lan_gateway'] = kwargs['default_lan_gateway']

            ####edit client_authentication     
            #'client_authentication': '{"allow_unauthenticated":{"name":"Firewalled Subnets"}}"}'}
            #"client_authentication": { "require_xauth": "Trusted Users"}
            if kwargs['client_authentication']:
                path['client_authentication'] = {}
                if kwargs['client_authentication'] == 'allow_unauthenticated':
                    path['client_authentication']['allow_unauthenticated'] = {}
                    path['client_authentication']['allow_unauthenticated']['group'] = kwargs['unauthenticated_group']
                elif kwargs['client_authentication'] == 'require_xauth':
                    path['client_authentication']['require_xauth'] = kwargs['xauth']
                else:
                    logger.error('Pls enter correct client_authentication')

        ####edit client

            path['client']['cache_xauth'] = kwargs['cache_xauth']
            path['client']['virtual_adaptor'] = kwargs['virtual_adaptor']
            path['client']['allow_connections_to'] = kwargs['allow_connections_to']
            path['client']['default_route'] = kwargs['default_route']
            path['client']['access_list'] = kwargs['access_list']
            path['client']['simple_provisioning'] = kwargs['simple_provisioning']


        except KeyError:
            logger.error("Error: In creating JSON for wangroup vpn policy")   
        logger.info("wangroup json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_ipv6_editvpn(self, **kwargs):
        json_input = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                # "name": ""
                            }
                        }
                    }
                ]
            }
        }
        logger.info(kwargs)
        try:
            path = json_input['vpn']['policy'][0]['ipv6']['site_to_site']
            path['name'] = kwargs['name']
            ### edit ipv6 vpn base setting
            if 'new_name' in kwargs:
                path['name'] = kwargs['new_name']
            if 'pri_gate' in kwargs or 'sec_gate' in kwargs:
                path['gateway'] = {}
                if 'pri_gate' in kwargs:
                    path['gateway']['primary'] = kwargs['pri_gate']
                if 'sec_gate' in kwargs:
                    path['gateway']['secondary'] = kwargs['sec_gate']
            ### edit local&remote network
            if kwargs['edit_network']:
                json_input = self._edit_json_vpn_network(kwargs, json_input)
            #### edit certificate/shared_secret auth mode
            if kwargs['edit_auth']:
                json_input = self._edit_json_vpn_authmode(kwargs, json_input)
            ### edit s2s proposal
            if kwargs['edit_proposal']:
                json_input = self._edit_json_vpn_proposal(kwargs, json_input)
            ### edit s2s advanced
            if kwargs['edit_advanced']:
                if 'auth_mode' not in kwargs:
                    logger.error('vpn auth_mode must be specified when edit vpn advanced')
                    return False
                if 'management_https' in kwargs or 'management_ssh' in kwargs or 'management_snmp' in kwargs:
                    path['management'] = {}
                    if 'management_https' in kwargs:
                        path['management']['https'] = kwargs['management_https']
                    if 'management_ssh' in kwargs:
                        path['management']['ssh'] = kwargs['management_ssh']
                    if 'management_snmp' in kwargs:
                        path['management']['snmp'] = kwargs['management_snmp']
                if 'allow_sonicpointn_layer3' in kwargs:
                    path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
                if 'bound_to' in kwargs:
                    path['bound_to'] = {}
                    path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                if kwargs['auth_mode'] == 'certificate' or kwargs['auth_mode'] == 'shared_secret':
                    t_path = json_input['vpn']['policy'][0]['ipv6'][kwargs['type']]
                    if 'anti_replay' in kwargs:
                        t_path['anti_replay'] = kwargs['anti_replay']
                    if 'keep_alive' in kwargs:
                        t_path['keep_alive'] = kwargs['keep_alive']
                    if 'local_ip' in kwargs:
                        if kwargs['local_ip'][0] == 'primary':
                            t_path['local_ip'][kwargs['local_ip'][0]] = True
                        elif kwargs['local_ip'][0] == 'custom':
                            t_path['local_ip'][kwargs['local_ip'][0]] = kwargs['local_ip'][-1]
                    if 'suppress_trigger_packet' in kwargs:
                        t_path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
                    if 'accept_hash' in kwargs:
                        t_path['accept_hash'] = kwargs['accept_hash']
                    if 'send_hash' in kwargs:
                        t_path['send_hash'] = kwargs['send_hash']
        except KeyError:
            logger.error("Error: In creating JSON for editvpn")
        logger.info("editvpn json obtained")   
        logger.info(json_input)      
        return json_input

    def build_json_provision_client(self, **kwargs):
        json_input = copy.deepcopy(self.init_provision_client_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
            path['gateway']['primary'] = kwargs['pri_gate']
            path['user_name'] = kwargs['user_name']
            path['user_password'] = kwargs['user_password']
            if kwargs['auth_mode'] == 'shared_secret':
                path['auth_method']['shared_secret'] = {}
                path['auth_method']['shared_secret']['ap_client_id'] = kwargs['ap_client_id']
                path['auth_method']['shared_secret']['use_default_key'] = kwargs['use_default_key']
                path['auth_method']['shared_secret']['shared_secret'] = kwargs['secret']
            elif kwargs['auth_mode'] == 'certificate':
                path['auth_method']['certificate'] = {}
                path['auth_method']['certificate']['certificate'] = kwargs['local_cert']
        except KeyError:
            logger.error("Error: In creating JSON for provision client ")   
        logger.info("provision client json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_provision_server(self, **kwargs):
        json_input = copy.deepcopy(self.init_provision_server_json)
        logger.info(kwargs)
        try:
            ### vpn base setting
            json_input = self._build_json_vpn_network(kwargs, json_input)
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['name'] = kwargs['name']
            path['enable'] = kwargs['enable']
    
            if kwargs['auth_mode'] == 'shared_secret':
                path['auth_method']['shared_secret'] = {}
                path['auth_method']['shared_secret']['ap_client_id'] = kwargs['ap_client_id']
                path['auth_method']['shared_secret']['use_default_key'] = kwargs['use_default_key']
                path['auth_method']['shared_secret']['shared_secret'] = kwargs['secret']
            elif kwargs['auth_mode'] == 'certificate':
                # pass
                path['auth_method']['certificate'] = {}
                path['auth_method']['certificate']['certificate'] = kwargs['local_cert']
                path['auth_method']['certificate']['client_id']={}
                path['auth_method']['certificate']['client_id']['peer']={}
                if 'domain_name' in kwargs.keys():
                    path['auth_method']['certificate']['client_id']['peer']['domain_name']=kwargs['domain_name']
                elif 'email_id' in kwargs.keys():
                    path['auth_method']['certificate']['client_id']['peer']['email_id']=kwargs['email_id']
                elif 'peer_ip' in kwargs.keys():
                    path['auth_method']['certificate']['client_id']['peer']['ip']=kwargs['peer_ip']
                elif 'distinguished_name' in kwargs.keys():
                    path['auth_method']['certificate']['client_id']['peer']['distinguished_name']=kwargs['distinguished_name']
        except KeyError:
            logger.error("Error: In creating JSON for provision server ")   
        logger.info("provision server json obtained")
        logger.info(json_input)      
        return json_input

    def _build_json_vpn_authmode(self, kwargs, json_vpn_authmode_input):
        json_input = copy.deepcopy(json_vpn_authmode_input)
        try:
            path =json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['auth_method']
            if kwargs['auth_mode'] == 'certificate':
                path['certificate'] = {}
                path['certificate']['certificate'] = kwargs['local_cert']
                path['certificate']['ike_id'] = {}
                path['certificate']['ike_id']['local'] = kwargs['local_ike_type']
                path['certificate']['ike_id']['peer'] = {}
                path['certificate']['ike_id']['peer'][kwargs['peer_ike_type']] = kwargs['peer_ike_id']
                ### config ocsp
                if kwargs['ocsp_checking'] and kwargs['ipversion'] == 'ipv4':
                    json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['ocsp_checking'] = {}
                    json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['ocsp_checking']['responder_url'] = kwargs['ocsp_resp_url']
            elif kwargs['auth_mode'] == 'shared_secret':
                path['shared_secret'] = {}
                path['shared_secret']['shared_secret'] = kwargs['secret']
                path['shared_secret']['ike_id'] = {}
                path['shared_secret']['ike_id']['local'] = {}
                path['shared_secret']['ike_id']['local'][kwargs['local_ike_type']] = kwargs['local_ike_id']
                path['shared_secret']['ike_id']['peer'] = {}
                path['shared_secret']['ike_id']['peer'][kwargs['peer_ike_type']] = kwargs['peer_ike_id']
        except KeyError:
            logger.error("Error: In creating JSON for vpn authmode")   
        logger.info("vpn authmode json obtained")
        return json_input

    def _build_json_vpn_network(self, kwargs, json_vpn_network_input):
        json_input = copy.deepcopy(json_vpn_network_input)
        try:
            if kwargs['type'] == 'provision_server':
                local_path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]['network']['local']['allow_unauthenticated']
            else:
                local_path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local']
            if kwargs['local_net_type'] == 'name':
                local_path['name'] = kwargs['local_net_name']
            elif kwargs['local_net_type'] == 'group':
                local_path['group'] = kwargs['local_net_group']
            elif kwargs['local_net_type'] == 'host':
                local_path['host'] = kwargs['local_net_host']
            elif kwargs['local_net_type'] == 'network':
                local_path['network']['subnet'] = kwargs['local_net_network'][0]
                local_path['network']['mask'] = kwargs['local_net_network'][1]
            elif kwargs['local_net_type'] == 'range':
                local_path['range']['begin'] = kwargs['local_net_range'][0]
                local_path['range']['end'] = kwargs['local_net_range'][1]
            elif kwargs['local_net_type'] == 'any':
                local_path['any'] = True
            elif kwargs['local_net_type'] == 'dhcp':
                local_path['dhcp'] = True
            if kwargs['type'] == 'provision_server':
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local']['allow_unauthenticated'] = local_path
            else:
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local'] = local_path

            remote_path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['remote']
            remote_path['destination_network'] = {}
            if kwargs['remote_net_type'] == 'name':
                # remote_path['destination_network'] = {}
                remote_path['destination_network']['name'] = kwargs['remote_net_name']
            elif kwargs['remote_net_type'] == 'group':
                remote_path['destination_network']['group'] = kwargs['remote_net_group']
            elif kwargs['remote_net_type'] == 'host':
                remote_path['destination_network']['host'] = kwargs['remote_net_host']
            elif kwargs['remote_net_type'] == 'network':
                remote_path['destination_network']['network']['subnet'] = kwargs['remote_net_network'][0]
                remote_path['destination_network']['network']['mask'] = kwargs['remote_net_network'][1]
            elif kwargs['remote_net_type'] == 'range':
                remote_path['destination_network']['range']['begin'] = kwargs['remote_net_range'][0]
                remote_path['destination_network']['range']['end'] = kwargs['remote_net_range'][1]
            elif kwargs['remote_net_type'] == 'any':
                remote_path['any'] = True
            # elif kwargs['remote_net_type'] == 'dhcp':
            #     remote_path['destination_network']['dhcp'] = True
            elif kwargs['remote_net_type'] == 'dhcp':
                del remote_path['destination_network']
                remote_path['dhcp'] = True
            elif kwargs['remote_net_type'] == 'pool':
                del remote_path['destination_network']
                remote_path['ikev2_ip_pool'] = {}
                remote_path['ikev2_ip_pool']['name'] = kwargs['remote_net_name']
            json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['remote'] = remote_path

        except KeyError:
            logger.error("Error: In creating JSON for vpn network")
        logger.info("vpn network json obtained")
        logger.info('/' * 50)
        logger.info(json_input)
        return json_input

    def _build_json_vpn_proposal(self, kwargs, json_vpn_proposal_input):
        json_input = copy.deepcopy(json_vpn_proposal_input)
        try:
            path =json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['proposal']
            path['ike']['exchange'] = kwargs['ike_exchange']
            path['ike']['encryption'] = kwargs['ike_encryption']
            path['ike']['authentication'] = kwargs['ike_auth']
            if path['ike']['encryption'] in ['aes-gcm16-128', 'aes-gcm16-192', 'aes-gcm16-256']:
                del path['ike']['authentication']
                path['ike']['prf'] = kwargs['prf']
            path['ike']['dh_group'] = kwargs['ike_dh_group']
            path['ike']['lifetime'] = int(kwargs['ike_lifetime'])
            path['ipsec']['protocol'] = kwargs['ipsec_protocol']
            if kwargs['ipsec_protocol'] == 'esp':
                path['ipsec']['encryption'] = {}
                path['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            ### enhance for ipsec_encryption
            # if kwargs['ipsec_encryption'] not in ['aes_gcm16_128', 'aes_gcm16_192', 'aes_gcm16_256']:
            #     path['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            if kwargs['ipsec_encryption'] not in ['aes_gcm16_128', 'aes_gcm16_192', 'aes_gcm16_256','aes_gmac_128','aes_gmac_192','aes_gmac_256']:
                path['ipsec']['authentication'] = {}
                path['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            if kwargs['ipsec_pfs']:
                path['ipsec']['perfect_forward_secrecy']['dh_group'] = kwargs['ipsec_pfs_dhgroup']
            path['ipsec']['lifetime'] = int(kwargs['ipsec_lifetime'])
        except KeyError:
            logger.error("Error: In creating JSON for vpn proposal")   
        logger.info("vpn proposal json obtained")
        return json_input        

    def _build_json_vpn_advanced(self, kwargs, json_vpn_advanced_input):
        json_input = copy.deepcopy(json_vpn_advanced_input)
        try:
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            if kwargs['type'] == 'site_to_site':
                path['netbios'] = kwargs['netbios']
                path['anti_replay'] = kwargs['anti_replay']
                # path['wxa_group'] = kwargs['wxa_group']
                path['multicast'] = kwargs['multicast']
                path['management']['https'] = kwargs['management_https']
                path['management']['ssh'] = kwargs['management_ssh']
                path['management']['snmp'] = kwargs['management_snmp']
                if kwargs['pri_gate'] == '0.0.0.0':
                    del path['keep_alive']
                else:
                    path['keep_alive'] = kwargs['keep_alive']
                # path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
                path['user_login']['http'] = kwargs['user_login_http']
                path['user_login']['https'] = kwargs['user_login_https']
                path['default_lan_gateway'] = kwargs['default_lan_gateway']
                if 'bound_to' in kwargs:
                    path['bound_to'] = {}
                    path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                logger.info("11111")
                if kwargs['sec_gate'] == '0.0.0.0':
                    if 'preempt_secondary_gateway' in kwargs:
                        del path['preempt_secondary_gateway']
                    if 'preempt_interval' in kwargs:
                        del path['preempt_interval']
                    logger.info("3333")
                elif 'preempt_interval' in kwargs:
                    path['preempt_secondary_gateway'] = {}
                    path['preempt_secondary_gateway']['interval'] = int(kwargs['preempt_interval'])
                    if not kwargs['preempt_secondary_gateway']:
                        del path['preempt_secondary_gateway']['interval']
                path['suppress_auto_add_rule'] = kwargs['suppress_auto_add_rule']
                #config apply_nat
                path['apply_nat'] = kwargs['apply_nat']
                if kwargs['apply_nat']:
                    logger.info("build json vpn applynat")
                    json_input = self._build_json_vpn_applynat(kwargs, json_input)
                ######
                if kwargs['ike_exchange'] == 'ikev2':
                    path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
                    path['accept_hash'] = kwargs['accept_hash']
                    path['send_hash'] = kwargs['send_hash']
                elif kwargs['ike_exchange'] == 'main' or kwargs['ike_exchange'] == 'aggressive':
                    path['require_xauth'] = kwargs['require_xauth']
            elif kwargs['type'] == 'tunnel_interface':
                if  'netbios' in kwargs:
                    path['netbios'] = kwargs['netbios']
                if  'anti_replay' in kwargs:
                    path['anti_replay'] = kwargs['anti_replay']
                # path['wxa_group'] = kwargs['wxa_group']
                if  'multicast' in kwargs:
                    path['multicast'] = kwargs['multicast']
                if  'management_https' in kwargs:
                    path['management']['https'] = kwargs['management_https']
                if  'management_ssh' in kwargs:
                    path['management']['ssh'] = kwargs['management_ssh']
                if  'management_snmp' in kwargs:
                    path['management']['snmp'] = kwargs['management_snmp']
                if kwargs['pri_gate'] == '0.0.0.0':
                    del path['keep_alive']
                else:
                    path['keep_alive'] = kwargs['keep_alive']
                if  'allow_sonicpointn_layer3' in kwargs:
                    path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
                if  'user_login_http' in kwargs:
                    path['user_login']['http'] = kwargs['user_login_http']
                if  'user_login_https' in kwargs:
                    path['user_login']['https'] = kwargs['user_login_https']
                if 'bound_to' in kwargs:
                    path['bound_to'] = {}
                    path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                path['advanced_routing'] = kwargs['advanced_routing']
                if kwargs['ike_exchange'] == 'ikev2':
                    path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
                    path['accept_hash'] = kwargs['accept_hash']
                    path['send_hash'] = kwargs['send_hash']
                if kwargs['ike_exchange'] == 'main' or kwargs['ike_exchange'] == 'aggressive':
                    path['transport_mode'] = kwargs['transport_mode']
        except KeyError:
            logger.error("Error: In creating JSON for vpn advanced ")   
        logger.info("vpn advanced json obtained")
        return json_input

    def _build_json_vpn_applynat(self, kwargs, json_vpn_applynat_input):
        json_input = copy.deepcopy(json_vpn_applynat_input)
        logger.info("22222")
        logger.info("json_input")
        try:
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]
            path['translated_network'] = {}
            path['translated_network']['local'] = {}
            path['translated_network']['remote'] = {}
            logger.info(path)
            if kwargs['nat_local_type'] != 'original':
                path['translated_network']['local'][kwargs['nat_local_type']] = kwargs['nat_local_name']
            elif kwargs['nat_local_type'] == 'original':
                path['translated_network']['local']['original'] = True
            else:
                pass
            if kwargs['nat_remote_type'] != 'original':
                path['translated_network']['remote'][kwargs['nat_remote_type']] = kwargs['nat_remote_name']
            elif kwargs['nat_remote_type'] == 'original':
                path['translated_network']['remote']['original'] = True
            else:
                pass
            # json_input['vpn']['policy'][0]['ipv4'][kwargs['type']] = path
        except KeyError:
            logger.error("Error: In creating JSON for build vpn apply_nat")
            logger.info("vpn advanced apply_nat json obtained")
        return json_input

    def _edit_json_vpn_authmode(self, kwargs, json_vpn_authmode_input):
        json_input = copy.deepcopy(json_vpn_authmode_input)
        try:
            if 'auth_mode' in kwargs:
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['auth_method'] = {}
                path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['auth_method']
                if kwargs['auth_mode'] == 'certificate':
                    if 'local_cert' in kwargs and 'local_ike_type' in kwargs and 'peer_ike_type' in kwargs and 'peer_ike_id' in kwargs:
                        path['certificate'] = {}
                        path['certificate']['certificate'] = kwargs['local_cert']
                        path['certificate']['ike_id'] = {}
                        path['certificate']['ike_id']['local'] = kwargs['local_ike_type']
                        path['certificate']['ike_id']['peer'] = {}
                        path['certificate']['ike_id']['peer'][kwargs['peer_ike_type']] = kwargs['peer_ike_id']
                    else:
                        logger.error('local_cert and local_ike_type and peer_ike_id must be specified')
                        return False
                    json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['auth_method'] = path
                    ### config ocsp
                    if 'ocsp_checking' in kwargs:
                        if kwargs['ocsp_checking'] and kwargs['ipversion'] == 'ipv4':
                            json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['ocsp_checking'] = {}
                            json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['ocsp_checking']['responder_url'] = kwargs['ocsp_resp_url']
                elif kwargs['auth_mode'] == 'shared_secret':
                    if 'secret' in kwargs and 'local_ike_type' in kwargs and 'peer_ike_type' and \
                            'local_ike_type' and 'peer_ike_id' in kwargs:
                        path['shared_secret'] = {}
                        path['shared_secret']['shared_secret'] = kwargs['secret']
                        path['shared_secret']['ike_id'] = {}
                        path['shared_secret']['ike_id']['local'] = {}
                        path['shared_secret']['ike_id']['local'][kwargs['local_ike_type']] = kwargs['local_ike_id']
                        path['shared_secret']['ike_id']['peer'] = {}
                        path['shared_secret']['ike_id']['peer'][kwargs['peer_ike_type']] = kwargs['peer_ike_id']
                    else:
                        logger.error('secret and local_ike_type and peer_ike_type and local_ike_id and peer_ike_id must be specified')
                        return False
                    json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['auth_method'] = path
        except KeyError:
            logger.error("Error: In creating JSON for edit vpn authmode")   
        logger.info("edit vpn authmode json obtained")
        return json_input

    def _edit_json_vpn_network(self, kwargs, json_vpn_network_input):
        json_input = copy.deepcopy(json_vpn_network_input)
        try:
            if 'local_net_type' in kwargs or 'remote_net_type' in kwargs:
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network'] = {}
            else:
                logger.error('local_net_type or remote_net_type should be specified')
                return False
            if 'local_net_type' in kwargs:
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local'] = {}
                local_path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local']
                if kwargs['local_net_type'] == 'name':
                    local_path['name'] = kwargs['local_net_name']
                elif kwargs['local_net_type'] == 'group':
                    local_path['group'] = kwargs['local_net_group']
                elif kwargs['local_net_type'] == 'host':
                    local_path['host'] = kwargs['local_net_host']
                elif kwargs['local_net_type'] == 'network':
                    local_path['network']['subnet'] = kwargs['local_net_network'][0]
                    local_path['network']['mask'] = kwargs['local_net_network'][1]
                elif kwargs['local_net_type'] == 'range':
                    local_path['range']['begin'] = kwargs['local_net_range'][0]
                    local_path['range']['end'] = kwargs['local_net_range'][1]
                elif kwargs['local_net_type'] == 'any':
                    local_path['any'] = True
                elif kwargs['local_net_type'] == 'dhcp':
                    local_path['dhcp'] = True
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['local'] = local_path

            if 'remote_net_type' in kwargs: 
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['remote'] = {}
                remote_path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['remote']
                if kwargs['remote_net_type'] == 'name':
                    remote_path['destination_network'] = {}
                    remote_path['destination_network']['name'] = kwargs['remote_net_name']
                elif kwargs['remote_net_type'] == 'group':
                    remote_path['group'] = kwargs['remote_net_group']
                elif kwargs['remote_net_type'] == 'host':
                    remote_path['host'] = kwargs['remote_net_host']
                elif kwargs['remote_net_type'] == 'network':
                    remote_path['network']['subnet'] = kwargs['remote_net_network'][0]
                    remote_path['network']['mask'] = kwargs['remote_net_network'][1]
                elif kwargs['remote_net_type'] == 'range':
                    remote_path['range']['begin'] = kwargs['remote_net_range'][0]
                    remote_path['range']['end'] = kwargs['remote_net_range'][1]
                elif kwargs['remote_net_type'] == 'any':
                    remote_path['any'] = True
                elif kwargs['remote_net_type'] == 'dhcp':
                    remote_path['dhcp'] = True
                elif kwargs['remote_net_type'] == 'pool':
                    remote_path['ikev2_ip_pool'] = {}
                    remote_path['ikev2_ip_pool']['name'] = kwargs['remote_net_name']
                json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['network']['remote'] = remote_path
        except KeyError:
            logger.error("Error: In creating JSON for edit vpn network")   
        logger.info("edit vpn network json obtained")
        return json_input

    def _edit_json_vpn_proposal(self, kwargs, json_vpn_proposal_input):
        json_input = copy.deepcopy(json_vpn_proposal_input)
        # try:
        if 'auth_mode' not in kwargs:
            logger.error('auth_mode must be specified when edit vpn_proposal')
            return False

        json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['proposal'] = {}
        ipv_path = json_input['vpn']['policy'][0][kwargs['ipversion']][kwargs['type']]['proposal']
        if 'ike_exchange' in kwargs or 'ike_encryption' in kwargs or 'ike_auth' in kwargs or \
                'ike_dh_group' in kwargs or 'ike_lifetime' in kwargs:
            ipv_path['ike'] = {}
        if 'ipsec_protocol' in kwargs or 'ipsec_encryption' in kwargs or 'ipsec_auth' in kwargs or \
                'ipsec_pfs' in kwargs or 'ipsec_pfs_dhgroup' in kwargs or 'ipsec_lifetime' in kwargs:
            ipv_path['ipsec'] = {}
        if (kwargs['auth_mode'] == 'certificate' or kwargs['auth_mode'] == 'shared_secret'):
            if 'ike_exchange' in kwargs:
                ipv_path['ike']['exchange'] = kwargs['ike_exchange']
            if 'ike_encryption' in kwargs:
                ipv_path['ike']['encryption'] = kwargs['ike_encryption']
                if  ipv_path['ike']['encryption'] in ['aes-gcm16-128', 'aes-gcm16-192', 'aes-gcm16-256']:
                    ipv_path['ike']['prf'] = kwargs['prf']
            if 'ike_auth' in kwargs:
                ipv_path['ike']['authentication'] = kwargs['ike_auth']
            if 'ike_dh_group' in kwargs:
                ipv_path['ike']['dh_group'] = kwargs['ike_dh_group']
            if 'ike_lifetime' in kwargs:
                ipv_path['ike']['lifetime'] = int(kwargs['ike_lifetime'])
            if 'ipsec_protocol' in kwargs:
                ipv_path['ipsec']['protocol'] = kwargs['ipsec_protocol']
                if kwargs['ipsec_protocol'] == 'esp' and 'ipsec_encryption' in kwargs:
                    ipv_path['ipsec']['encryption'] = {}
                    ipv_path['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            if 'ipsec_auth' in kwargs:
                ipv_path['ipsec']['authentication'] = {}
                ipv_path['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            ### enhance for ipsec_encryption and ipsec_auth
            if 'ipsec_encryption' in kwargs:
                ipv_path['ipsec']['encryption'] = {}
                ipv_path['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
                if kwargs['ipsec_encryption'] in ['aes_gcm16_128', 'aes_gcm16_192', 'aes_gcm16_256','aes_gmac_128','aes_gmac_192','aes_gmac_256'] and 'ipsec_auth' in ipv_path['ipsec']:
                    del ipv_path['ipsec']['authentication']
            if 'ipsec_pfs_dhgroup' in kwargs:
                if kwargs['ipsec_pfs']:
                    ipv_path['ipsec']['perfect_forward_secrecy']['dh_group'] = kwargs['ipsec_pfs_dhgroup']
            if 'ipsec_lifetime' in kwargs:
                ipv_path['ipsec']['lifetime'] = int(kwargs['ipsec_lifetime'])

        elif kwargs['auth_mode'] == 'manual':
            prop_path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]['proposal']
            if 'ipsec_protocol' in kwargs:
                prop_path['ipsec']['protocol'] = kwargs['ipsec_protocol']
                if kwargs['ipsec_protocol'] == 'esp' and 'ipsec_encryption' in kwargs:
                    prop_path['ipsec']['encryption'] = {}
                    prop_path['ipsec']['encryption'][kwargs['ipsec_encryption']] = True
            if 'ipsec_auth' in kwargs:
                prop_path['ipsec']['authentication'] = {}
                prop_path['ipsec']['authentication'][kwargs['ipsec_auth']] = True
            if 'in_spi' in kwargs:
                prop_path['ipsec']['in_spi'] = kwargs['in_spi']
            if 'out_spi' in kwargs:
                prop_path['ipsec']['out_spi'] = kwargs['out_spi']
            # if kwargs['ipversion'] == ipv4:
            if kwargs['ipversion'] == 'ipv4':
                if 'encryption_key' in kwargs:
                    prop_path['ipsec']['encryption_key'] = kwargs['encryption_key']
                if 'authentication_key' in kwargs:
                    prop_path['ipsec']['authentication_key'] = kwargs['authentication_key']
            elif kwargs['ipversion'] == 'ipv6':
                ipsec_path = json_input['vpn']['policy'][0]['ipv6']['site_to_site']['proposal']['ipsec']
                if 'in_encryption_key' in kwargs:
                    ipsec_path['in_encryption_key'] = kwargs['in_encryption_key']
                if 'in_authentication_key' in kwargs:
                    ipsec_path['in_authentication_key'] = kwargs['in_authentication_key']
                if 'out_encryption_key' in kwargs:
                    ipsec_path['out_encryption_key'] = kwargs['out_encryption_key']
                if 'out_authentication_key' in kwargs:
                    ipsec_path['out_authentication_key'] = kwargs['out_authentication_key']
        # except KeyError:
        #     logger.error("Error: In creating JSON for edit_vpn_proposal")
        logger.info(" edit_vpn_proposal json obtained")
        return json_input

    def _edit_json_vpn_advanced(self, kwargs, json_vpn_advanced_input):
        json_input = copy.deepcopy(json_vpn_advanced_input)
        try:
            if 'auth_mode' not in kwargs or 'ike_exchange' not in kwargs:
                logger.error('vpn auth_mode and ike_exchange must be specified when edit vpn_advanced')
                return False 
            ###### common config
            path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]

            if 'management_https' in kwargs or 'management_ssh' in kwargs or 'management_snmp' in kwargs:
                path['management'] = {}
                if 'management_https' in kwargs:
                    path['management']['https'] = kwargs['management_https']
                if 'management_ssh' in kwargs:
                    path['management']['ssh'] = kwargs['management_ssh']
                if 'management_snmp' in kwargs:
                    path['management']['snmp'] = kwargs['management_snmp']
            if 'user_login_http' in kwargs or 'user_login_https' in kwargs:
                path['user_login'] = {}
                if 'user_login_http' in kwargs:
                    path['user_login']['http'] = kwargs['user_login_http']
                if 'user_login_https' in kwargs:
                    path['user_login']['https'] = kwargs['user_login_https']
            ###############
            if kwargs['auth_mode'] == 'certificate' or kwargs['auth_mode'] == 'shared_secret':
                ###########################
                if kwargs['type'] == 'site_to_site':
                    if 'netbios' in kwargs:
                        path['netbios'] = kwargs['netbios']
                    if 'anti_replay' in kwargs:
                        path['anti_replay'] = kwargs['anti_replay']
                    if 'wxa_group' in kwargs:
                        path['wxa_group'] = kwargs['wxa_group']
                    if 'multicast' in kwargs:
                        path['multicast'] = kwargs['multicast']
                    if 'keep_alive' in kwargs:
                        path['keep_alive'] = kwargs['keep_alive']
                    if 'allow_sonicpointn_layer3' in kwargs:
                        path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
                    if 'default_lan_gateway' in kwargs:
                        path['default_lan_gateway'] = kwargs['default_lan_gateway']
                    if 'bound_to' in kwargs:
                        path['bound_to'] = {}
                        path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                    if 'suppress_auto_add_rule' in kwargs:
                        path['suppress_auto_add_rule'] = kwargs['suppress_auto_add_rule']
                    ###config apply_nat
                    if kwargs['edit_applynat']:
                        json_input = self._edit_json_vpn_applynat(kwargs, json_input)
                    ######
                    if 'ike_exchange' in kwargs:
                        if kwargs['ike_exchange'] == 'ikev2':
                            if 'suppress_trigger_packet' in kwargs:
                                path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
                            if 'accept_hash' in kwargs:
                                path['accept_hash'] = kwargs['accept_hash']
                            if 'send_hash' in kwargs:
                                path['send_hash'] = kwargs['send_hash']
                        elif kwargs['ike_exchange'] == 'main' or kwargs['ike_exchange'] == 'aggressive':
                            if 'require_xauth' in kwargs:
                                path['require_xauth'] = kwargs['require_xauth']
                #########################
                elif kwargs['type'] == 'tunnel_interface':
                    if 'netbios' in kwargs:
                        path['netbios'] = kwargs['netbios']
                    if 'anti_replay' in kwargs:
                        path['anti_replay'] = kwargs['anti_replay']
                    if 'wxa_group' in kwargs:
                        path['wxa_group'] = kwargs['wxa_group']
                    if 'multicast' in kwargs:
                        path['multicast'] = kwargs['multicast']
                    if 'keep_alive' in kwargs:
                        path['keep_alive'] = kwargs['keep_alive']
                    if 'bound_to' in kwargs:
                        path['bound_to'] = {}
                        path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                    if 'advanced_routing' in kwargs:
                        path['advanced_routing'] = kwargs['advanced_routing']
                    if 'suppress_trigger_packet' in kwargs or 'accept_hash' in kwargs or 'send_hash' in kwargs:
                        if kwargs['ike_exchange'] == 'ikev2':
                            if 'suppress_trigger_packet' in kwargs:    
                                path['suppress_trigger_packet'] = kwargs['suppress_trigger_packet']
                            if 'accept_hash' in kwargs:
                                path['accept_hash'] = kwargs['accept_hash']
                            if 'send_hash' in kwargs:
                                path['send_hash'] = kwargs['send_hash']
                        else:
                            logger.error('ike_exchange must be specified as ikev2')
                            return False
                    if 'transport_mode' in kwargs:
                        if kwargs['ike_exchange'] == 'main' or kwargs['ike_exchange'] == 'aggressive':
                            path['transport_mode'] = kwargs['transport_mode']
            ########## manual auth mode advanced setting ########
            elif kwargs['auth_mode'] == 'manual':
                if 'netbios' in kwargs:
                    path['netbios'] = kwargs['netbios']
                # if 'wxa_group' in kwargs:
                    # path['wxa_group'] = kwargs['wxa_group']
                if 'allow_sonicpointn_layer3' in kwargs:
                    path['allow_sonicpointn_layer3'] = kwargs['allow_sonicpointn_layer3']
                if 'bound_to' in kwargs:
                    path['bound_to'] = {}
                    path['bound_to'][kwargs['bound_to'][0]] = kwargs['bound_to'][-1]
                if (kwargs['type'] == 'site_to_site'):
                    if 'default_lan_gateway' in kwargs:                    
                        path['default_lan_gateway'] = kwargs['default_lan_gateway']
                    if 'suppress_auto_add_rule' in kwargs:
                        path['suppress_auto_add_rule'] = kwargs['suppress_auto_add_rule']
                        ###config apply_nat
                    if 'edit_applynat' in kwargs:
                        json_input = self._edit_json_vpn_applynat(kwargs, json_input)
        except KeyError:
            logger.error("Error: In creating JSON for vpn advanced ")   
        logger.info("vpn advanced json obtained")
        return json_input

    def _edit_json_vpn_applynat(self, kwargs, json_vpn_applynat_input):
        json_input = copy.deepcopy(json_vpn_applynat_input)
        path = json_input['vpn']['policy'][0]['ipv4'][kwargs['type']]

        if kwargs['apply_nat']:
            path['apply_nat'] = {}
            logger.info("build json vpn applynat")
            try:
                if 'nat_local_type' in kwargs:
                    path['apply_nat']['translated_local'] = {}
                    if kwargs['nat_local_type'] == 'name':
                        path['apply_nat']['translated_local']['name'] = kwargs['nat_local_name']
                    elif kwargs['nat_local_type'] == 'group':
                        path['apply_nat']['translated_local']['group'] = kwargs['nat_local_group']
                    elif kwargs['nat_local_type'] == 'host':
                        path['apply_nat']['translated_local']['host'] = kwargs['nat_local_host']
                    elif kwargs['nat_local_type'] == 'network':
                        path['apply_nat']['translated_local']['network']['subnet'] = kwargs['nat_local_network'][0]
                        path['apply_nat']['translated_local']['network']['mask'] = kwargs['nat_local_network'][1]
                    elif kwargs['nat_local_type'] == 'range':
                        path['apply_nat']['translated_local']['range']['begin'] = kwargs['nat_local_range'][0]
                        path['apply_nat']['translated_local']['range']['end'] = kwargs['nat_local_range'][1]
                    elif kwargs['nat_local_type'] == 'original':
                        path['apply_nat']['translated_local']['original'] = True
                    else:
                        pass
                if 'nat_remote_type' in kwargs:
                    path['apply_nat']['translated_remote'] = {}
                    if kwargs['nat_remote_type'] == 'name':
                        path['apply_nat']['translated_remote']['name'] = kwargs['nat_remote_name']
                    elif kwargs['nat_remote_type'] == 'group':
                        path['apply_nat']['translated_remote']['group'] = kwargs['nat_remote_group']
                    elif kwargs['nat_remote_type'] == 'host':
                        path['apply_nat']['translated_remote']['host'] = kwargs['nat_remote_host']
                    elif kwargs['nat_remote_type'] == 'network':
                        path['apply_nat']['translated_remote']['network']['subnet'] = kwargs['nat_remote_network'][0]
                        path['network']['translated_remote']['network']['mask'] = kwargs['nat_remote_network'][1]
                    elif kwargs['nat_remote_type'] == 'range':
                        path['apply_nat']['translated_remote']['range']['begin'] = kwargs['nat_remote_range'][0]
                        path['apply_nat']['translated_remote']['range']['end'] = kwargs['nat_remote_range'][1]
                    elif kwargs['nat_remote_type'] == 'original':
                        path['apply_nat']['translated_remote']['original'] = True
                    else:
                        pass
            except KeyError:
                logger.error("Error: In creating JSON for edit vpn apply_nat")
            logger.info("vpn advanced apply_nat json obtained")
        return json_input

    def Renegotiate_VPN_Tunnel(self,msg=False,**kwargs):
        src_addr_type = 4
        dst_addr_type = 4
        dhcp_flag = 0
        for i in range(5):
            cookie_data = self.fw.api_get(self.url_cookie)
            cookie = cookie_data['data']['activeIPsecSAs'][0]['initCookie']
            if cookie:
                logger.info(f'The cookie is: {cookie} ')
                break
            else:
                logger.info('The cookie is null ')
                time.sleep(15)
        #cookie_data = self.fw.api_get(self.url_cookie)
        port = cookie_data['data']['activeIPsecSAs'][0]['inDstGwPort']
        #cookie = cookie_data['data']['activeIPsecSAs'][0]['initCookie']
        inSpi =  cookie_data['data']['activeIPsecSAs'][0]['inSpi']
        if 'dhcp' in kwargs.keys():
            if kwargs['dhcp'] == 1:
                dhcp_flag = kwargs['dhcp']

        if "/" in cookie:
            cookie = cookie.replace('/', '%2F')
        if "%" in cookie:
            cookie = cookie.replace('/', '%25')
            
        SrcIpType   = str(src_addr_type)
        SrcNet      = kwargs['local_net']
        SrcMask     = kwargs['local_mask']
        DstIpType   = str(dst_addr_type)
        DstNet      = kwargs['remote_net']
        DstMask     = kwargs['remote_mask']
        InitCookie  = cookie
        DstGW       = kwargs['remote_gw']
        DstGwPort   = str(port)
        IsDhcpCl    = str(dhcp_flag)
        InSpi       = str(inSpi)

        url = 'api/sonicos/renegotiate/tunnel'\
              +'/'+SrcIpType+'/'+SrcNet+'/'+ SrcMask\
              +'/'+DstIpType+'/'+DstNet+'/'+ DstMask\
              +'/'+InitCookie+'/'+DstGW+'/'+DstGwPort\
              +'/'+IsDhcpCl+'/'+InSpi
        logger.info(url)
        res = self.fw.api_post(url, msg)
        return res

    def RenegotiateVPN(self,msg=False,**kwargs):
        '''
        Raw api is not supported.
        '''
        raw_json = copy.deepcopy(self.renegotiateVpn_raw)
        dst_addr_type = 4
        dhcp_flag     = 0
        if 'local_mask' not in kwargs.keys():
            raw_json["stream"]['ikeSrcMask'] = "255.255.255.0"
        if 'remote_mask' not in kwargs.keys():
            raw_json["stream"]['ikeDstMask'] = "255.255.255.0"
        # if kwargs['remote_net_type'] == 'range':
        #     dst_addr_type = 7
        if 'dhcp' in kwargs.keys():
            if kwargs['dhcp'] == 1:
                dhcp_flag = kwargs['dhcp']

        cookie_data = self.fw.api_get(self.url_cookie)
        cookie = cookie_data['data']['activeIPsecSAs'][0]['initCookie']

        raw_json["stream"]['ikeSrcNet']        = kwargs['local_net']
        raw_json["stream"]['ikeSrcMask']       = kwargs['local_mask']
        raw_json["stream"]['ikeDstAddrType']   = dst_addr_type
        raw_json["stream"]['ikeDstNet']        = kwargs['remote_net']
        raw_json["stream"]['ikeDstMask']       = kwargs['remote_mask']
        raw_json["stream"]['ikeDstGw']         = kwargs['remote_gw']
        raw_json["stream"]['InitCookie']       = cookie
        raw_json["stream"]['ikeIsDhcpClient']  = dhcp_flag

        json_input = {"stream": {}}
        line = ''
        for item in raw_json['stream']:
            line += item + '=' + str(raw_json['stream'][item]) + '&'
        json_input['stream'] = line[:-1]
        res = self.fw.api_post(self.url_raw, msg, data=json_input)
        return res
 
    def get_shared_secret(self, name):
        vpn_url = 'api/sonicos/dynamic-file/getVPNPolicyInfo.json?name=' + name
        vpn_resp = self.fw.api_get(vpn_url)
        return vpn_resp

    # add by JLian
    # 710:'policyName': '"localvpn"       701:'policyName': 'localvpn'
    def get_vpn_status(self, policyname):
        url = 'api/sonicos/dynamic-file/getStatsData.json?restype=12&datatype=1'
        res = self.fw.api_get(url)
        vpnstatus = False
        try:
            datas = res['data']['vpnPolices']
            logger.info(f'get vpn policies result :{datas}')
            for data in datas:
                # {'data': {'resourceType': 'vpn-policies', 'dataType': 'current', 'vpnPolices': [
                #     {'policyName': '"WAN GroupVPN"', 'tunnelInfo': [{'destNetwork': ''}],
                #      'cryptoSuite': 'ESP: 3DES/HMAC SHA1 (IKE)', 'policyIndex': 0, 'policyEnabled': 'no'},
                #     {'policyName': '"WLAN GroupVPN"', 'tunnelInfo': [{'destNetwork': ''}],
                #      'cryptoSuite': 'ESP: 3DES/HMAC SHA1 (IKE)', 'policyIndex': 1, 'policyEnabled': 'no'},
                #     {'policyName': '"localvpn"', 'gateway': '12.12.1.201 ', 'tunnelInfo': [
                #         {'activeSAIndex': '0', 'vpnDstStr': 'vpn2_dst_1', 'destNetwork': '172.16.1.0 - 172.16.1.255'}],
                #      'cryptoSuite': 'ESP: AES-128/HMAC SHA1 (IKEv2)', 'policyIndex': 2, 'policyEnabled': 'yes'}],
                #           'strVpnPolicies': '1 Policies Defined, 1 Policies Enabled, 250 Maximum Policies Allowed',
                #           'strGroupVpnPolicies': '2 Policies Defined, 0 Policies Enabled, 25 Maximum Policies Allowed',
                #           'vpnPolicyCount': 3}, 'productModel': 'TZ 570', 'upTime': '0 Days 00:18:21',
                #  'systime': 1661463878, 'loggedin': True, 'status': 'OK',
                #  'apiLink': 'HTTPS://SONICOS-API.SONICWALL.COM/index.html?sonicwallIp=12.12.1.200&sonicwallPort=443&model=TZ&version=7.0.1'}
                if data['policyName'].strip('"') == policyname:
                    if 'activeSAIndex' in str(data['tunnelInfo']):
                        vpnstatus = True if data['tunnelInfo'][0]['activeSAIndex'] >= '0' else False
                    else:
                        logger.info(f'tunnel vpn policy is down.')
                    info = 'up' if vpnstatus else 'down'
                    return vpnstatus, info
        except Exception as e:
            info = 'error'
            logger.error(repr(e))
            return False, info

    def get_vpn_all_status_info(self, policyname=None):
        url = 'api/sonicos/dynamic-file/getStatsData.json?restype=12&datatype=1'
        res = self.fw.api_get(url)
        if policyname:
            datas = res['data']['vpnPolices']
            for data in datas:
                if data['policyName'].strip('"') == policyname:
                    logger.info(f'The data status info is: {data}')
                    return data
        else:
            return res
            
    def get_tunnel_spi(self):
        res = self.fw.api_get(self.spi_url)
        spi = res["data"]["activeIPsecSAs"][0]["statsLink"]
        return spi

    def get_Tunnel_stats_status(self):
        spi = self.get_tunnel_spi()
        url = self.stats_url + spi
        res = ( self.fw.api_get(url))["data"]
        return res

    def get_active_vpn_tunnels(self):
        activeIPsecSAs = []
        res = self.fw.api_get(self.spi_url)
        try:
            activeIPsecSAs = res["data"]["activeIPsecSAs"]
        except Exception as e:
            logger.error(f"Error: {e}")
        return activeIPsecSAs

    def get_active_vpn_tunnels_ipv6(self):
        activeIPsecSAs = []
        url = 'api/sonicos/dynamic-file/getStatsData.json?restype=24&datatype=1'
        res = self.fw.api_get(url)
        try:
            activeIPsecSAs = res["data"]["activeIPsecSAs"]
        except Exception as e:
            logger.error(f"Error: {e}")
        return activeIPsecSAs

    def Renegotiate_Tunnel_stats(self):
        spi = self.get_tunnel_spi()
        cgi = {
        "stream": "cgiaction=ikeNegotiate&ikeSrcAddrType=4&ikeSrcNet=192.168.168.0&ikeSrcMask=255.255.255.0&ikeDstAddrType=4&ikeDstNet=172.16.1.0&ikeDstMask=255.255.255.0&ikeDstGw=12.12.1.201&ikeDstGwPort=500&InitCookie=JZbKrYOXmCk=&ikeIsDhcpClient=0&ikeInSpi="+spi
        }
        self.fw.api_post(url=self.url_raw,data = cgi,headers = self.headers)
        res = self.get_Tunnel_stats_status()
        rxpkt, txpkts, rxbytes, txbytes,rxfrags, txfrag = int(res['rxPkts']), \
            int(res['txPkts']), int(res['rxBytes']),  int(res['txBytes']), \
            int(res['rxFrags']), int(res['txFrags'])
        if rxpkt==0 and txpkts == 0 and rxbytes == 0 and txbytes == 0 and \
            rxfrags ==0 and txfrag == 0:
            rc = True
        else:
            rc = False
        return rc    

    def Re_Negotiate_Entry(self, stream):
        # stream is
        # 'cgiaction=ikeNegotiate&ikeSrcAddrType=4&ikeSrcNet=192.168.168.0&ikeSrcMask=255.255.255.0
        # &ikeDstAddrType=4&ikeDstNet=172.16.1.0&ikeDstMask=255.255.255.0&ikeDstGw=12.12.1.201&ikeDstGwPort=500
        # &InitCookie=JZbKrYOXmCk=&ikeIsDhcpClient=0&ikeInSpi='
        res = False
        # get old tunnel stats
        oldres = self.get_Tunnel_stats_status()

        ikeinspi = self.get_tunnel_spi()
        request_payload = {"stream": stream + ikeinspi}
        self.fw.api_post(url=self.url_raw, data=request_payload, headers=self.headers)
        logger.info('wait for 30s to make sure re negotiate finished...')
        time.sleep(30)

        # get new tunnel stats
        newres = self.get_Tunnel_stats_status()

        # check create time in tunnel stats
        try:
            logger.info(f'old create time: {oldres["createTm"]}, new create time: {newres["createTm"]}')
            if oldres["createTm"] < newres["createTm"]:
                logger.info('re negotiate entry successful.')
                res = True
        except Exception as e:
            logger.info(repr(e))
        return res    


class VpnAdvancedsettingApi:
    '''VpnAdvancedsettingApi class'''
    default_options = {
        'enable': True,
        'firewall_identifier': 'C0EAE486F7AA',
        'cleanup_tunnels': True,
        'preserve_ike_port': False,
        'traps_on_change': False,
        'nat_traversal': True,
        'ocsp_checking': False,
        'responder_url': '',
        'frag_packets': True,
        'ignore_df_bit': False,
        'ike_dpd': True,
        'dpd_interval': '60',
        'dpd_trigger': '3',
        'idle_dpd': False,
        'idle_dpd_interval': '600',
        'dns_server': 'inherit',  ## inherit or static
        'dns_primary': '0.0.0.0',
        'dns_sencondary': '0.0.0.0',
        'dns_tertiary': '0.0.0.0',
        'win_primary': '0.0.0.0',
        'win_sencondary': '0.0.0.0',
        'send_cookie': False,
        'send_invalid_spi': True,
        'dh_group': '2',
        'encryption': 'aes-128',
        'authentication': 'sha-1',
        }
        
    def __init__(self, fw):
        self.fw = fw
        '''
        # modified URL and json by neil zhang 2021 6/22
        self.url = 'api/sonicos/vpn/settings'
        self.initial_vpnadvancedsetting_json = {
            "vpn": {
                "enable": True,
                "firewall_identifier": "",
                "cleanup_tunnels": False,
                "preserve_ike_port": False,
                "traps_on_change": False,
                "nat_traversal": False,
                "ocsp_checking": {
                            # "responder_url": "http://www.sonicwall.com/ocsp"   
                },
                "frag_packets": {
                            # "ignore_df_bit": true
                },
                "ike_dpd": {
                    # "interval": 60,
                    # "trigger": 3,
                    # "idle_dpd": {
                    #     "interval": 600
                    # }
                },
                "dns": {
                    "server": {
                        # "static": {
                        #     "primary": "0.0.0.0",
                        #     "secondary": "0.0.0.0",
                        #     "tertiary": "0.0.0.0"
                        # }
                    }
                },
                "wins": {
                    "primary": "0.0.0.0",
                    "secondary": "0.0.0.0"
                },
                "ikev2": {
                    "send_cookie": False,
                    "send_invalid_spi": False,
                    "proposal": {
                        "dh_group": "2",
                        "encryption": "aes-128",
                        "authentication": "sha-1"
                    }
                }
            }
        }
        '''
        self.url = 'api/sonicos/vpn/base'
        self.initial_vpnadvancedsetting_json = {
            "vpn": {
                "enable": True,
                "firewall_identifier": "",
                "cleanup_tunnels": True,
                "preserve_ike_port": False,
                "traps_on_change": False,
                "nat_traversal": True,
                "ocsp_checking": False,
                "responder_url": "",
                "frag_packets": {
                    "enable": True,
                    "ignore_df_bit": False
                },
                "ike_dpd": {
                    "enable": True,
                    "interval": 60,
                    "trigger": 3,
                    "idle_dpd": False,
                    "idle_dpd_interval": 600
                },
                "dns": {
                    "server": {
                        "inherit": True
                    }
                },
                "wins": {
                    "primary": "0.0.0.0",
                    "secondary": "0.0.0.0"
                },
                "ikev2": {
                    "send_cookie": False,
                    "send_invalid_spi": True,
                    "proposal": {
                        "dh_group": "2",
                        "encryption": "aes-128",
                        "authentication": "sha-1"
                    }
                }
            }
        }

    def config_vpnadvanced(self, msg=False, **kwargs):
        self.options = dict(VpnAdvancedsettingApi.default_options)
        self.options.update(kwargs)         
        kwargs = self.options        
        json_input = self.build_json_vpnadvanced(**kwargs)
        vpnadvanced_resp = self.fw.api_put(self.url, msg, data=json_input)
        return vpnadvanced_resp

    def modify_vpnadvanced(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        vpnadvanced_resp = self.fw.api_put(self.url, msg, data=json_input)
        return vpnadvanced_resp

    def show_vpnadvanced(self):
        vpnadvanced_output = self.fw.api_get(self.url)
        return vpnadvanced_output

    def build_json_vpnadvanced(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_vpnadvancedsetting_json)
            ### vpn base setting
            json_input['vpn']['enable'] = kwargs['enable']
            json_input['vpn']['firewall_identifier'] = kwargs['firewall_identifier']
            json_input['vpn']['cleanup_tunnels'] = kwargs['cleanup_tunnels']
            json_input['vpn']['preserve_ike_port'] = kwargs['preserve_ike_port']
            json_input['vpn']['traps_on_change'] = kwargs['traps_on_change']
            json_input['vpn']['nat_traversal'] = kwargs['nat_traversal']
            if kwargs['ocsp_checking']:
                json_input['vpn']['ocsp_checking']['responder_url'] = kwargs['responder_url']
            #if kwargs['frag_packets']:
                ## Added enable key by neil zhang 2021 6/22
                #json_input['vpn']['frag_packets']['enable'] = kwargs['enable']
                #json_input['vpn']['frag_packets']['ignore_df_bit'] = kwargs['ignore_df_bit']
            json_input['vpn']['frag_packets']['enable'] = kwargs['frag_packets']
            json_input['vpn']['frag_packets']['ignore_df_bit'] = kwargs['ignore_df_bit']
            json_input['vpn']['ike_dpd']['enable'] = kwargs['ike_dpd']
            if kwargs['ike_dpd']:
                json_input['vpn']['ike_dpd']['interval'] = kwargs['dpd_interval']
                json_input['vpn']['ike_dpd']['trigger'] = kwargs['dpd_trigger']
                try:
                    json_input['vpn']['ike_dpd']['interval'] = int(kwargs['dpd_interval'])
                    json_input['vpn']['ike_dpd']['trigger'] = int(kwargs['dpd_trigger'])
                except:
                    pass
                json_input['vpn']['ike_dpd']['idle_dpd'] = kwargs['idle_dpd']
                json_input['vpn']['ike_dpd']['idle_dpd_interval'] = int(kwargs['idle_dpd_interval'])
            if kwargs['dns_server'] == 'inherit':
                json_input['vpn']['dns']['server']['inherit'] = True
            elif kwargs['dns_server'] =='static':
                json_input['vpn']['dns']['server']['static'] = {}
                json_input['vpn']['dns']['server']['static']['primary'] = kwargs['dns_primary']
                json_input['vpn']['dns']['server']['static']['secondary'] = kwargs['dns_sencondary']
                json_input['vpn']['dns']['server']['static']['tertiary'] = kwargs['dns_tertiary']
            json_input['vpn']['wins']['primary'] = kwargs['win_primary']
            json_input['vpn']['wins']['secondary'] = kwargs['win_sencondary']
            json_input['vpn']['ikev2']['send_cookie'] = kwargs['send_cookie']
            json_input['vpn']['ikev2']['send_invalid_spi'] = kwargs['send_invalid_spi']
            json_input['vpn']['ikev2']['proposal']['dh_group'] = kwargs['dh_group']
            json_input['vpn']['ikev2']['proposal']['encryption'] = kwargs['encryption']
            json_input['vpn']['ikev2']['proposal']['authentication'] = kwargs['authentication']
        except KeyError:
            logger.error("Error: In creating JSON for vpnadvancedsetting")   
        logger.info("vpnadvancedsetting json obtained")
        logger.info(json_input)      
        return json_input


class DhcpOverVpnApi:
    '''DhcpOverVpnApi class'''
    default_centralgw_options = {
        'internal_dhcp': False,
        'global_vpn': False,
        'remote': False,
        'relay_ip': '0.0.0.0',
        'send_requests': False,
        # 'dhcp_server_ip_list': ['0.0.0.0'],
        }

    default_remotegw_options = {
        'bound_to': 'X0',
        #'accept_bridged_wlan_request': False,
        'relay_ip': '0.0.0.0',
        'management_ip': '0.0.0.0',
        'block_spoof': True,
        'temp_lease': False,
        'lease_time': '2',
        }
        
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/vpn/dhcp-over-vpn'
        self.url_base = 'api/sonicos/vpn/dhcp-over-vpn/base'
        self.url_central = 'api/sonicos/vpn/dhcp-over-vpn/base/central'
        self.url_remote= 'api/sonicos/vpn/dhcp-over-vpn/base/remote'
        self.url_static_devices = 'api/sonicos/vpn/dhcp-over-vpn/static-devices'
        self.url_excluded_devices = 'api/sonicos/vpn/dhcp-over-vpn/excluded-devices'
        self.url_dhcp_servers = 'api/sonicos/vpn/dhcp-over-vpn/dhcp-servers'
        self.url_dhcp_leases = 'api/sonicos/reporting/vpn/dhcp-over-vpn/leases'        #updata_by_JLian

        self.initial_centralgw_json = {
            "vpn": {
                "dhcp_over_vpn": {
                    "central": {
                        "internal_dhcp": False,
                        # "global_vpn": False,
                        # "remote": False,
                        "relay_ip": "0.0.0.0",
                        "send_requests": False
                        # "dhcp_server": [
                            # {
                            #     "ip": "1.1.1.1"
                            # },
                            # {
                            #     "ip": "2.2.2.2"
                            # }
                        # ]
                    }
                }
            }
        }

        self.initial_remotegw_json = {
            "vpn": {
                "dhcp_over_vpn": {
                    "remote": {
                        "bound_to": "X0",
                        #"accept_bridged_wlan_request": False,
                        "relay_ip": "0.0.0.0",
                        "management_ip": "0.0.0.0",
                        "block_spoof": True,
                        "temp_lease": False,
                        "lease_time": 2
                        # "static_device": [
                            # {
                                # "ip": "1.1.1.1",
                                # "mac": "012111224433"
                            # },
                            # {
                                # "ip": "10.20.10.10",
                                # "mac": "022221331401"
                            # }
                        # ],
                        # "excluded_device": [
                            # {
                                # "mac": "332244668814"
                            # },
                            # {
                                # "mac": "521122441121"
                            # }
                        # ]
                    }
                }
            }
        }

    def config_dhcpvpn_centralgw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_centralgw_options)
        self.options.update(kwargs)
        if 'dhcp_server_ip_list' in kwargs:
            tmp_dict = {'node': 'central', 'servers': kwargs['dhcp_server_ip_list']}
            rc = self.add_dhcp_server(**tmp_dict)
            if not rc:
                logger.error("Add external DHCP server failed.")
                return rc
            else:
                logger.info("Add external DHCP server passed. Go on with other settings.")
        kwargs = self.options
        json_input = self.build_json_centralgw(**kwargs)
        centralgw_resp = self.fw.api_put(self.url_central, msg, data=json_input)
        return centralgw_resp

    def edit_dhcpvpn_centralgw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_centralgw_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_centralgw(**kwargs)
        delcentralgw_resp = self.fw.api_put(self.url, msg, data=json_input)
        return delcentralgw_resp

    def modify_dhcpvpn_central(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        dhcpvpn_central_resp = self.fw.api_put(self.url_central, msg, data=json_input)
        return dhcpvpn_central_resp


    def del_dhcpvpn_centralgw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_centralgw_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_centralgw(**kwargs)
        delcentralgw_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return delcentralgw_resp

    def config_dhcpvpn_remotegw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_remotegw_options)
        self.options.update(kwargs)
        static_dev_list = {}
        exclude_dev_list = []
        if 'static_device_ip_list' in kwargs and 'static_device_mac_list' in kwargs:
            i = 0
            for device_ip in kwargs['static_device_ip_list']:
                static_dev_list[kwargs['static_device_ip_list'][i]] = kwargs['static_device_mac_list'][i]
                i += 1
            rc = self.add_static_device_remotegw(**static_dev_list)
            if not rc:
                logger.error("Add static devices failed.")
                return rc
        if 'excluded_device_mac_list' in kwargs:
            exclude_dev_list = kwargs['excluded_device_mac_list']
            rc = self.add_exclude_device_remotegw(*exclude_dev_list)
            if not rc:
                logger.error("Add exclude devices failed.")
                return rc

        kwargs = self.options
        json_input = self.build_json_remotegw(**kwargs)
        remotegw_resp = self.fw.api_put(self.url_remote, msg, data=json_input)
        return remotegw_resp

    def edit_dhcpvpn_remotegw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_remotegw_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_remotegw(**kwargs)
        remotegw_resp = self.fw.api_put(self.url, msg, data=json_input)
        return remotegw_resp

    def del_dhcpvpn_remotegw(self, msg=False, **kwargs):
        self.options = dict(DhcpOverVpnApi.default_remotegw_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_remotegw(**kwargs)
        remotegw_resp = self.fw.api_delete(self.url, msg, data=json_input)
        return remotegw_resp

    def show_dhcpovervpn(self):      
        dhcpovervpn_output = self.fw.api_get(self.url_base)
        return dhcpovervpn_output

    def show_dhcpovervpn_central(self):
        dhcpovervpn_output = self.fw.api_get(self.url_central)
        return dhcpovervpn_output

    def show_dhcpovervpn_remote(self):
        dhcpovervpn_output = self.fw.api_get(self.url_remote)
        return dhcpovervpn_output

    def show_dhcp_servers(self):      
        dhcpovervpn_output = self.fw.api_get(self.url_dhcp_servers)
        return dhcpovervpn_output
        
    def add_dhcp_server(self, msg=False, **kwargs):
        '''
            kwargs example: { 'node': 'central', 'servers': ['192.168.168.169'] }
        '''
        dhcp_server_dict = {
            'vpn': {
                'dhcp_over_vpn': {
                }
            }
        }
        node = 'central'
        if 'node' in kwargs.keys():
            node = kwargs['node']
        if 'servers' not in kwargs.keys() or len(kwargs['servers']) == 0:
            logger.error("You must pass in DHCP server IPs")
            return False
        ips = []
        for item in kwargs['servers']:
            ips.append({'ip': item})

        dhcp_server_dict['vpn']['dhcp_over_vpn'].update({node: {'dhcp_server': ips}})
        logger.info(dhcp_server_dict)
        dhcpserver_resp = self.fw.api_post(self.url_dhcp_servers, msg, data=dhcp_server_dict)
        return dhcpserver_resp

    def del_dhcp_server(self, msg=False, **kwargs):
        '''
            kwargs example: { 'node': 'central', 'servers': ['192.168.168.169'] }
        '''
        dhcp_server_dict = {
            'vpn': {
                'dhcp_over_vpn': {
                }
            }
        }
        node = 'central'
        if 'node' in kwargs.keys():
            node = kwargs['node']
        if 'servers' not in kwargs.keys() or len(kwargs['servers']) == 0:
            logger.error("You must pass in DHCP server IPs")
            return False
        ips = []
        for item in kwargs['servers']:
            ips.append({'ip': item})

        dhcp_server_dict['vpn']['dhcp_over_vpn'].update({node: {'dhcp_server': ips}})
        logger.info(dhcp_server_dict)
        dhcpserver_resp = self.fw.api_delete(self.url_dhcp_servers, msg, data=dhcp_server_dict)
        return dhcpserver_resp

    def del_all_dhcp_server(self, msg=False):
        url = self.url + '/dhcp-servers-all'
        output = self.fw.api_delete(url, msg, data={})
        return output

    def show_dhcp_leases(self):      
        dhcpovervpn_output = self.fw.api_get(self.url_dhcp_leases)
        return dhcpovervpn_output
    
    def show_dhcp_excluded_devices(self):      
        dhcpovervpn_output = self.fw.api_get(self.url_excluded_devices)
        return dhcpovervpn_output

    def show_dhcp_static_devices(self):      
        dhcpovervpn_output = self.fw.api_get(self.url_static_devices)
        return dhcpovervpn_output

    def add_static_device_remotegw(self, msg=False, **ip_mac_list):
        '''
            ip_mac_list = {
                '192.168.168.100': '11:22:33:44:55:66', ### MAC can contain ':' or not
                '192.168.168.101': '112233445566'
            }
        '''
        static_dev_dict = {
            "vpn":{
                "dhcp_over_vpn":{
                    "remote":{
                        "static_device":[]
                    }
                }
            }
        }
        static_list = []
        for key in ip_mac_list.keys():
            mac = ip_mac_list[key].replace(':','')
            static_list.append({'ip': key, 'mac': mac})
        static_dev_dict['vpn']['dhcp_over_vpn']['remote']['static_device'] = static_list
        output = self.fw.api_post(self.url_static_devices, msg, data=static_dev_dict)
        return output

    def del_static_device_remotegw(self, msg=False, **ip_mac_list):
        '''
            ip_mac_list = {
                '192.168.168.100': '11:22:33:44:55:66', ### MAC can contain ':' or not
                '192.168.168.101': '112233445566'
            }
        '''
        static_dev_dict = {
            "vpn":{
                "dhcp_over_vpn":{
                    "remote":{
                        "static_device":[]
                    }
                }
            }
        }
        static_list = []
        for key in ip_mac_list.keys():
            mac = ip_mac_list[key].replace(':','')
            static_list.append({'ip': key, 'mac': mac})
        static_dev_dict['vpn']['dhcp_over_vpn']['remote']['static_device'] = static_list
        output = self.fw.api_delete(self.url_static_devices, msg, data=static_dev_dict)
        return output

    def del_all_static_device_remotegw(self, msg=False):
        url = self.url + '/static-devices-all'
        output = self.fw.api_delete(url, msg, data={})
        return output

    def add_exclude_device_remotegw(self, *exclude_list, msg=False):
        print(exclude_list)
        exclude_dict = {
            "vpn":{
                "dhcp_over_vpn":{
                    "remote":{
                        "excluded_device":[]
                    }
                }
            }
        }
        ex_dev = []
        for item in exclude_list:
            print(item)
            ex_dev.append({'mac': item.replace(':','')})
        print(ex_dev)
        exclude_dict['vpn']['dhcp_over_vpn']['remote']['excluded_device'] = ex_dev
        output = self.fw.api_post(self.url_excluded_devices, msg, data=exclude_dict)
        return output

    def del_exclude_device_remotegw(self, *exclude_list, msg=False):
        print(exclude_list)
        exclude_dict = {
            "vpn":{
                "dhcp_over_vpn":{
                    "remote":{
                        "excluded_device":[]
                    }
                }
            }
        }
        ex_dev = []
        for item in exclude_list:
            print(item)
            ex_dev.append({'mac': item.replace(':','')})
        print(ex_dev)
        exclude_dict['vpn']['dhcp_over_vpn']['remote']['excluded_device'] = ex_dev
        output = self.fw.api_delete(self.url_excluded_devices, msg, data=exclude_dict)
        return output

    def del_all_exclude_device_remotegw(self, msg=False):
        url = self.url + '/excluded-lan-devices-all'
        output = self.fw.api_delete(url, msg, data={})
        return output

    # add by jlian
    def delete_dhcp_over_vpn_dynamic_lease(self, lease_ip):
        url = f'api/sonicos/reporting/dhcp-over-vpn/leases/ip/{lease_ip}'
        dhcp_resp = self.fw.api_delete(url)
        return dhcp_resp

    def build_json_centralgw(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_centralgw_json)
            ### vpn base setting
            json_input['vpn']['dhcp_over_vpn']['central']['internal_dhcp'] = kwargs['internal_dhcp']
            json_input['vpn']['dhcp_over_vpn']['central']['relay_ip'] = kwargs['relay_ip']
            if kwargs['internal_dhcp']:
                ### global_vpn or remote must be choose when internal_dhcp is enable
                if kwargs['global_vpn'] or kwargs['remote']:   
                    json_input['vpn']['dhcp_over_vpn']['central']['global_vpn'] = kwargs['global_vpn']
                    json_input['vpn']['dhcp_over_vpn']['central']['remote'] = kwargs['remote']
                else:
                    logger.error('at least one value of global_vpn or remote should be true')
                    return False
                if kwargs['global_vpn'] and kwargs['remote']:
                    del json_input['vpn']['dhcp_over_vpn']['central']['send_requests']
                    del json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server']
                else:
                    json_input['vpn']['dhcp_over_vpn']['central']['send_requests'] = kwargs['send_requests']
                    if kwargs['send_requests']:
                        if 'dhcp_server_ip_list' in kwargs:
                            json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'] = []
                            i = 0
                            for server_ip in kwargs['dhcp_server_ip_list']:
                                json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'].append({})
                                json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'][i]['ip'] = server_ip
                                i += 1
                        else:
                            pass
                    else:
                        pass
            else:
                json_input['vpn']['dhcp_over_vpn']['central']['send_requests'] = kwargs['send_requests']
#                if kwargs['send_requests']:
#                    if 'dhcp_server_ip_list' in kwargs:
#                        json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'] = []
#                        i = 0
#                        for server_ip in kwargs['dhcp_server_ip_list']:
#                            json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'].append({})
#                            json_input['vpn']['dhcp_over_vpn']['central']['dhcp_server'][i]['ip'] = server_ip
#                            i += 1
#                    else:
#                        pass
#                else:
#                    pass  
        except KeyError:
            logger.error("Error: In creating JSON for dhcpovervpn centralgw")
        logger.info("dhcpovervpn centralgw json obtained")
        logger.info(json_input)      
        return json_input

    def build_json_remotegw(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_remotegw_json)
            ### vpn base setting
            json_input['vpn']['dhcp_over_vpn']['remote']['bound_to'] = kwargs['bound_to']
            #json_input['vpn']['dhcp_over_vpn']['remote']['accept_bridged_wlan_request'] = kwargs['accept_bridged_wlan_request']
            json_input['vpn']['dhcp_over_vpn']['remote']['relay_ip'] = kwargs['relay_ip']
            json_input['vpn']['dhcp_over_vpn']['remote']['management_ip'] = kwargs['management_ip']
            json_input['vpn']['dhcp_over_vpn']['remote']['block_spoof'] = kwargs['block_spoof']
            json_input['vpn']['dhcp_over_vpn']['remote']['temp_lease'] = kwargs['temp_lease']
            json_input['vpn']['dhcp_over_vpn']['remote']['lease_time'] = int(kwargs['lease_time'])
#            if 'static_device_ip_list' in kwargs and 'static_device_mac_list' in kwargs:
#                json_input['vpn']['dhcp_over_vpn']['remote']['static_device'] = []
#                i = 0
#                for device_ip in kwargs['static_device_ip_list']:
#                    json_input['vpn']['dhcp_over_vpn']['remote']['static_device'].append({})
#                    json_input['vpn']['dhcp_over_vpn']['remote']['static_device'][i]['ip'] = kwargs['static_device_ip_list'][i]
#                    json_input['vpn']['dhcp_over_vpn']['remote']['static_device'][i]['mac'] = kwargs['static_device_mac_list'][i]
#                    i += 1
#            if 'excluded_device_mac_list' in kwargs:
#                json_input['vpn']['dhcp_over_vpn']['remote']['excluded_device'] = []
#                i = 0
#                for device_mac in kwargs['excluded_device_mac_list']:
#                    json_input['vpn']['dhcp_over_vpn']['remote']['excluded_device'].append({})
#                    json_input['vpn']['dhcp_over_vpn']['remote']['excluded_device'][i]['mac'] = device_mac
#                    i += 1
        except KeyError:
            logger.error("Error: In creating JSON for dhcpovervpn remotegw")
        logger.info("dhcpovervpn remotegw json obtained")
        logger.info(json_input)      
        return json_input


class L2tpServerApi:
    '''L2tpServerApi class'''
    default_l2tpserver_options = {
        'enable': False,
        'keep_alive': 60,
        'dns_primary': '0.0.0.0',
        'dns_secondary': '0.0.0.0',
        'wins_primary': '0.0.0.0',
        'wins_secondary': '0.0.0.0',
        'ip_pool': 'local',     ### provided or local
        'ippool_begin': '0.0.0.0',
        'ippool_end': '0.0.0.0',
        'user_group': '',
    }
        
    def __init__(self, fw):
        self.fw = fw
        self.url = 'api/sonicos/vpn/l2tp-server'
        self.url_base = 'api/sonicos/vpn/l2tp-server/base'
        self.url_ppp = 'api/sonicos/vpn/l2tp-server/ppp'
        self.url_active_l2tp_server = 'api/sonicos/reporting/l2tp-server/sessions'
        self.initial_l2tpserver_json = {
            "vpn": {
                "l2tp_server": {
                    "enable": True,
                    "keep_alive": 60,
                    "dns": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0"
                    },
                    "wins": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0"
                    },
                    "ip_pool": {
                        # "provided": true
                        "local": {
                            "begin": "0.0.0.0",
                            "end": "0.0.0.0"
                        }
                    },
                    "user_group": ""
                }
            }
        }

    def config_l2tpserver(self, msg=False, **kwargs):
        self.options = dict(L2tpServerApi.default_l2tpserver_options)
        self.options.update(kwargs)         
        kwargs = self.options        
        json_input = self.build_json_l2tpserver(**kwargs)
        l2tpserver_resp = self.fw.api_put(self.url_base, msg, data=json_input)
        return l2tpserver_resp

    def show_l2tpserver(self):      
        l2tpserver_output = self.fw.api_get(self.url_base)
        return l2tpserver_output


    def modify_l2tp(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        l2tp_resp = self.fw.api_put(self.url_base, msg, data=json_input)
        return l2tp_resp


    def show_ppp_settings(self):      
        ppp_settings_output = self.fw.api_get(self.url_ppp)
        return ppp_settings_output

    def show_active_l2tp_server_section(self):      
        output = self.fw.api_get(self.url_active_l2tp_server)
        return output
        
    def enable_or_disable_l2ptpserver(self,msg=False,enable=True):
        input_json = {
            "vpn":{
                "l2tp_server":{
                    "enable":enable
                    }
                }
            }
        resp = self.fw.api_put(self.url_base, msg, data=input_json)
        return resp

    def disconnect_l2tp_client(self, client_ip):
        url_disconnect = self.url + '/disconnect/' + client_ip
        output = self.fw.api_delete(url_disconnect)
        return output

    def build_json_l2tpserver(self, **kwargs):
        json_input = {}
        logger.info(kwargs)
        try:
            json_input = copy.deepcopy(self.initial_l2tpserver_json)
            if kwargs['enable']:
                json_input['vpn']['l2tp_server']['enable'] = kwargs['enable']
                json_input['vpn']['l2tp_server']['keep_alive'] = int(kwargs['keep_alive'])
                json_input['vpn']['l2tp_server']['dns']['primary'] = kwargs['dns_primary']
                json_input['vpn']['l2tp_server']['dns']['secondary'] = kwargs['dns_secondary']
                json_input['vpn']['l2tp_server']['wins']['primary'] = kwargs['wins_primary']
                json_input['vpn']['l2tp_server']['wins']['secondary'] = kwargs['wins_secondary']
                if kwargs['ip_pool'] == 'local':
                    json_input['vpn']['l2tp_server']['ip_pool']['local']['begin'] = kwargs['ippool_begin']
                    json_input['vpn']['l2tp_server']['ip_pool']['local']['end'] = kwargs['ippool_end']
                elif kwargs['ip_pool'] == 'provided':
                    del json_input['vpn']['l2tp_server']['ip_pool']['local']    
                    json_input['vpn']['l2tp_server']['ip_pool']['provided'] = True                   
                json_input['vpn']['l2tp_server']['user_group'] = kwargs['user_group']
            else:
                del json_input['vpn']['l2tp_server']['keep_alive']
                del json_input['vpn']['l2tp_server']['dns']
                del json_input['vpn']['l2tp_server']['wins']
                del json_input['vpn']['l2tp_server']['ip_pool']
                del json_input['vpn']['l2tp_server']['user_group']
        except KeyError:
            logger.error("Error: In creating JSON for l2tpserver")
        logger.info("l2tpserver json obtained")
        logger.info(json_input)      
        return json_input
