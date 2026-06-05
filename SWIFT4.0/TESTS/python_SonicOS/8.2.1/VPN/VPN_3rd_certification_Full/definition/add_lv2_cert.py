from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "add level 2 cert"
    goto_teardown = True

    def test_00_01_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2019:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        rc &= RTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    @repeat_method(3)
    def test_00_02_Add_L2_Cert(self):
        logger.info('-'*10+'Add Level 2 CA cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + l2_cert, name='l2_cert', password='test1234')
        rc &= RCACertObj.import_cert_local(cert_path='@' + l2_cert, name='l2_cert', password='test1234')
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')
