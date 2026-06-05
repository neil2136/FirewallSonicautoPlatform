from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_01_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '12.12.1.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_v6_addr_for_x0(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '2000::168',
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X0 IPv6 static failed")

    def test_04_config_v6_addr_for_x1(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '2010::168',
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X1 IPv6 static failed")

    def test_05_add_probe_v6_addr_for_nm_policy(self):
        host_dict = {
            "object_type": 'host',
            'name': 'probe_wan_host',
            'zone': 'WAN',
            'value': '2010::100'
        }
        rc = ao_api.config_addressobject(**host_dict)
        Assertion.assert_equal(rc, True, "ERR: add probe v6 addr object for nm policy failed!!")

    def test_06_add_probe_v6_range_addr_obj_for_nm_policy(self):
        range_dict = {
            "object_type": "range",
            "name": "probe_wan_range",
            "zone": "WAN",
            "value": "2010::1,2010::ffff"
        }
        rc = ao_api.config_addressobject(**range_dict)
        Assertion.assert_equal(rc, True, 'ERR: add_probe_v6_range_addr_obj_for_nm_policy!!')
