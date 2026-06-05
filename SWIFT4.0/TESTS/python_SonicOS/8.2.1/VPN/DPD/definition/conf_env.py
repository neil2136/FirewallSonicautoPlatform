from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_00_Configure_Interface_in_DUT(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUTX2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.DUTX3,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = LintfaceObj.config_interface(**x2_static)
        rc &= LintfaceObj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2&X3 to static failed")

    def test_00_01_Configure_Interface_in_Remote(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTEX2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.REMOTEX3,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = RintfaceObj.config_interface(**x2_static)
        rc &= RintfaceObj.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2&X3 to static failed")

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.config_addressobject(**remote_l)
        rc1 &= LAddrOBJ.config_addressobject(**remote_l_2)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.config_addressobject(**remote_r)
        rc2 &= RAddrOBJ.config_addressobject(**remote_r_2)
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')
