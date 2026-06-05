from settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacecfgapi.config_interface(**x1_static)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")
