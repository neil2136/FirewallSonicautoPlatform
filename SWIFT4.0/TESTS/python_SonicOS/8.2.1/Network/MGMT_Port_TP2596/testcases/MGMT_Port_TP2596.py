from definition.settings import *


class Test_MGMT_Port_TP2596_01(Test):
    uuid = "SOSAIOT-TC-56855"
    description = show_testcase_info(TESTPLAN, '1516165', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516165')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_config_MGMT_interface(self):
        rc = Linterface.config_interface(**MGMT)
        ref1,ref2,ref3 = copy.deepcopy(MGMT),copy.deepcopy(MGMT),copy.deepcopy(MGMT)
        ref1['ip'] = '192.168.1.300'
        ref2['ip'] = '192.168.1.0'
        ref3['ip'] = '192.168.1.255'
        res1 = Linterface.config_interface(msg=True,**ref1)
        res2 = Linterface.config_interface(msg=True,**ref2)
        res3 = Linterface.config_interface(msg=True,**ref3)
        if 'Invalid IP' in str(res1) and 'Invalid IP Address' in str(res2) and 'Invalid IP Address' in str(res3):
            rc &= True
        else:
            rc &= False
        logger.info(f'----{res1}----------{res2}----------{res3}')
        Assertion.assert_equal(rc, True, f"ERR: check error message when config illegal IP failed")


class Test_MGMT_Port_TP2596_02(Test):
    uuid = "SOSAIOT-TC-56856"
    jira = "GEN8-7484"
    description = show_testcase_info(TESTPLAN, '1516170', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516170')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_02_01_login_via_MGMT_interface(self):
        rc = mgmt_fw.api_login()
        mgmt_fw.api_logout()
        Assertion.assert_equal(rc, True, f"ERR: login via mgmt interface failed")


class Test_MGMT_Port_TP2596_03(Test):
    uuid = "SOSAIOT-TC-56857"
    jira = "GEN8-7484"
    description = show_testcase_info(TESTPLAN, '1516176', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516176')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    @repeat_method(3)
    def test_03_01_restart_dut(self):
        rc = restartobj.restart_now()
        Assertion.assert_equal(rc, True, f"ERR: restart dut failed")

    @repeat_method(3)
    def test_03_02_check_ping(self):
        res = PC1.send_command(f'ping {DUT_MGMT} -w 2 ')
        if '100% packet loss' not in str(res) :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: check ping failed")

    def test_03_03_check_ssh_and_http(self):
        rc = mgmt_cli.cli_login()
        mgmt_cli.cli_logout()
        rc &= mgmt_fw.api_login()
        rc &= mgmt_fw.api_logout()
        Assertion.assert_equal(rc, True, f"ERR: check ssh failed")


class Test_MGMT_Port_TP2596_04(Test):
    uuid = "SOSAIOT-TC-56859"
    description = show_testcase_info(TESTPLAN, '1516179', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516179')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_04_01_check_ssh(self):
        rc = mgmt_cli.cli_login()
        mgmt_cli.cli_logout()
        Assertion.assert_equal(rc, True, f"ERR: check ssh failed")


class Test_MGMT_Port_TP2596_05(Test):
    uuid = "SOSAIOT-TC-56858"
    description = show_testcase_info(TESTPLAN, '1516177', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1516177')
        logger.info(Params)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_05_01_config_MGMT_interface(self):
        rc = Linterface.config_interface(**MGMT)
        Assertion.assert_equal(rc, True, f"ERR: config mgmt interface failed")
        
    @repeat_method(3)
    def test_05_02_upload_firmware_via_mgmt(self):
        (rc, rc_log) = setting_obj.import_firmware(log_tag=True, **import_dict)
        logger.info(rc_log)
        Assertion.assert_equal(rc, True, f"ERR: upload firmware via mgmt interface failed")



