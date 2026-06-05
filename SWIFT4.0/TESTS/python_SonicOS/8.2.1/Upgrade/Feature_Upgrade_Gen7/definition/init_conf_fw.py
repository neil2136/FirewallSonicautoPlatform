from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(30)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_configure_dpissl_client(self):
        client_dict = {
            'enable': True,
            'application_firewall': False,
            'intrusion_prevention': True,
            'gateway_anti_virus': True,
            'gateway_anti_spyware': True,
            'content_filter': True,
            'auth_server_for_decrypted_connections': False,
            'deployment_server_domains': False,
            'bypass_decryption': True,
            'audit_built_in_exclusion': False,
            'authenticate_server': False,
            'open_failed_connections': True,
        }
        output = clientsslapi.config_general_settings(**client_dict)
        Assertion.assert_equal(output, True, "ERR: configure dpissl client failed")


