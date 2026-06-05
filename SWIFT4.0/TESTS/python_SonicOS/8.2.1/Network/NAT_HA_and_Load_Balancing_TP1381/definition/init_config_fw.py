from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
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

    def test_02_add_acl_wan_to_lan_ping(self):
        acl_dict = deepcopy(acl_base)
        acl_dict.update({"name": "wan_to_lan", "to": "LAN", "service": {"group": "Ping"}})
        res = acl_api.config_accessrule(**acl_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add acl allow wan to lan ipv4 failed!\033[0m')

    def test_03_add_X1_NAT_ao(self):
        ao_dict = {
            "object_type": "host",
            "name": "X1_NAT",
            "zone": "WAN",
            "value": Parameter.X1_NAT_IP
        }
        res = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add X1 NAT addr object failed!\033[0m')

    def test_04_add_dst_nat_range_x0(self):
        ao_dict = {
            "object_type": "range",
            "name": "X0_range",
            "zone": "LAN",
            "value": "192.168.168.169,192.168.168.170"
        }
        res = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add X1 NAT addr object for X1 interface failed!\033[0m')

    def test_05_add_src_nat_network(self):
        ao_dict = {
            "object_type": "network",
            "name": "x1_net",
            "zone": "WAN",
            'value': "12.12.1.0,255.255.255.0",
        }
        res = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add src network for nat rule failed!\033[0m')

    def test_06_add_dst_nat_network(self):
        ao_dict = {
            "object_type": "network",
            "name": "x0_net",
            "zone": "LAN",
            'value': "192.168.168.0,255.255.255.0",
        }
        res = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add src network for nat rule failed!\033[0m')

    def test_06_config_x2_dmz(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = if_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(res, True, '\033[1;31mERR: config x2 ipv4 failed!\033[0m')

    def test_07_add_src_nat_range_x2(self):
        ao_dict = {
            "object_type": "range",
            "name": "X2_range",
            "zone": "LAN",
            "value": "13.13.1.169,13.13.1.170"
        }
        res = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, '\033[1;31mERR: add X1 NAT addr object for X2 interface failed!\033[0m')

    def test_08_register_fw(self):
        for i in range(5):
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
        