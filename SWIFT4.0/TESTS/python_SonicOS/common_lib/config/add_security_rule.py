import sys
import os
import argparse
import time
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
## Add test
from utm import Firewall
from lib.modules.API import policy
from runner.settings import logger

parser = argparse.ArgumentParser(description='add security policy for policy mode.')
parser.add_argument('-ip', type=str, dest='ip', required=False, default='192.168.168.168', help='DUT ip')
parser.add_argument('-user', type=str, dest='user', required=False, default='admin', help='device user name')
parser.add_argument('-password', type=str, dest='password', required=False, default='password',help='device user password')
args = parser.parse_args()

fw = Firewall(args.ip, user=args.user, password=args.password)

policy_obj = policy.SecurityPolicyApi(fw)
policy_v4 = {
    'rule0': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_lan_v4",
                    "uuid": "200",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule1': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_wan_v4",
                    "uuid": "201",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule2': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_dmz_v4",
                    "uuid": "202",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule3': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_vpn_ping_v4",
                    "uuid": "203",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "group": 'Ping'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule4': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_dmz_to_dmz_v4",
                    "uuid": "204",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule5': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_dmz_to_wan_v4",
                    "uuid": "205",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    }, 
    'rule6': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_wan_to_wan_ping_v4",
                    "uuid": "206",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "WAN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X1 Management IP'
                        }
                    },
                    "service": {
                        "group": 'Ping'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule7': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_wan_to_wan_https_v4",
                    "uuid": "207",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "WAN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X1 Management IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule8': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_wan_to_wan_http_v4",
                    "uuid": "208",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "WAN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X1 Management IP'
                        }
                    },
                    "service": {
                        "name": 'HTTP Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule9': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_lan_ssh_v4",
                    "uuid": "209",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule10': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_lan_ping_v4",
                    "uuid": "210",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "group": 'Ping'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule11': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_lan_https_v4",
                    "uuid": "211",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule12': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_lan_http_v4",
                    "uuid": "212",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "name": 'HTTP Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule13': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_dmz_snmp_v4",
                    "uuid": "213",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule14': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_dmz_ssh_v4",
                    "uuid": "214",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule15': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_dmz_https_v4",
                    "uuid": "215",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule16': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_lan_ping_v4",
                    "uuid": "216",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All X0 Management IP'
                        }
                    },
                    "service": {
                        "group": 'Ping'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule17': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_lan_snmp_v4",
                    "uuid": "217",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule18': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_lan_ssh_v4",
                    "uuid": "218",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule19': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_lan_https_v4",
                    "uuid": "219",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule20': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_sslvpn_v4",
                    "uuid": "220",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "SSLVPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule21': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_sslvpn_ssh_v4",
                    "uuid": "221",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "SSLVPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule22': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_sslvpn_https_v4",
                    "uuid": "222",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "SSLVPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule23': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_vpn_snmp_v4",
                    "uuid": "223",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule24': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_vpn_ssh_v4",
                    "uuid": "224",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule25': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_vpn_https_v4",
                    "uuid": "225",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule26': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_wan_snmp_v4",
                    "uuid": "226",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule27': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_wan_ssh_v4",
                    "uuid": "227",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule28': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_vpn_to_wan_https_v4",
                    "uuid": "228",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IP'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule29': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_dmz_to_lan_v4",
                    "uuid": "229",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "deny",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule30': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_wan_to_lan_v4",
                    "uuid": "230",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "WAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "deny",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule31': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_wan_to_dmz_v4",
                    "uuid": "231",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "WAN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "deny",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule32': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_lan_to_vpn_v4",
                    "uuid": "232",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "name": 'WAN RemoteAccess Networks'
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule33': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_dmz_to_vpn_v4",
                    "uuid": "233",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "name": 'WAN RemoteAccess Networks'
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
   'rule34': {
        "security_policies": [
            {
                "ipv4": {
                    "name": "default_dmz_to_vpn_v4",
                    "uuid": "234",
                    "enable": True,
                    "priority": {
                        "manual": 1
                    },
                    "comment": "IPv4:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "name": 'WAN RemoteAccess Networks'
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
}

policy_v6 = {
    'rule0': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_lan_v6",
                    "uuid": "100",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule1': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_wan_v6",
                    "uuid": "101",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule2': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_dmz_v6",
                    "uuid": "102",
                    "enable": True,
                    "priority": {
                        "manual":100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule3': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_vpn_ping6_v6",
                    "uuid": "103",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "group": 'Ping6'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule4': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_dmz_to_dmz_v6",
                    "uuid": "104",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule5': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_dmz_to_wan_v6",
                    "uuid": "105",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "DMZ",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "any": True
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule6': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_lan_ssh_v6",
                    "uuid": "106",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule7': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_lan_ping6_v6",
                    "uuid": "107",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "group": 'Ping6'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule8': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_lan_https_v6",
                    "uuid": "108",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule9': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_lan_to_lan_http_v6",
                    "uuid": "109",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "LAN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'HTTP Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule10': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_dmz_snmp_v6",
                    "uuid": "110",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "DMZ",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule13': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_lan_ping6_v6",
                    "uuid": "113",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'X0 Management IPv6 Addresses'
                        }
                    },
                    "service": {
                        "group": 'Ping6'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule14': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_lan_snmp_v6",
                    "uuid": "114",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "LAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule17': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_sslvpn_v6",
                    "uuid": "117",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "SSLVPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule20': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_vpn_snmp_v6",
                    "uuid": "120",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule21': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_vpn_ssh_v6",
                    "uuid": "121",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SSH Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule22': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_vpn_https_v6",
                    "uuid": "122",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "VPN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'HTTPS Management'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
    'rule23': {
        "security_policies": [
            {
                "ipv6": {
                    "name": "default_vpn_to_wan_snmp_v6",
                    "uuid": "123",
                    "enable": True,
                    "priority": {
                        "manual": 100
                    },
                    "comment": "IPv6:From Any to Any for Any service",
                    "from": "VPN",
                    "to": "WAN",
                    "source": {
                        "address": {
                            "any": True
                        },
                        "port": {
                            "any": True
                        }
                    },
                    "destination": {
                        "address": {
                            "group": 'All Interface IPv6 Addresses'
                        }
                    },
                    "service": {
                        "name": 'SNMP'
                    },
                    "users": {
                        "all": True
                    },
                    "match_operation": "or",
                    "application": {
                        "any": True
                    },
                    "and_all_matched_applications": False,
                    "web_category": {
                        "any": True
                    },
                    "url_list": {
                        "any": True
                    },
                    "custom_match": {
                        "any": True
                    },
                    "country": {
                        "any": True
                    },
                    "schedule": {
                        "always_on": True
                    },
                    "action": "allow",
                    "action_profile": "Default Profile",
                }
            }
        ]
    },
}
tc = True
tcs = True
for policy in policy_v6.values():
    logger.info(f"Add IPv6 rules from {policy['security_policies'][0]['ipv6']['from']} to {policy['security_policies'][0]['ipv6']['to']}.")
    tc = policy_obj.add_security_policy(**policy)
    time.sleep(1)
    if not tc:
        logger.error(f"Add IPv6 rules from {policy['security_policies'][0]['ipv6']['from']} to {policy['security_policies'][0]['ipv6']['to']} failed.")
        tcs &= tc
for policy in policy_v4.values():
    logger.info(f"Add IPv4 rules from {policy['security_policies'][0]['ipv4']['from']} to {policy['security_policies'][0]['ipv4']['to']}.")
    tc = policy_obj.add_security_policy(**policy)
    time.sleep(1)
    if not tc:
        logger.error(f"Add IPv4 rules from {policy['security_policies'][0]['ipv4']['from']} to {policy['security_policies'][0]['ipv4']['to']} failed.")
        tcs &= tc
if tcs:
    logger.info('Add security rule successfully.')
    exit(0)
else:
    logger.info('Add security rule unsuccessfully.')
    exit(1)        
