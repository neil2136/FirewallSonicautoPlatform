from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 ipv4 address failed")

    def test_02_config_x2(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_v4_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 ipv4 address failed")

    def test_03_create_probe_target_lan_host_pc2_eth2(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc2_eth2",
            "zone": "LAN",
            "value": PC2_ETH2_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_04_create_probe_target_wan_host_pc2_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc2_eth1",
            "zone": "WAN",
            "value": PC2_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_05_create_probe_target_lan_host_pc3_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc3_eth1",
            "zone": "LAN",
            "value": PC3_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_06_create_lan_ao_group_include_pc2_eth2_and_pc3_eth2(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "pc2_eth2"
                                },
                                {
                                    "name": "pc3_eth1"
                                },
                            ]
                        },
                        "name": "lanprobgroup"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add probe ao group failed")

    def test_07_create_probe_target_x1_gateway_host_ao(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "x1_gw",
            "zone": "WAN",
            "value": Parameter.X1_GW
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_08_create_probe_target_x1_gw_unreachable_host_ao(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "gw_unreachable",
            "zone": "WAN",
            "value": "12.12.1.10"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_09_create_probe_target_with_x2_range_ao(self):
        probe_object_dict = {
            "object_type": "range",
            "name": "range_ao",
            "zone": "LAN",
            "value": "193.168.1.20,193.168.1.22"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_10_create_probe_target_host(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "10.103.202.200",
            "zone": "WAN",
            "value": "10.103.202.200"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")

    def test_11_create_probe_target_unreachable_x2(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "x2_unreacheable_host",
            "zone": "LAN",
            "value": "193.168.168.200"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe address object failed")







