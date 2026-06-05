from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "10:00:39",
                "date": "2022:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

