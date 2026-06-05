from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        rc = iface_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed!')

    def test_02_register_fw(self):
        for i in range(5):
            sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_conf_x2(self):
        rc = iface_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed!')

    def test_04_config_pkt_mon(self):
        opt = {'monitor_filter':{'destination_ports': "67,68"}}
        rc = pkt_api.conf_packmon(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config packet monitor failed!!')
