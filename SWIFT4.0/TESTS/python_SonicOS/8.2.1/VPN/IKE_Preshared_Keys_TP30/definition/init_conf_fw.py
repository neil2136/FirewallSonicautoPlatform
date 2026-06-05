from definition.settings import *


class TestLocalFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        x2_static_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        res = interfaceapi.config_interface(**x2_static_dict)
        Assertion.assert_equal(res, True, "ERR: Config remote X3 to static failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")



