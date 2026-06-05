from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_configure_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': "10.10.0.1"
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_x1_again(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2
        }
        res = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_04_config_x3_to_WAN(self):
        x3_static = {
            'if': 'X3',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True
        }
        res = interfacev4api.config_interface(**x3_static)
        Assertion.assert_equal(res, True, 'ERR: config x3 failed')

    def test_05_config_x4_to_DMZ(self):
        x4_dict = {
            'if': 'X4',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_https': True
        }
        res = interfacev4api.config_interface(**x4_dict)
        Assertion.assert_equal(res, True, 'ERR: config x4 failed')

    def test_06_configure_x5_to_DMZ(self):
        x5_dict = {
            'if': 'X5',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'netmask': '255.255.255.0',
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_https': True
        }
        res = interfacev4api.config_interface(**x5_dict)
        Assertion.assert_equal(res, True, 'ERR: config x5 failed')

    def test_07_add_aos(self):
        tag = []
        wan_host1 = {
            'object_type': 'host',
            "name": "wan_ao1",
            "zone": "WAN",
            "value": Parameter.X1_NAT_IP
        }
        wan_host2 = {
            'object_type': 'host',
            "name": "wan_ao2",
            "zone": "WAN",
            "value": Parameter.X3_NAT_IP
        }
        dmz_pc1 = {
            'object_type': 'host',
            'name': 'dmz_pc1',
            'zone': 'DMZ',
            'value': PC3_ETH1_IP
        }
        dmz_pc2 = {
            'object_type': 'host',
            'name': 'dmz_pc2',
            'zone': 'DMZ',
            'value': PC4_ETH1_IP
        }

        ao_list = [wan_host1, wan_host2, dmz_pc1, dmz_pc2]
        for ao in ao_list:
            res = aoapi.config_addressobject(**ao)
            tag.append(res)
        Assertion.assert_equal(all(tag), True, 'ERR: add aos failed')

    def test_08_config_x3_to_wlb(self):
        wlb_json = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        # "preempt":True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X3",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            }
                        ]
                    }
                ]
            }
        }
        res = wlbapi.config_failover_groups_by_multi(**wlb_json)
        Assertion.assert_equal(
            res, True, 'ERR: config x3 to default wlb failed')
