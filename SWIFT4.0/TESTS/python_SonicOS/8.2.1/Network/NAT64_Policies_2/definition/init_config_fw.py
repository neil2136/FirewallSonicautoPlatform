from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x0_v6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        res = if_v6_api.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(res, True, "\033[1;31mERR: Configure X0 ipv6 failed!\033[0m")

    def test_02_config_x1_v4(self):
        x1_opt = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': "12.12.1.1",
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X2_DNS_2,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = if_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(res, True, '\033[1;31mERR: config x1 ipv4 failed!\033[0m')

    def test_03_register_fw(self):
        for i in range(10):
            sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_config_x1_v6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X1_V6_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        out = if_v6_api.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "\033[1;31mERR: Configure X1 ipv6 failed!\033[0m")

    def test_05_config_x2_v4(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = if_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(res, True, '\033[1;31mERR: config x2 ipv4 failed!\033[0m')

    def test_06_config_x2_v6(self):
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X2_V6_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        out = if_v6_api.config_interface_ipv6(**x2_opt)
        Assertion.assert_equal(out, True, "\033[1;31mERR: Configure X2 ipv6 failed!\033[0m")

    def test_07_add_wan_to_wan_acl(self):
        acl_dict = deepcopy(acl_base)
        acl_dict.update({"name": "wan_to_wan"})
        res = acl_api.config_accessrule(**acl_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add acl allow wan to wan ipv4 failed!\033[0m')

    def test_08_add_wan_to_wan_v6_acl(self):
        acl_dict = {
            'option': "add",
            "from": "WAN",
            "to": "WAN",
            "action": "allow",
            "name": "wan_to_wan",
        }
        res = acl_v6_api.config_ipv6_access_rule(**acl_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add acl allow wan to wan ipv6 failed!\033[0m')

    # def test_09_config_packet_mon(self):
    #     param = {
    #         'monitor_filter': {
    #             'ip_types': 'icmp,icmpv6'
    #         }
    #     }
    #     res = pkt_api.conf_packmon(**param)
    #     Assertion.assert_equal(res, True, '\033[1;31mERR: config packet monitor failed!\033[0m')

    def test_10_add_wan_to_lan_acl(self):
        acl_dict = deepcopy(acl_base)
        acl_dict.update({"name": "wan_to_lan", "to": "LAN", "service": {"group": "Ping"}})
        res = acl_api.config_accessrule(**acl_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add acl allow wan to lan ipv4 failed!\033[0m')

    def test_11_add_wan_to_dmz_acl_v6_ping6(self):
        acl_dict = {
            "access_rules": [
                {
                    "ipv6": {
                        "name": "wan_to_dmz_ping6",
                        "enable": True,
                        "from": "WAN",
                        "to": "DMZ",
                        "action": "allow",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "service": {
                            "group": "Ping6"
                        },
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "schedule": {
                            "always_on": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "comment": "",
                        "fragments": True,
                        "logging": True,
                        "sip": False,
                        "h323": False,
                        "flow_reporting": False,
                        "botnet_filter": False,
                        "geo_ip_filter": {
                            "enable": False,
                            "global": True
                        },
                        "block": {
                            "countries": {
                                "unknown": False
                            }
                        },
                        "packet_monitoring": False,
                        "management": False,
                        "max_connections": 100,
                        "priority": {
                            "auto": True
                        },
                        "tcp": {
                            "timeout": 5,
                            "urgent": False
                        },
                        "udp": {
                            "timeout": 30
                        },
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                        },
                        "dpi": True,
                        "dpi_ssl": {
                            "client": True,
                            "server": True
                        },
                        "redirect_unauthenticated_users_to_log_in": True,
                        "quality_of_service": {
                            "class_of_service": {},
                            "dscp": {
                                "preserve": True
                            }
                        }
                    }
                }
            ]
        }
        res = acl_v6_api.add_accessrule_ipv6(**acl_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add acl allow wan to dmz ipv6 failed!\033[0m')
