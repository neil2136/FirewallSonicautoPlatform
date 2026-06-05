from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_Add_AddObj(self):
        logger.info('-'*10+'Add remote AddObj for DUT and Remote DUT'+'-'*10)
        logger.info('-'*10+'Add remote AddObj for DUT '+'-'*10)
        rc = LAddrOBJ.config_addressobject(**local_r)
        logger.info('-'*10+'Add remote AddObj for Remote DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    def test_00_02_config_interface(self):
        logger.info('config  interface.....')
        rc = Linterface.config_interface(**Lx1)
        rc &= Linterface.config_interface(**Lx0)
        rc &= Rinterface.config_interface(**Rx1)
        rc &= Rinterface.config_interface(**Rx0)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(5)
    def test_00_03_register_fw(self):
        self.goto_teardown=True
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

