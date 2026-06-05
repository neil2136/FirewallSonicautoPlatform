from definition.settings import *
import copy

class TestInitConfigFW(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_x1(self):
        logger.info("config x0 x1 interface... ")
        rc = interface_api.config_interface(**x0_static_dict)
        rc = interface_api.config_interface(**x1_static_dict)
        rc = interface_api.config_interface(**x2_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 X1 X2 to static failed")

    def test_02_ConfigureX0_ipv6(self):
        out = interface_apiv6.config_interface_ipv6_new_json(**x0_opt_ipv6)
        Assertion.assert_equal(out, True, "ERR: Configure X0 failed!")

    def test_03_ConfigureX1_ipv6(self):
        out = interface_apiv6.config_interface_ipv6_new_json(**x1_opt_ipv6)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    def test_04_ConfigureX2_ipv6(self):
        out = interface_apiv6.config_interface_ipv6_new_json(**x2_opt_ipv6)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    @repeat_method(3)
    def test_05_register_fw(self):
        time.sleep(10)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_06_add_address_object(self):
        rc = ao_api.config_addressobject(**wan_ao_dict)
        # rc &= ao_api.config_addressobject(**sslvpn_ao_dict)
        rc &= ao_api.config_addressobject(**syslog_ao_dict)

        # rc &= ao_api.config_addressobject(**vpn_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Add address objects failed")

    def test_07_add_syslog_server(self):
        ret = syslog_api.add_syslog_server_custom(**syslog_param)
        Assertion.assert_equal(ret, True, "ERR: add syslog server failed")

    def test_08_set_audit_log_level(self):
        rc = logsetting_api.edit_event(event_id='1382', **audit_setting_dict1)
        rc &= logsetting_api.edit_event(event_id='1383', **audit_setting_dict2)
        Assertion.assert_equal(rc, True, "ERR: set log level failed")

    def test_09_enable_snmp(self):
        rc = snmp_api.enable_snmp()
        Assertion.assert_equal(rc, True, 'ERR: Enable snmp failed!')

    def test_10_config_snmp(self):
        rc = snmp_api.configure_snmp(**snmp_dict)
        Assertion.assert_equal(rc, True, 'ERR: Configure SNMPv3 failed!')

    def test_11_enable_debug_log_for_app_control_filename(self):
        application_control_detection_copy = copy.deepcopy(application_control_detection)
        application_control_detection_copy['log']['event'][0]['priority_level'] = 'inform'

        resp = logsetting_api.enable_event(**application_control_detection_copy)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        application_control_prevention_copy = copy.deepcopy(application_control_prevention)
        application_control_prevention_copy['log']['event'][0]['priority_level'] = 'inform'

        resp = logsetting_api.enable_event(**application_control_prevention_copy)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        resp = logsetting_api.enable_event(**filename_logging_log_http)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_12_set_logging_level(self):
        default_global_cate = {
            "log": {
                "categories": {
                "logging_level": "debug",
                "alert_level": "alert"
                }
            }
            }
        rc = log_cat_api.config_global_categories(**default_global_cate)
        Assertion.assert_equal(rc , True , "ERR: config global categories failed")

