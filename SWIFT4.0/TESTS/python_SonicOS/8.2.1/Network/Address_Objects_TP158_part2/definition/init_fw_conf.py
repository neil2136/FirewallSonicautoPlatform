from definition.settings import *


class TestConfigFW_IPv4(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': PC4_ETH1_IP,
            'dns2': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_skip_automatic_update_window(self):
        autoupdatedict = {
                        "update": True,
                        "download": True,
                        "install_firmware": True,
                        "hide_advice": True,
                        "critical_only": False
                    }
        res = settingapi.edit_firmware_auto_update(**autoupdatedict)
        Assertion.assert_equal(res, True, "ERR: Skip Automatic Update window failed!!")

    def test_04_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
