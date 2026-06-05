from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_Configure_Interface(self):
        x2_static = {
            'if'     : 'X2',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.DUTX2,
            'mask'   : '255.255.255.0',
            'gateway': Parameter.SECGWWAN,
            'dns1'   : Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
            'fragment_packets': True,
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_02_set_FW_time(self):
        curt_systime = os.popen("date +'%Y-%m-%d %H:%M:%S'").read()
        curt_date = curt_systime[0:10].replace('-',':')
        curt_time = curt_systime[-9:-1]
        logger.info("current system time {}".format(curt_systime))
        logger.info("current time {}".format(curt_time))
        logger.info("current date {}".format(curt_date))
        time_json = {
            "time": {
                "use_ntp": False,
                "time": curt_time,
                "date": curt_date,
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
        Assertion.assert_equal(rc, True, 'set FW time Failed.')

    def test_00_03_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add local AddObj for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**local_l)
        logger.info('-'*10+'Add remote AddObj for  DUT'+'-'*10)
        rc &= LAddrOBJ.config_addressobject(**local_r)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    def test_00_04_Add_Remote_DUT_AddObj(self):
        logger.info('-'*10+'Add local AddObj for Remote DUT'+'-'*10)
        rc = RAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add remote AddObj for Remote DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for Remote DUT Failed.')

    @repeat_method(3)
    def test_00_05_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        rc &= RCACertObj.import_ca_cert(file=ca_cert)
        (rc1, output1) = fw_cli.do_cli_commands(show_cmds, 1)
        (rc2, output2) = rm_cli.do_cli_commands(show_cmds, 1)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')
    
    # @repeat_method(3)
    # def test_00_06_Add_Local_Cert_for_FW(self):
    #     logger.info('-'*10+'generate signing request'+'-'*10)
    #     rc = LCACertObj.generate_req(**signreq)
    #     rc &= LCACertObj.export_req(filename='my_cert', filepath='/tmp/logs/my_cert.p10')
    #     rc &= Gen_Local_Cert.gen_local_cert(sign_req='my_cert', sub=False)
    #     rc &= LCACertObj.import_req_cert(req_cert='my_cert', signed_cert='/tmp/logs/01.pem')
    #     (rc1, output) = fw_cli.do_cli_commands(show_cmds, 1)
    #     logger.info(f'show cert: {output}')
    #     if 'Local certificate' in output and 'Yes' in output:
    #         rc1 &= True
    #     else:
    #         rc1 &= False
    #     Assertion.assert_equal(rc1, True, 'add local cert Failed.')
    
    # @repeat_method(3)
    # def test_00_07_Add_Local_Cert_for_Remote(self):
    #     logger.info('-'*10+'generate signing request'+'-'*10)
    #     rc = RCACertObj.generate_req(**signreq)
    #     rc &= RCACertObj.export_req(filename='my_cert', filepath='/tmp/logs/my_cert.p10')
    #     rc &= Gen_Local_Cert.gen_local_cert(sign_req='my_cert', sub=False)
    #     rc &= RCACertObj.import_req_cert(req_cert='my_cert', signed_cert='/tmp/logs/01.pem')
    #     logger.info('-'*10+'generate signing request rc is {}'.format(rc))
    #     (rc1, output) = rm_cli.do_cli_commands(show_cmds, 1)
    #     logger.info(f'show cert: {output}')
    #     if 'Local certificate' in output and 'Yes' in output:
    #         rc1 &= True
    #     else:
    #         rc1 &= False
    #     Assertion.assert_equal(rc1, True, 'add remote cert Failed.')
        
    @repeat_method(3)
    def test_00_06_Add_Local_Cert(self):
        logger.info('-'*10+'Add local cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        rc &= RCACertObj.import_cert_local_with_json(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add  cert Failed.')


    