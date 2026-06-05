from settings import *


class TestInitConfigFW(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_x1(self):
        logger.info("config x1 x2 interface... ")
        rc = interface_api.config_interface(**x1_static_dict)
        rc &= interface_api.config_interface(**x2_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 X2 to static failed")

    @repeat_method(3)
    def test_02_register_fw(self):
        time.sleep(10)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_address_object(self):
        rc = ao_api.config_addressobject(**lan_ao_dict)
        rc &= ao_api.config_addressobject(**sslvpn_ao_dict)
        rc &= ao_api.config_addressobject(**syslog_ao_dict)
        rc &= ao_api.config_addressobject(**vpn_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Add address objects failed")

    def test_04_add_syslog_server(self):
        ret = syslog_api.add_syslog_server(**syslog_param)
        Assertion.assert_equal(ret, True, "ERR: add syslog server failed")

    def test_05_set_audit_log_level(self):
        rc = logsetting_api.edit_event(event_id='1382', **audit_setting_dict1)
        rc &= logsetting_api.edit_event(event_id='1383', **audit_setting_dict2)
        Assertion.assert_equal(rc, True, "ERR: set log level failed")

    def test_07_enable_snmp(self):
        rc = snmp_api.enable_snmp()
        Assertion.assert_equal(rc, True, 'ERR: Enable snmp failed!')

    def test_08_config_snmp(self):
        rc = snmp_api.configure_snmp(**snmp_dict)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')
