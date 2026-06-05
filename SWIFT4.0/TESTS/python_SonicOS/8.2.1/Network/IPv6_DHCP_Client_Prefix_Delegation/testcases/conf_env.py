from settings import *

fw = Firewall(Parameter.DUT_X0_IP, user='admin', password='password')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
dhcp_v6 = network.DHCPServerApi(fw)


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_config_X2(self):
        X2_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'gateway': Parameter.DUT_X2_GW,
            'dns1': Parameter.DNS,
        }
        rc = interface.config_interface(**X2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_02_config_X3(self):
        X3_static = {
            'if': 'X3',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'gateway': Parameter.DUT_X3_GW,
            'dns1': Parameter.DNS,
        }
        rc = interface.config_interface(**X3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_00_03_config_dhcp_scope(self):
        dhcp_server_ipv6_scope = {
            "dhcp_server": {
                "ipv6": {
                    "scope": {
                        "dynamic": [
                            {
                                "name": "scope_ipv6",
                                "enable": True,
                                "prefix": Parameter.DUT_X0_PREFIX,
                                "range": {
                                    "from": Parameter.DHCP_SCOPE[0],
                                    "to": Parameter.DHCP_SCOPE[1],
                                }
                            }
                        ]
                    }
                }
            }
        }
        rc = dhcp_v6.add_dhcp_server_scope_dynamic(**dhcp_server_ipv6_scope)    
        Assertion.assert_equal(rc, True, "ERR: Add dhcp scope failed")

    def test_00_04_config_X2_dhcp_PD(self):
        X2_ipv6_dhcp = {
            'name': 'X2',
            'mode': 'dhcpv6',
            'dhcpv6': {
                'prefix_delegation': True, 
            }
        }
        rc = interface_v6.config_interface_ipv6(**X2_ipv6_dhcp)
        Assertion.assert_equal(rc, True, "ERR: config X2 ipv6 to dhcp fail .")

    def test_00_05_config_X3_IPv6(self):
        x3_pd = {
            'name': 'X3',
            'mode': 'static',
            'type': 'prefix_delegation',
            'preferred_ip': Parameter.EXTRA_IP,
            'delegated_prefix': 'X2 Delegated Prefix',
            'prefix_length': 64,
        }
        rc = interface_v6.add_ipv6_extra_ip(**x3_pd)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv6 failed")


