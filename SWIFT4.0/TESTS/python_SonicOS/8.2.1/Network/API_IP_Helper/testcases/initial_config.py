from parameter import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    def test_00_01_Config_X2(self):
        x2_static_opt = {
           'if': 'x2',
           'zone': 'WAN',
           'mode': 'static',
           'ip': Parameter.X2_IP,
           'netmask': '255.255.255.0',
           'gateway': '0.0.0.0',
           'mgmt_http': False,
        }
        output = interface_ipv4.config_interface(**x2_static_opt)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")


if __name__ == '__main__':
    config_fw = TestConfigFW()
