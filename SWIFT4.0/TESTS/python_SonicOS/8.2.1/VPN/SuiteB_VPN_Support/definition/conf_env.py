from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    # def test_00_01_set_FW_time(self):
    #     time_json = {
    #         "time": {
    #             "use_ntp": False,
    #             "time": "00:00:00",
    #             "date": "2024:01:01",
    #             "time_zone": "pacific-time",
    #             "daylight_savings": True,
    #             "universal": False,
    #             "international_format": False,
    #             "only_custom_ntp": False,
    #             "ntp_update_interval": 60
    #         }
    #     }
    #     rc = LTimeObj.set_time(**time_json)
    #     rc &= RTimeObj.set_time(**time_json)
    #     Assertion.assert_equal(rc, True, 'conf system time Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_03_Add_CA_Cert_for_DUT(self):
        logger.info('-'*10+'Add CA_ECDSA_OSCP cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        cmds = ['show certificates status imported']
        (resp, output) = fw_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in dut Failed.')

    def test_00_04_Add_CA_Cert_for_Remote(self):
        logger.info('-'*10+'Add CA_ECDSA_OSCP cert'+'-'*10)
        rc = RCACertObj.import_ca_cert(file=ca_cert)
        cmds = ['show certificates status imported']
        (resp, output) = rm_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in remote Failed.')

    @repeat_method(3)
    def test_00_05_Add_Local_Cert(self):
        logger.info('-'*10+'Add local cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        # rc &= RCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        rc &= RCACertObj.import_cert_local_with_json(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed.')
