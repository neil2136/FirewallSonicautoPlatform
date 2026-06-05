from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_pkt_mon(self):
        param = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '546,547'
            }
        }
        res = pkt_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')
    
    def test_02_set_ipv6_x1_to_dhcpv6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                "mode": "manual",
                # 'prefix_delegation': True
                'prefix_delegation': {"preferred": {}}
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')


