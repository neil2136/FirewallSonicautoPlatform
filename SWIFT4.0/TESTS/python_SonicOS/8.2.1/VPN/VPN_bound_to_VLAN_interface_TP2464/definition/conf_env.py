from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_config_interface(self):
        rc = interfacev4api.config_interface(**Lx2)
        rc &= Rinterfacev4api.config_interface(**Rx2)
        rc &= Rinterfacev4api.config_interface(**Rx3)
        res1= interfacev4api.add_interface(msg = True,**Lv3)
        res2= Rinterfacev4api.add_interface(msg=True,**Rv2)
        if (res1[0] or 'Already exists' in str(res1[1]))  and (res2[0] or 'Already exists' in str(res2[1])) :
            rc &= True
            logger.info("add vlan interface success.")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    


    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')