from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        x1_opt = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': "12.12.1.1",
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X2_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = iface_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_02_register_fw(self):
        for i in range(10):
            sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_addr_obj_for_syslog_server(self):
        ao_opt = {
            "object_type": "host",
            "name": "syslog_server",
            "zone": "WAN",
            "value": PC2_ETH1_IP,
        }
        rc = ao_api.config_addressobject(**ao_opt)
        Assertion.assert_equal(rc, True, 'ERR: Add syslog server address obj Failed!!')
