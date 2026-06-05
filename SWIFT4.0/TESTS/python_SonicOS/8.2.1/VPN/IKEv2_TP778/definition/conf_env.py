from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    # goto_teardown = True

    def test_00_01_Enable_DPD(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Ldpd)
        # rc &= RAdv_obj.config_vpnadvanced(**Rdpd)
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

