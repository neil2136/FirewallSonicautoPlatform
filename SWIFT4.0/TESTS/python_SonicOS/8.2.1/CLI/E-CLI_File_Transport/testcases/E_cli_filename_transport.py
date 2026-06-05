from definition.init_param import *
import time

class Test_01_FTP(Test):
    uuid = "SOSAIOT-TC-48537"
    description = show_testcase_info(Parameter.TESTPLAN, "1529802", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529803')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_TSR_export_via_FTP(self):
        commands = ["config","export tech-support-report ftp ftp://root:password@192.168.13.200","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

class Test_02_FTP(Test):
    uuid = "SOSAIOT-TC-48538"
    description = show_testcase_info(Parameter.TESTPLAN, "1529803", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529803')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Config_export_via_FTP(self):
        commands = ["config","export current-config cli ftp ftp://root:password@192.168.13.200/currentconf.txt","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

class Test_03_FTP(Test):
    uuid = "SOSAIOT-TC-48539"
    description = show_testcase_info(Parameter.TESTPLAN, "1529804", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529804')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_TSR_export_via_SCP(self):
        commands = ["config","export tech-support-report scp scp://root:password@192.168.13.200/techsupport.wri","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

class Test_04_FTP(Test):
    uuid = "SOSAIOT-TC-48540"
    description = show_testcase_info(Parameter.TESTPLAN, "1529805", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529805')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Current_Config_export_via_SCP(self):
        commands = ["config","export current-config cli scp scp://root:password@192.168.13.200/currentconf.txt","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

class Test_05_FTP(Test):
    uuid = "SOSAIOT-TC-48541"
    description = show_testcase_info(Parameter.TESTPLAN, "1529865", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529806')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    
    def test_01_Current_Config_export_via_SCP(self):
        commands = ["config","export tech-support-report ftp ftp://root:password@192.168.13.200","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

       
class Test_06_FTP(Test):
    uuid = "SOSAIOT-TC-48542"
    
    def test_01_Current_Config_export_via_SCP(self):
        commands = ["config","export tech-support-report scp scp://root:password@192.168.13.200/techsupport.wri","commit"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

    
