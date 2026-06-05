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
        out = if_v6_api.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 ipv6 failed!")
    
    def test_02_config_x1_v6(self):
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_V6_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        out = if_v6_api.config_interface_ipv6(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 ipv6 failed!")
    
    def test_03_assign_x2_to_dmz(self):
        x2_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': '13.13.1.168',
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        res = if_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(res, True, "ERR: assign x2 to dmz failed")
    
    def test_04_config_x2_v6(self):
        x2_v6_opt = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'DMZ',
            'ip': Parameter.X2_V6_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        out = if_v6_api.config_interface_ipv6(**x2_v6_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 ipv6 failed!")
    
    def test_05_add_nat_ao(self):
        res = False
        wan_host = {'object_type': 'host', 'name': "wan_host", 'zone': 'WAN', 'ip': PC2_ETH1_V6}
        lan_host = {'object_type': 'host', 'name': 'lan_host', 'zone': 'LAN', 'ip': PC1_ETH1_V6}
        dmz_host = {'object_type': 'host', 'name': 'dmz_host', 'zone': 'DMZ', 'ip': "2002::169"}
        wan_nat = {'object_type': 'host', 'name': 'wan_nat', 'zone': 'WAN', 'ip': Parameter.X1_V6_NAT}
        dmz_nat = {'object_type': 'host', 'name': 'dmz_nat', 'zone': 'DMZ', 'ip': Parameter.X2_V6_NAT}
        ao_objs = (wan_host, lan_host, dmz_host, wan_nat, dmz_nat)
        for ao in ao_objs:
            res = ao_api.config_ipv6_addressobject(**ao)
            if not res:
                logger.error(f'add {ao} failed')
                break
        Assertion.assert_equal(res, True, "ERR: Add nat addr objects failed!")
    
    def test_06_add_wan_to_lan_ping_acl(self):
        acl_dict = {
            "access_rules": [
                {
                    "ipv6": {
                        "name": "wan_to_lan_acl_ping",
                        "enable": True,
                        "from": "WAN",
                        "to": "LAN",
                        "action": "allow",
                        "source": {
                            "address": {"any": True},
                            "port": {"any": True}
                        },
                        "service": {"group": "Ping6"},
                        "destination": {"address": {"any": True}},
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
                        "comment": "None",
                        "fragments": True,
                        "logging": True,
                        "flow_reporting": False,
                        "botnet_filter": False,
                        "geo_ip_filter": {"enable": False},
                        "packet_monitoring": False,
                        "management": False,
                        "max_connections": 100,
                        "priority": {
                            "auto": True
                        },
                        "tcp": {
                            "timeout": 15
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
                        "quality_of_service": {
                            "dscp": {
                                "preserve": True
                            },
                            "class_of_service": {}
                        }
                    }
                }
            ]
        }
        res = acl_api.add_accessrule_ipv6(**acl_dict)
        Assertion.assert_equal(res, True, 'ERR: add acl allow wan to lan failed.')
    
    def test_07_add_custom_service(self):
        ser_dict = {
            'object_type': 'tcp',
            "name": "tcp-8888",
            "tcp": {
                "begin": 8888,
                "end": 8888
            }
        }
        res, _ = service_api.config_service_object(**ser_dict)
        Assertion.assert_equal(res, True, 'ERR: add service object failed.')

    def test_08_config_x1(self):
        x1_opt = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': "12.12.1.1"

        }
        rc = if_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed!')

    def test_09_register_fw(self):
        for i in range(5):
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
