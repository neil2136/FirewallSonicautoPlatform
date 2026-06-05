import sys
import os
sys.path.append(os.environ["SONICOS_HOME"]+'/7.0.0/python_lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall

ip = '192.168.168.168'

from modules.API import policy

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
route_obj = policy.RoutePolicyApi(fw)
route_policy = {
    "route_policies": [
        {
            "ipv4": {
                "interface": "X2",
                "metric": 1,
                "source": {
                    "any": True
                },
                "destination": {
                    "name": "test"
                },
                "service": {
                    "any": True
                },
                "gateway": {
                    "default": True
                },
                "tos": "",
                "mask": "",
                "distance": {
                    "auto": True
                },
                #"uuid": "00000000-0000-0001-0900-004010292f2d",
                "name": "test",
                "type": "standard",
                "priority": 1,
                "comment": "",
                "disable_on_interface_down": True,
                "vpn_precedence": False,
                "probe": "",
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        }      
    ]
} 
                
#ret = route_obj.add_route_policy(**route_policy)
#ret = route_obj.del_route_policy('test')
#print(ret)
decryption_obj = policy.DecryptionPolicyApi(fw)
decryption_policy = {
    "decryption_policy": {
        "client": [
            {
                "name": "test",
                "uuid": "00000000-0000-0001-1e00-004010292f2d",
                "enable": True,
                "priority": {
                    "manual": 1
                },
                "source": {
                    "address": {
                        "name": "X0 Subnet"
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
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    }
                }, 
                "comment": "",
                "match_operation": {
                    "or": True
                },
                "action": {
                    "decrypt": True
                },
                "web_category": {
                    "any": True
                },
                "web_site": {
                    "any": True
                },
                "country": {
                    "any": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                },
                "ip_type": "ipv4"
            }
        ]
    }
}
#ret = decryption_obj.add_decryption_policy(**decryption_policy)
#print(ret)
decryption_policy1 = {
    "decryption_policy": {
        "client": [
            {
                "name": "test1",
                #"uuid": "00000000-0000-0021-1e00-004010292f2d",
                "enable": True,
                "priority": {
                    "manual": 3
                },
                "source": {
                    "address": {
                        "name": "X0 Subnet"
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
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "all": True
                    }
                }, 
                "comment": "",
                "match_operation": {
                    "or": True
                },
                "action": {
                    "decrypt": True
                },
                "web_category": {
                    "any": True
                },
                "web_site": {
                    "any": True
                },
                "country": {
                    "any": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                },
                "ip_type": "ipv4"
            }
        ]
    }
}
#ret = decryption_obj.edit_decryption_policy('test1', **decryption_policy1)
#ret = decryption_obj.get_decryption_policies_statistics()
#ret = decryption_obj.get_decryption_policy_statistics("test1")
#print(ret)
#ret = decryption_obj.get_decryption_policy()
#print(ret)
#ret = decryption_obj.del_decryption_policy('test', 'client')
#print(ret)

policy_setting = {
    "dpi_ssl": {
        "client": {
            "enable": True,
            "authenticate_server_for_decrypted_connections": False,
            "deployment_server_domains": True,
            "bypass_decryption": True,
            "audit_built_in_exclusion": False,
            "authenticate_server": False,
            "resigning_authority": {
                "default": "2048-bit"
            }
        }
    }
}
#policy_setting_obj = policy.PolicySettingsApi(fw)
#rc = policy_setting_obj.config_dpi_ssl_client_general(**policy_setting)

#dos_obj = policy.DosPolicyApi(fw)
#ret = dos_obj.get_dos_policy()
dos_dic = {
    "dos_policies": [
        {
            "uuid": "00000000-0000-0001-1d00-004010292f2d",
            "name": "test",
            "id": 1,
            "priority": {
                "manual": 1
            },
            "enable": True,
            "comment": "",
            "destination": {
                "address": {
                    "any": True
                }
            },
            "source": {
                "address": {
                    "name": "X1 Subnet"
                }
            },
            "ip_version": "ipv4",
            "service": {
                "any": True
            },
            "schedule": {
                "always_on": True
            },
            "action": "protect",
            "action_profile": "Default DoS Action Profile",
            "ticket": {
                "tag1": "",
                "tag2": "",
                "tag3": ""
            }
        }
    ]
}
#ret = dos_obj.add_dos_policy(**dos_dic)
#ret = dos_obj.del_dos_policy("test")
#print(ret)


from lib.modules.API.policy import SecurityPolicyApi
import requests

fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
security_policy_obj = SecurityPolicyApi(fw)
security_policy_lan_to_wan = {
    "security_policies": [
        {
            "ipv4": {
                "name": "lan_to_wan",
                "uuid": "2",
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
                    "group": "web cat"
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
                "action": "service",
                "default_action": "allow",
                "action_profile": "action profile test"
            }
        }
    ]
}
# rc = security_policy_obj.add_security_policy(**security_policy_lan_to_wan)
# rc = security_policy_obj.del_security_policy('any')
#
# rc = security_policy_obj.del_security_policy('lan_to_wan')
security_policy_any_ipv6 = {
    "security_policies": [{
        "ipv6": {
            "uuid": "2",
            "name": "any_ipv6",
            "enable": True,
            "priority": {
                "manual": 3
            },
            "comment": "IPv4:From Any to Any for Any service",
            "from": "any",
            "to": "any",
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
            "action": "service",
            "default_action": "allow",
            "action_profile": "Default Profile"
        }
    }]
}
rc = security_policy_obj.add_security_policy(**security_policy_any_ipv6)


shadow_obj = policy.ShadowApi(fw)
#ret = shadow_obj.generate_rule_list("decryption-policies")
#ret = shadow_obj.export_rule_list("decryption-policies")
#print(ret)


policy_setting = {
#    "dpi_ssl": {
#        "server": {
#            "enable": True,
#        }
#    }
#}
#rc = policy_setting_obj.config_dpi_ssl_server_general(**policy_setting)

nat_obj = policy.NatPolicyApi(fw)

nat_dic = {
    "nat_policies":[
        {
            "ipv4": {
                #"uuid": "903e2aa9-c782-a2a6-0800-004010292f2d",
                "name": "My Rule",
                "enable": True,
                "comment": "",
                "dns_doctoring": False,
                #"priority": {
                #    "auto": True
                #},
                "inbound": "any",
                "outbound": "any",
                "source": {
                    "any": True
                },
                "translated_source": {
                    "original": True
                },
                "destination": {
                    "name": "X1 IP"
                },
                "translated_destination": {
                    "original": True
                },
                "service": {
                    "name": "SNMP"
                },
                "translated_service": {
                    "original": True
                },
                "ticket": {
                    "tag1": "",
                    "tag2": "",
                    "tag3": ""
                }
            }
        }
    ]
}
#ret = nat_obj.add_nat_policy(**nat_dic)
ret = nat_obj.del_nat_policy("My Rule")
print(ret)


