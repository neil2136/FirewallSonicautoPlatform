from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        rc &= interfacev4api.config_interface(**MGMT)
        rc &= interfacev6api.config_interface_ipv6(**x0_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x1_ipv6)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    @repeat_method(5)
    def test_02_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


    
   

  
