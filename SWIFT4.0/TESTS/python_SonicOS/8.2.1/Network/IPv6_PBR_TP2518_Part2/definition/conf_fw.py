from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        rc &= interfacev4api.config_interface(**x2_static)
        rc &= interfacev6api.config_interface_ipv6(**x0_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x1_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x2_ipv6)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    @repeat_method(5)
    def test_02_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    @repeat_method(3)
    def test_03_add_address_object_and_group(self):
        res1 = addr_obj.config_addressobject(**ipv4_ao1,msg=True)
        res2 = addr_obj.config_addressobject(**ipv4_ao2,msg=True)
        res3 = addr_obj.config_ipv6_addressobject(**ipv6_ao1,msg=True)
        res4 = addr_obj.config_ipv6_addressobject(**ipv6_ao2,msg=True)
        res5 = addr_obj.config_ipv6_addressobject(**ipv6_ao3,msg=True)
        res6 = addrGroup_obj.add_addressgroup(**ipv6_group,msg=True)
        if (res1[0] or "Already exists" in str(res1[1])) and (res2[0] or "Already exists" in str(res2[1])) and \
            (res3[0] or "Already exists" in str(res3[1])) and (res4[0] or "Already exists" in str(res4[1])) and \
            (res5[0] or "Already exists" in str(res5[1])) and (res6[0] or "Already exists" in str(res6[1])):
            rc = True
            logger.info(' add address_object_and_group success')
        else:
            False

        get_rt = route_obj.get_route_policy(version= 'all')
        logger.info(f'-----------{get_rt}')
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
