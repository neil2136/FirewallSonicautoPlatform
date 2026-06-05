from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        rc &= interfacev6api.config_interface_ipv6(**x0_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x1_ipv6)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    def test_02_create_sslvpn_address_object(self):
        rc = address_objects.config_addressobject(**address_object)
        rc &= address_objects.config_ipv6_addressobject(**address_ipv6)
        Assertion.assert_equal(rc, True, "ERR: create sslvpn address object failed")

    def test_03_config_sslserver(self):
        rc = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        rc &= sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(rc, True, "ERR:  config server settings failed")

    def test_04_config_client_settings(self):
        rc = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(rc, True, "ERR: config Client settings pagefailed")

    def test_05_add_sslvpn_user(self):
        rc = user_local.local_user(**add_user)
        rc &= user_local.user_vpn_client_access(**uesr_access1)
        rc &= user_local.user_member_of(**user_member1)
        Assertion.assert_equal(rc, True, "ERR:  add sslvpntest user failed")

    @repeat_method(5)
    def test_06_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
   

  
