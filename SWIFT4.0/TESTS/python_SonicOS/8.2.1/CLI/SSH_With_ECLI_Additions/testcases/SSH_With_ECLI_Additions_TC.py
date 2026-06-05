from definition.settings import *


class Test_01_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49379"
    description = show_testcase_info(Parameter.TESTPLAN, '1520297', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520297')

    def test_01_generate_new_key(self):
        cmds = ['configure',
                'ssh server',
                'keygen',
                'commit',
                'end', 
                'exit']
        rc1 = fw_cli.do_cli_commands(cmds)
        rc2 = fw_cli.ssh_connect()
        Assertion.assert_equal(rc1&rc2, True, "ERR: generate new key failed")

    def test_02_verify_new_key_changed_after_reboot(self):
        cmds = ['restart']
        rc1 = fw_cli.do_cli_commands(cmds)
        resp = subprocess.getoutput("ssh 192.168.168.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED", str(resp)):
            rc2 = True
        else:
            rc2 = False
        Assertion.assert_equal(rc1&rc2, True, "ERR: verify new key changed after reboot failed")


class Test_02_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49380"
    description = show_testcase_info(Parameter.TESTPLAN, '1520298', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520298')

    def test_01_show_ssh_session_via_console(self):
        global con_svr,con_port
        rc1 = fw_cli.ssh_connect()
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        if re.search('192\.168\.168\.\d+\s*\d+', str(resp)):
            con_svr = re.search('(192.168.168.\d+)\s*(\d+)', str(resp)).group(1)
            con_port = re.search('(192.168.168.\d+)\s*(\d+)', str(resp)).group(2)
            rc2 = True
        else:
            logger.info(resp)
            con_svr = 0
            con_port = 0
            rc2 = False
        Assertion.assert_equal(rc1&rc2, True, "ERR: get ssh session info failed")

    def test_02_check_kill_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                f'kill session ip {con_svr} port {con_port} ',
                ]
        resp = fw_console.do_cli_commands(cmds,1)
        time.sleep(3)
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        if re.search('No entries', str(resp)):
            rc = True
        else:
            logger.info(resp)
            rc = False        
        Assertion.assert_equal(rc, True, "ERR: kill ssh session failed")


class Test_03_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49381"
    description = show_testcase_info(Parameter.TESTPLAN, '1520299', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520299')

    def test_01_connect_4_ssh_session(self):
        rc1 = fw_cli.ssh_connect()
        rc2 = fw_cli2.ssh_connect()
        rc3 = fw_cli3.ssh_connect()
        rc4 = fw_cli4.ssh_connect()
        time.sleep(3)
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        try:
            ses_list = re.findall(r'(192.168.168.\d+)\s*(\d+)', str(resp), re.S)
        except Exception as e:
            print ("Error info: " + str(e))
            ses_list = []
        if len(ses_list) == 4:
            rc = True
        else:
            rc = False      
        Assertion.assert_equal(rc, True, "ERR: get ssh session info failed")

    def test_02_check_kill_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'terminate',
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        time.sleep(3)
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        if re.search('No entries', str(resp)):
            rc2 = True
        else:
            logger.info(resp)
            rc2 = False        
        Assertion.assert_equal(rc1&rc2, True, "ERR: kill ssh server session failed")

    def test_03_reconnect_ssh_session(self):
        resp = subprocess.getoutput("ssh 192.168.168.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("Connection refused", str(resp)):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: verify ssh connection refused failed")


class Test_04_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49382"
    description = show_testcase_info(Parameter.TESTPLAN, '1520300', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520300')

    def test_01_restart_and_connect_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'restart',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        rc2 = fw_cli.ssh_connect()
        Assertion.assert_equal(rc1&rc2, True, "ERR: restart ssh session failed")


class Test_05_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49383"
    description = show_testcase_info(Parameter.TESTPLAN, '1520301', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520301')

    def test_01_modify_ssh_port(self):
        cmds = ['configure',
                'ssh server',
                'port 54022',
                'commit',
                'end', 
                'exit']
        rc = fw_console.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: modify ssh port failed")

    def test_02_connect_ssh_session_via_default_port(self):
        resp = subprocess.getoutput("ssh 192.168.168.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("Connection refused", str(resp)):
            rc = True
        else:
            rc = False 
        Assertion.assert_equal(rc, True, "ERR: verify ssh connection refused failed")

    def test_03_connect_ssh_session_via_new_port(self):
        rc = fw_cli_p.ssh_connect()  
        Assertion.assert_equal(rc, True, "ERR: ssh to dut via new port passed")

    def test_04_recover_ssh_port(self):
        cmds = ['configure',
                'ssh server',
                'port 22',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        rc2 = fw_cli.ssh_connect()  
        Assertion.assert_equal(rc1&rc2, True, "ERR: recover ssh port failed")


class Test_06_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49384"
    description = show_testcase_info(Parameter.TESTPLAN, '1520302', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520302')

    def test_01_connect_4_ssh_session(self):
        rc1 = fw_cli.ssh_connect()
        rc2 = fw_cli2.ssh_connect()
        rc3 = fw_cli3.ssh_connect()
        rc4 = fw_cli4.ssh_connect()
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        logger.info(f"resp info: {resp}")
        try:
            ses_list = re.findall(r'(192.168.168.\d+)\s*(\d+)', str(resp), re.S)
        except Exception as e:
            print ("Error info: " + str(e))
            ses_list = []
        if len(ses_list) == 4:
            rc = True
        else:
            rc = False      
        Assertion.assert_equal(rc, True, "ERR: get ssh session info failed")

    def test_02_check_kill_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'terminate',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        if re.search('No entries', str(resp)):
            rc2 = True
        else:
            logger.info(resp)
            rc2 = False        
        Assertion.assert_equal(rc1&rc2, True, "ERR: kill ssh session failed")

    def test_03_reconnect_ssh_session(self):
        resp = subprocess.getoutput("ssh 192.168.168.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("Connection refused", str(resp)):
            rc = True
        else:
            rc = False 
        Assertion.assert_equal(rc, True, "ERR: verify ssh connection refused failed")

    def test_04_enable_ssh_and_connect_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'enable',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        rc2 = fw_cli.ssh_connect()        
        Assertion.assert_equal(rc1&rc2, True, "ERR: enable ssh connection failed")


class Test_07_SSH_With_ECLI_Additions(Test):
    uuid = "SOSAIOT-TC-49385"
    description = show_testcase_info(Parameter.TESTPLAN, '1520303', description=True)['title']

    def test_00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1520303')

    def test_01_config_x2(self):
        rc = if_api.config_interface(**if_x2_dict)
        Assertion.assert_equal(rc, True, "ERR: config x2 failed.")

    def test_02_connect_4_ssh_session(self):
        rc1 = fw_cli.ssh_connect()
        rc2 = fw_cli2.ssh_connect()
        rc3 = fw_cli_x2.ssh_connect()
        rc4 = fw_cli2_x2.ssh_connect()
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        try:
            ses_list1 = re.findall(r'(192.168.168.\d+)\s*(\d+)', str(resp), re.S)
            ses_list2 = re.findall(r'(12.12.2.\d+)\s*(\d+)', str(resp), re.S)
            ses_list = ses_list1 + ses_list2
        except Exception as e:
            print ("Error info: " + str(e))
            ses_list = []
        if len(ses_list) == 4:
            rc = True
        else:
            rc = False      
        Assertion.assert_equal(rc, True, "ERR: get ssh session info failed")

    def test_03_check_kill_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'terminate',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        resp = fw_console.do_cli_commands(['show ssh server sessions'],1)
        if re.search('No entries', str(resp)):
            rc2 = True
        else:
            logger.info(resp)
            rc2 = False        
        Assertion.assert_equal(rc1&rc2, True, "ERR: terminate ssh session failed")

    def test_04_reconnect_ssh_session(self):
        resp = subprocess.getoutput("ssh 192.168.168.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("Connection refused", str(resp)):
            rc = True
        else:
            rc = False 
        Assertion.assert_equal(rc, True, "ERR: verify ssh connection refused failed")

    def test_05_reconnect_ssh_session(self):
        resp = subprocess.getoutput("ssh 12.12.2.168 -l admin")
        logger.info(f"return info: {resp}")
        if re.search("Connection refused", str(resp)):
            rc = True
        else:
            rc = False 
        Assertion.assert_equal(rc, True, "ERR: verify ssh connection refused failed")

    def test_06_enable_ssh_and_connect_ssh_session(self):
        cmds = ['configure',
                'ssh server',
                'enable',
                'commit',
                'end', 
                'exit']
        rc1 = fw_console.do_cli_commands(cmds)
        rc2 = fw_cli.ssh_connect()        
        rc3 = fw_cli_x2.ssh_connect()        
        Assertion.assert_equal(rc1&rc2&rc3, True, "ERR: enable ssh session failed")

