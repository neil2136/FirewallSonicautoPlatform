from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static_dict = {
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
            'user_https': True
        }
        res = interfacecli.config_interface(**x1_static_dict)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_add_address_object(self):
        syslog_ao_dict1 = {
            "object_type": "host",
            "name": 'test_syslog1',
            "zone": "LAN",
            "value": PC1_ETH1_IP,
        }
        syslog_ao_dict2 = {
            "object_type": "host",
            "name": 'test_syslog2',
            "zone": "LAN",
            "value": PC3_ETH1_IP,
        }
        rc = ao_api.config_addressobject(**syslog_ao_dict1)
        rc &= ao_api.config_addressobject(**syslog_ao_dict2)
        Assertion.assert_equal(rc, True, "ERR: Add address objects failed")

    def test_03_add_syslog_server(self):
        syslog_param1 = {
            "name": 'test_syslog1',
            'profile': 0
        }
        syslog_param2 = {
            "name": 'test_syslog2',
            'profile': 1
        }
        ret1 = syslog_api.add_syslog_server(**syslog_param1)
        ret2 = syslog_api.add_syslog_server(**syslog_param2)
        Assertion.assert_equal(ret1 & ret2, True, "ERR: add syslog server failed")

    @repeat_method(5)
    def test_04_Register_fw(self):
        logger.info("register firewall")
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
