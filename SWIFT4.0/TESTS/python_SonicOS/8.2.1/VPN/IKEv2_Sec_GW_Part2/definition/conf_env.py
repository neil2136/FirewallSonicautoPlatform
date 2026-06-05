from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_Conf_Local_DPD(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Ldpd)
        rc &= RAdv_obj.config_vpnadvanced(**Rdpd)
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_03_Config_Log_Settings_in_rm(self):
        logger.info('-'*10+'Enable all VPN log'+'-'*10)
        rc = Rlog_set.enable_all_log_category()
        rc &= Rlog_set.logging_level(level='debug')
        logger.info('-' * 10 + 'Set the level of LOG as Debug' + '-' * 10)
        Assertion.assert_equal(rc, True, "ERR: set rm log level failed")

