from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_config_dut1_x2_to_wan(self):
        res = interfacev4api.config_interface(**x2_static_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to static wan failed")

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
        rc = interfacev4api.unassign_interface(interface='X2')
        Assertion.assert_equal(rc, True, "ERR: Config X2 to unassign failed")

