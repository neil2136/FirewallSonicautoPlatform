from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize Firewall interface config'

    def test_01_static_x1(self):
        config_x1 = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True, }
        rc = interfaceapi.config_interface(**config_x1)
        Assertion.assert_equal(rc, True, "=====> ERR: Configure X1 failed!")

    @repeat_method(5)
    def test_02_register(self):
        time.sleep(20)
        res = lc.register(mode='online')
        Assertion.assert_equal(res, True, 'ERR: register firewall failed')
