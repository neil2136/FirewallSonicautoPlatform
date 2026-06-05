from definition.settings import *


class TestConfigFW_IPv4(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': PC3_ETH1_IP,
            'dns2': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_Config_X2(self):
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    # disable dns proxy cache due to jira issue,when jira is fixed, should remove this step
    def test_04_disable_dns_proxy_cache(self):
        dnsproxy_dict = {
            "dns_proxy": {
                # "enable": True,
                # "mode": "ipv4-to-ipv4",
                # "protocol": "udp-only",
                "enforce_all_dns_requests": False,
                "dns_cache": False
            }
        }
        res = fw_api.api_put('api/sonicos/dns-proxy/base',False, dnsproxy_dict)
        # res = dnsproxyapi.config_dnsproxy()
        Assertion.assert_equal(res, True, "ERR: disable dns proxy cache failed")


class TestConfigFW_IPv6(Test):
    uuid = 'NonTC'

    def test_01_config_x0_v6(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPv6,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfaceipv6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X0 IPv6 address failed")

    def test_02_config_x1_v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True,
            'dns': {'primary': PC3_ETH1_IPv6}
        }
        res = interfaceipv6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X1 IPv6 address failed")

    def test_03_config_x2_v6(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_IPv6,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfaceipv6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 IPv6 address failed")

    def test_04_add_ipv6_nat_policy(self):
        nat_dict = {
            "nat_policies": [
                {
                    "ipv6": {
                        "comment": "ipv6_nat_added",
                        "destination": {
                            "any": True
                        },
                        "enable": True,
                        "inbound": "any",
                        "name": "customipv6nat",
                        "outbound": "any",
                        "priority": {
                            "auto": True
                        },
                        "reflexive": False,
                        "service": {
                            "any": True
                        },
                        "source": {
                            "any": True
                        },
                        "source_port_remap": True,
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        },
                        "translated_destination": {
                            "original": True
                        },
                        "translated_service": {
                            "original": True
                        },
                        "translated_source": {
                            "name": "X1 IPv6 Primary Static Address"
                        }
                    }
                }
            ]
        }
        res = natpolicyapi.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, "ERR: add ipv6 nat policy failed")

    # # 8.2.0 dns_proxy_cache is enabled by default，jira exists
    # def test_05_disable_dns_proxy_chache(self):
    #     default_options = {
    #     'enable': False,
    #     'mode': 'ipv4-to-ipv4',
    #     # 'protocol': 'udp-only',
    #     'enforce_all_dns_requests': False,
    #     'dns_cache': False
    # }








