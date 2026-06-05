from definition.initial_parameter import *


class TestInitConfig(Test):
    uuid = 'NonTC'
   
    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_disable_icmp_settings(self):
        logger.info('disable enforceDropUnreachICMP and enforceDropTimeExceedICMP in diag.html')
        diag_icmp_settings = {
            'stream': 'enforceDropUnreachICMP=&enforceDropTimeExceedICMP='
        }
        rc = diagObj.config_raw_api(**diag_icmp_settings)
        Assertion.assert_equal(rc, True, "ERR: disable enforceDropUnreachICMP and enforceDropTimeExceedICMP in diag.html failed")
