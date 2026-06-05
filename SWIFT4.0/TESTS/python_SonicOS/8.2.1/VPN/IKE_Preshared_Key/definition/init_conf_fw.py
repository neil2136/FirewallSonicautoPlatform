from definition.settings import *


class TestLocalFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x2_to_wan(self):
        x2_wan_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '22.22.22.168',
            'netmask': '255.255.255.0',
            'gateway': '22.22.22.1',
            'dns1': '10.103.202.200',
            'dns2': '8.8.8.8',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }

        rc = interfaceapi.config_interface(**x2_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to wan failed")

    def test_02_configure_dut_failover(self):
        wlb_conf_dict = {
            "failover_lb": {
                "group": [
                    {
                        "final_backup": "",
                        "interface": [
                            {
                                "name": "X2",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 1
                            },
                            {
                                "name": "X1",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 2
                            }
                        ],
                        "name": " Default LB Group",
                        "preempt": True,
                        "probing": {
                            "global_responder": False,
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3
                        },
                        "type": "basic"
                    }
                ]
            }
        }
        res = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config DUT failover failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_config_x2_to_unasign(self):
        rc = interfaceapi.unassign_interface(interface='X2')
        Assertion.assert_equal(rc, True, "ERR: Config X2 to unassign failed")
