from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    # def test_00_01_set_FW_time(self):
    #     curt_systime = os.popen("date +'%Y-%m-%d %H:%M:%S'").read()
    #     curt_date = curt_systime[0:10].replace('-',':')
    #     curt_time = curt_systime[-9:-1]
    #     logger.info("current system time {}".format(curt_systime))
    #     logger.info("current time {}".format(curt_time))
    #     logger.info("current date {}".format(curt_date))
    #     time_json = {
    #         "time": {
    #             "use_ntp": False,
    #             "time": curt_time,
    #             "date": curt_date,
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
    #     Assertion.assert_equal(rc, True, 'set FW time Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    @repeat_method(3)
    def test_00_03_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        rc &= RCACertObj.import_ca_cert(file=ca_cert)
        (rc1, output1) = fw_cli.do_cli_commands(show_cmds, 1)
        (rc2, output2) = rm_cli.do_cli_commands(show_cmds, 1)
        res = True if rc or ('myCA' in output1 and 'Valid' in output1 and 'myCA' in output2 and 'Valid' in output2) else False
        Assertion.assert_equal(res, True, 'Add CA cert Failed.')

    @repeat_method(3)
    def test_00_04_Add_Local_Cert(self):
        logger.info('-'*10+'Add local cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        # rc &= RCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        rc &= RCACertObj.import_cert_local_with_json(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add  cert Failed.')

