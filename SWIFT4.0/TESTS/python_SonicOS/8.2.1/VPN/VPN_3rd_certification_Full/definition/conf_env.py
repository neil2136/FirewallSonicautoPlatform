from definition.settings import *


class TestConfigENV1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_set_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2024:01:01",
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
        Assertion.assert_equal(rc, True, 'set DUT time Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.config_addressobject(**remote_l)
        rc1 &= LAddrOBJ.config_addressobject(**local_Tran_l)
        rc1 &= LAddrOBJ.config_addressobject(**remote_Tran_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.config_addressobject(**remote_r)
        rc2 &= RAddrOBJ.config_addressobject(**local_Tran_r)
        rc2 &= RAddrOBJ.config_addressobject(**remote_Tran_r)
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_03_Add_CA_Cert_for_DUT(self):
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        cmds = ['show certificates status imported']
        (resp, output) = fw_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in dut Failed.')

    def test_00_04_Add_CA_Cert_for_Remote(self):
        rc = RCACertObj.import_ca_cert(file=ca_cert)
        cmds = ['show certificates status imported']
        (resp, output) = rm_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in remote Failed.')

    @repeat_method(3)
    def test_00_05_Add_Local_Cert_for_DUT(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed in DUT.')

    @repeat_method(3)
    def test_00_06_Add_Local_Cert_for_Remote(self):
        rc = RCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed in remote.')

    @repeat_method(3)
    def test_00_07_install_expect(self):
        resp1 = os.popen('yum install -y expect').read()
        logger.info(resp1)
        logger.info("check expect installed")
        resp = os.popen('expect -v').read()
        Assertion.assert_regular(str(resp), 'expect version 5\.45', "ERR: install expect failed")


class TestConfigENV2(Test):
    uuid = 'NonTC'
    description = "add ocsp cert"
    goto_teardown = True

    def test_00_01_set_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2024:01:01",
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
        Assertion.assert_equal(rc, True, 'set DUT time expired Failed.')

    def test_00_02_Add_CA_Cert_for_DUT(self):
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        rc &= LCACertObj.import_ca_cert(file=ocsp_root)
        rc &= LCACertObj.import_ca_cert(file=ocsp_revk_root)
        cmds = ['show certificates status imported']
        (resp, output) = fw_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in dut Failed.')

    def test_00_03_Add_CA_Cert_for_Remote(self):
        rc = RCACertObj.import_ca_cert(file=ca_cert)
        rc &= RCACertObj.import_ca_cert(file=ocsp_root)
        rc &= RCACertObj.import_ca_cert(file=ocsp_revk_root)
        cmds = ['show certificates status imported']
        (resp, output) = rm_cli.do_cli_commands(cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert in remote Failed.')

    @repeat_method(3)
    def test_00_04_Add_Local_Cert_for_DUT(self):
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        rc &= LCACertObj.import_cert_local(cert_path='@' + ocsp_pfx, name='validcert', password='12345678')
        rc &= LCACertObj.import_cert_local(cert_path='@' + ocsp_revk_pfx, name='revokecert', password='12345678')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed in DUT.')

    @repeat_method(3)
    def test_00_05_Add_Local_Cert_for_Remote(self):
        rc = RCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        rc &= RCACertObj.import_cert_local(cert_path='@' + ocsp_pfx, name='validcert', password='12345678')
        rc &= RCACertObj.import_cert_local(cert_path='@' + ocsp_revk_pfx, name='revokecert', password='12345678')
        Assertion.assert_equal(rc, True, 'Add loacl cert Failed in remote.')
