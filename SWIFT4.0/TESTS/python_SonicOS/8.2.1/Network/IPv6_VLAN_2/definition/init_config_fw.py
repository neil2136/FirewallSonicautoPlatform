from definition.settings import *


class TestConfig_FW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_addsubif_for_x1(self):
        x1_vlan = {
            'if': 'x1',
            'type': 'vlan',
            'vlan_tag': X1_VLAN_ID,
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_V1_IP,
            'mgmt_ping': True,
            'mgmt_https': True,
        }
        res = interfacev4api.add_interface(**x1_vlan)
        Assertion.assert_equal(
            res, True, "ERR: add sub vlan if for X1 failed.")

    def test_02_addsubif_for_X3(self):
        x3_vlan1 = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN_ID1,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_V1_IP,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        x3_vlan2 = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN_ID2,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_V2_IP,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res1 = interfacev4api.add_interface(**x3_vlan1)
        res2 = interfacev4api.add_interface(**x3_vlan2)
        Assertion.assert_equal(
            res1 & res2, True, "ERR, add sub vlans for x3 failed")

    def test_03_config_x3_vlan_v6(self):
        x3_vlan1_v6 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID1,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V1_V6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
        x3_vlan2_v6 = {
            'name': 'X3',
            'vlan': X3_VLAN_ID2,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V2_V6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'ra_max': 30
        }
        res1 = interfacev6api.config_interface_ipv6(**x3_vlan1_v6)
        res2 = interfacev6api.config_interface_ipv6(**x3_vlan2_v6)
        Assertion.assert_equal(
            res1 & res2, True, 'ERR: config ipv6 addrs for vlan1 and vlan2 failed.')
