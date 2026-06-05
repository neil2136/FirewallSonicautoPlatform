from definition.init_param import *


class Test_01_WireMode_2580_tc_1511478(Test):
    uuid = "SOSAIOT-TC-57484"
    description= show_testcase_info(Parameter.TESTPLAN, '1511478', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511478')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_normal(self):
        logger.info('config interface x2 normal...')
        interfaceObj.unassign_interface(interface = 'X2')
        interfaceObj.unassign_interface(interface = 'X3')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            
        }
        rc = interfaceObj.config_interface(**x2)
        
        cmd = 'ping -c 5 {}'.format(Parameter.X2_IP)
        logger.info('from pc3 ping interface x2 IP:{}'.format(cmd))
        output = pc3_ssh.send_command(cmd)
        if re.search(r".*100% packet loss.*", str(output), re.S|re.I|re.M) == None:
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: Config X2 interface failed")

    def test_02_config_interface_x2_wiremode(self):
        logger.info('config interface x2 to wiremode bypass...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        cmd = 'ping -c 5 {}'.format(Parameter.X2_IP)
        logger.info('from pc3 ping interface x2 IP:{}'.format(cmd))
        output = pc3_ssh.send_command(cmd)
        if re.search(r".*100% packet loss.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR:config interface x2 wire-mode bypass failed")


class Test_02_WireMode_2580_tc_1511479(Test):
    uuid = "SOSAIOT-TC-57485"
    description= show_testcase_info(Parameter.TESTPLAN, '1511479', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511479')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 to wiremode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")

    def test_02_from_pc3_ping_pc4(self):
        logger.info('from pc3 ping pc4...')
        flag = False
        cmd = 'ping -c 5 {}'.format(Parameter.PC4_ETH0)
        logger.info('from pc3 ping pc4 eth0:{}'.format(cmd))
        output = pc3_ssh.send_command(cmd)
        if not re.search(r".*100% packet loss.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:from pc3 ping pc4 failed")


class Test_03_WireMode_2580_tc_1511450(Test):
    # duplicate case with Wiremode_Consolidated
    # uuid = '1511450'
    uuid = "SOSAIOT-TC-57456"
    description= show_testcase_info(Parameter.TESTPLAN, '1511450', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511450')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_interface_x2_bypass(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_02_reboot_dut(self):
        logger.info('reboot DUT and check dpissl server....')
        logger.info('reboot fw.....')
        rc = settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, "ERR: reboot fw failed")

    def test_03_check_interface_x2_bypass(self):
        logger.info('check interface x2....')
        flag = False
        output = interfaceObj.get_interface_status('X2')
        if re.search(r"zone.*LAN.*mode.*wire_mode.*type.*bypass", str(output), re.S|re.I) != None:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 bypass failed")

    def test_04_config_interface_x2_secure(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_05_reboot_dut(self):
        logger.info('reboot DUT and check dpissl server....')
        logger.info('reboot fw.....')
        rc = settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, "ERR: reboot fw failed")

    def test_06_check_interface_x2_secure(self):
        logger.info('check interface x2....')
        flag = False
        output = interfaceObj.get_interface_status('X2')
        if re.search(r"zone.*LAN.*mode.*wire_mode.*type.*secure", str(output), re.S|re.I) != None:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 secure failed")

    def test_07_config_interface_x2_inspect(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_05_reboot_dut(self):
        logger.info('reboot DUT and check dpissl server....')
        logger.info('reboot fw.....')
        rc = settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, "ERR: reboot fw failed")

    def test_06_check_interface_x2_inspect(self):
        logger.info('check interface x2....')
        flag = False
        output = interfaceObj.get_interface_status('X2')
        if re.search(r"zone.*LAN.*mode.*wire_mode.*type.*inspect", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 inspect failed")


class Test_04_WireMode_2580_tc_1511456(Test):
    uuid = "SOSAIOT-TC-57462"
    description= show_testcase_info(Parameter.TESTPLAN, '1511456', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511456')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_bypass(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_02_enable_app_rule(self):
        logger.info('enable app rule...')
        apprule_setting_dict = {
            "enable": True,
            "log_redundancy":{}
        }
        rc = appObj.config_apprule_setting(**apprule_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: enable app rule failed")

    def test_03_traffic_from_pc3_to_pc4(self):
        logger.info('send traffic from interface pc3 to interface pc4....')
        flag = False
        cmd = 'touch /home/test_bypass.txt'
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        logger.info('traffic from pc3 to pc4...')
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '/home/test_bypass.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc4 = 'ls -l /home'
        logger.info('run cmd in pc4:{}'.format(cmd_pc4))
        output = pc4_ssh.send_command(cmd_pc4)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r".*test_bypass.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: send traffic from pc3 to pc4 failed")


class Test_05_WireMode_2580_tc_1511457(Test):
    uuid = "SOSAIOT-TC-57463"
    description= show_testcase_info(Parameter.TESTPLAN, '1511457', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511457')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_inspect(self):
        logger.info('config interface x2 wire-mode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    @repeat_method(3)
    def test_02_traffic_from_pc3_to_pc4(self):
        logger.info('send traffic from interface pc3 to interface pc4....')
        flag = False
        sleep(10)
        cmd = 'touch /home/test_inspect.txt'
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        logger.info('traffic from pc3 to pc4...')
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '/home/test_inspect.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc4 = 'ls -l /home'
        logger.info('run cmd in pc4:{}'.format(cmd_pc4))
        output = pc4_ssh.send_command(cmd_pc4)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r".*test_inspect.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: send traffic from pc3 to pc4 failed")


class Test_06_WireMode_2580_tc_1511459(Test):
    uuid = "SOSAIOT-TC-57465"
    description= show_testcase_info(Parameter.TESTPLAN, '1511459', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511459')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_secure(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")

    @repeat_method(3)
    def test_02_traffic_from_pc3_to_pc4(self):
        logger.info('send traffic from interface pc3 to interface pc4....')
        flag = False
        cmd = 'touch /home/test_secure.txt'
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        logger.info('traffic from pc3 to pc4...')
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '/home/test_secure.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc4 = 'ls -l /home'
        logger.info('run cmd in pc4:{}'.format(cmd_pc4))
        output = pc4_ssh.send_command(cmd_pc4)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r".*test_secure.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: send traffic from pc3 to pc4 failed")


class Test_07_WireMode_2580_tc_1511461(Test):
    uuid = "SOSAIOT-TC-57467"
    description= show_testcase_info(Parameter.TESTPLAN, '1511461', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511461')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_bypass(self):
        logger.info('config interface x2 wire-mode bypass...')
        
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_02_add_match_object(self):
        logger.info('add match object and app rule...')
        match_opt = {
            'name':'tc_32',
            'object_type':'file-extension',
            'match_type':'exact',
            'input_representation':'alphanumeric',
             "negative_matching": False,
            'content_entry': [{"content_entry":"txt"}],
        }

        rc = matchObj.config_matchobject(**match_opt)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_03_app_rule(self):
        apprule_dict = {
            "app_rules":{
                "policy":[
                    {"action_object":"Reset/Drop",
                    "connection_side":"client",
                    "destination":{
                        "service": {
                            "name": "FTP Control"
                        },
                        "address": {
                            "any": True
                        }
                    },
                    "direction":{"basic":"both"},
                    "enable":True,
                    "exclusion":{"address":{}},
                    "flow_reporting":False,
                    "log":{"individual":False,
                    "redundancy":{"global":True}},
                    "logging":True,
                    "match_object":{
                        "object": "tc_32",
                        
                        },
                    "name":"tc_32",
                    "schedule":{"always_on":True},
                    "source": {
                        "service": {
                            "any": True
                        },
                        "address": {
                            "any": True
                        }
                    },
                    "type":{"ftp": "client-download"},
                    "users":{"excluded":{},"included":{"all":True}}
                    }
                ]
            }
        }
        
        rc = appObj.add_apprule(**apprule_dict)
        Assertion.assert_equal(rc, True, "ERR: add match object and app rule failed")

    @repeat_method(3)
    def test_04_download_file_usr_ftp(self):
        logger.info('download file from pc4 use ftp...')
        sleep(60)
        cmd = "echo 'aaaaa' > /home/ftp_tc32.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc32.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc32.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc32.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_08_WireMode_2580_tc_1511462(Test):
    uuid = "SOSAIOT-TC-57468"
    description= show_testcase_info(Parameter.TESTPLAN, '1511462', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511462')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_inspect(self):
        logger.info('config interface x2 wire-mode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    def test_04_download_file_usr_ftp(self):
        logger.info('download file from pc4 use ftp...')
        sleep(60)
        cmd = "echo 'aaaaa' >  /home/ftp_tc33.txt"
        flag = False
        logger.info('create a new file ftp_tc33.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc33.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc33.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc33.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_09_WireMode_2580_tc_1511463(Test):
    uuid = "SOSAIOT-TC-57469"
    description= show_testcase_info(Parameter.TESTPLAN, '1511463', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511463')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_secure(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")

    @repeat_method(3)
    def test_04_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' > /home/ftp_tc34.txt"
        flag = False
        logger.info('create a new file ftp_tc34.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc34.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc34.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc34.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_10_WireMode_2580_tc_1511490(Test):
    uuid = "SOSAIOT-TC-57496"
    description= show_testcase_info(Parameter.TESTPLAN, '1511490', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511490')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_inspect(self):
        logger.info('config interface x2 wire-mode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    @repeat_method(3)
    def test_04_download_file_usr_ftp(self):
        logger.info('download file from pc4 use ftp...')
        sleep(60)
        cmd = "echo 'aaaaa' > /home/ftp_tc69.txt"
        flag = False
        logger.info('create a new file ftp_tc69.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc69.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc69.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc69.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_11_WireMode_2580_tc_1511465(Test):
    uuid = "SOSAIOT-TC-57471"
    description= show_testcase_info(Parameter.TESTPLAN, '1511465', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511465')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_bypass(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_02_enable_gav_in_security_service(self):
        logger.info('enable gav in security service...')
        gav_params = {
            'enable_GAV':True,
        }
        rc = gavObj.config_gav(**gav_params)
        Assertion.assert_equal(rc, True, "ERR: config gav in security services failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        pc3_ssh.send_command('mkdir {}'.format(Parameter.TMP_PATH))
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '{}/klez.h.bin'.format(Parameter.TMP_PATH) +' root ' + Parameter.PC4_ETH0 + \
             ' {}/klez.h.bin'.format(Parameter.TMP_PATH)  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l {}'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and not \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_12_WireMode_2580_tc_1511466(Test):
    uuid = "SOSAIOT-TC-57472"
    description= show_testcase_info(Parameter.TESTPLAN, '1511466', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511466')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_inspect(self):
        logger.info('config interface x2 wire-mode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    @repeat_method(3)
    def test_02_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(20)
        pc3_ssh.send_command('rm -rf {}/klez.h.bin'.format(Parameter.TMP_PATH))
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '{}/klez.h.bin'.format(Parameter.TMP_PATH) +' root ' + Parameter.PC4_ETH0 + \
             ' {}/klez.h.bin'.format(Parameter.TMP_PATH)  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l {}'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_13_WireMode_2580_tc_1511467(Test):
    uuid = "SOSAIOT-TC-57473"
    description= show_testcase_info(Parameter.TESTPLAN, '1511467', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511467')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_secure(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")


    @repeat_method(3)
    def test_02_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        pc3_ssh.send_command('mkdir {}'.format(Parameter.TMP_PATH))
        flag = False
        cmd = 'rm -rf {}/klez.h.bin'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l {}'.format(Parameter.TMP_PATH))
        logger.info(output)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '{}/klez.h.bin'.format(Parameter.TMP_PATH) +' root ' + Parameter.PC4_ETH0 + \
             ' {}/1.cab.bin'.format(Parameter.TMP_PATH)  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l {}'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_14_WireMode_2580_tc_1511474(Test):
    uuid = "SOSAIOT-TC-57480"
    description= show_testcase_info(Parameter.TESTPLAN, '1511474', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511474')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_from_pc3_ping_pc4_and_capture_packets(self):
        logger.info('from pc3 ping pc4 and capture packets...')
        flag = False
        logger.info('start capture....')
        captureObj.clear_packets()
        captureObj.start_capture()
        cmd = 'ping -c 3 {}'.format(Parameter.PC4_ETH0)
        pc3_ssh.send_command(cmd)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r".*172.16.4.104.*172.16.3.103.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from pc3 ping pc4 and capture packets failed")


class Test_15_WireMode_2580_tc_1511489(Test):
    uuid = "SOSAIOT-TC-57495"
    description= show_testcase_info(Parameter.TESTPLAN, '1511489', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511489')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    def test_02_enable_app_rule(self):
        logger.info('enable app rule...')
        apprule_setting_dict = {
            "enable": True,
            "log_redundancy":{}
        }
        rc = appObj.config_apprule_setting(**apprule_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: enable app rule failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(60)
        pc3_ssh.send_command('mkdir {}'.format(Parameter.TMP_PATH))
        flag = False
        cmd = 'rm -rf {}/klez.h.bin'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l {}'.format(Parameter.TMP_PATH))
        logger.info(output)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download sftp ') + '{}/klez.h.bin'.format(Parameter.TMP_PATH) +' root ' + Parameter.PC4_ETH0 + \
             ' {}/klez.h.bin'.format(Parameter.TMP_PATH)  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l {}'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and not \
            re.search(r"Gateway Anti-Virus Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_16_WireMode_2580_tc_1511442(Test):
    uuid = "SOSAIOT-TC-57448"
    description= show_testcase_info(Parameter.TESTPLAN, '1511442', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511442')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unassign_x2_x3_and_check_mac_address(self):
        logger.info('unassign x2 x3 and check mac address...')
        global mac_x2
        global mac_x3
        interfaceObj.unassign_interface(interface = 'X2')
        interfaceObj.unassign_interface(interface = 'X3')
        mac_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        mac_x3 = interfaceObj.get_interface_mac(interface = 'X3')
    
        logger.info(mac_x2)
        logger.info(mac_x3)
        Assertion.assert_equal(True, True, "ERR: unassign x2 x3 and check mac address failed")

    def test_02_config_interface_x2_wiremode_bypass(self):
        logger.info('config interface x2 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_03_check_interface_x2_x3_status(self):
        logger.info('check interface x2 x3 status...')
        flag = False
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        type_x3 = output_x3['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        logger.info(type_x2)
        logger.info(type_x3)
        if type_x2 == 'bypass' and type_x3 == 'bypass':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 x3 status failed")

    def test_04_check_mac_address_not_overridden(self):
        logger.info('check mac address not overridden...')
        flag = False
        output_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        output_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(output_x2)
        logger.info(output_x3)
        logger.info(mac_x2)
        logger.info(mac_x3)
        if str(output_x2) == str(mac_x2) and str(output_x3) == str(mac_x3):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check mac address not overridden failed")

            
class Test_17_WireMode_2580_tc_1511448(Test):
    uuid = "SOSAIOT-TC-57454"
    description= show_testcase_info(Parameter.TESTPLAN, '1511448', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511448')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_pref(self):
        logger.info('export pref...')
        rc = settingObj.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: export pref config failed")

    def test_02_import_pref_and_check_x2_x3_status(self):
        logger.info('import pref and check x2 x3 status...')
        flag = False
        settingObj.import_setting_exp(filepath='/tmp/test.exp')
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        type_x3 = output_x3['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        logger.info(type_x2)
        logger.info(type_x3)
        if type_x2 == 'bypass' and type_x3 == 'bypass':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: import pref and check x2 x3 status failed")


class Test_18_WireMode_2580_tc_1511449(Test):
    uuid = "SOSAIOT-TC-57455"
    description= show_testcase_info(Parameter.TESTPLAN, '1511449', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511449')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unassign_x2_x3_and_check_mac_address(self):
        logger.info('unassign x2 x3 and check mac address...')
        global mac_x2
        global mac_x3
        interfaceObj.unassign_interface(interface = 'X2')
        interfaceObj.unassign_interface(interface = 'X3')
        mac_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        mac_x3 = interfaceObj.get_interface_mac(interface = 'X3')
    
        logger.info(mac_x2)
        logger.info(mac_x3)
        Assertion.assert_equal(True, True, "ERR: unassign x2 x3 and check mac address failed")

    def test_02_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    def test_03_check_interface_x2_x3_status(self):
        logger.info('check interface x2 x3 status...')
        flag = False
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        type_x3 = output_x3['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        logger.info(type_x2)
        logger.info(type_x3)
        if type_x2 == 'inspect' and type_x3 == 'inspect':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 x3 status failed")

    def test_04_check_mac_address_not_overridden(self):
        logger.info('check mac address not overridden...')
        flag = False
        output_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        output_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(output_x2)
        logger.info(output_x3)
        logger.info(mac_x2)
        logger.info(mac_x3)
        if str(output_x2) == str(mac_x2) and str(output_x3) == str(mac_x3):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check mac address not overridden failed")


class Test_19_WireMode_2580_tc_1511451(Test):
    uuid = "SOSAIOT-TC-57457"
    description= show_testcase_info(Parameter.TESTPLAN, '1511451', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511451')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_bypass(self):
        logger.info('config interface x2 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    @repeat_method(3)
    def test_02_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' > /home/ftp_1511451.txt"
        flag = False
        logger.info('create a new file ftp_1511451.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath +'/upload_or_download_file.py download ftp ') + '/home/ftp_1511451.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511451.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511451.txt", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_20_WireMode_2580_tc_1511452(Test):
    uuid = "SOSAIOT-TC-57458"
    description= show_testcase_info(Parameter.TESTPLAN, '1511452', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511452')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    @repeat_method(3)
    def test_02_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' > /home/ftp_1511452.txt"
        flag = False
        logger.info('create a new file ftp_1511452.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_1511452.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511452.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511452.txt", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_21_WireMode_2580_tc_1511453(Test):
    uuid = "SOSAIOT-TC-57459"
    description= show_testcase_info(Parameter.TESTPLAN, '1511453', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511453')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_secure(self):
        logger.info('config interface x2 to wiremode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")

    def test_02_disable_app_rule(self):
        logger.info('disable app rule')
        apprule_setting_dict = {
            "enable": False,
            "log_redundancy":{}
        }
        rc = appObj.config_apprule_setting(**apprule_setting_dict)
        Assertion.assert_equal(rc, True, "ERR: enable app rule failed")

    @repeat_method(3)
    def test_03_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' >  /home/ftp_1511453.txt"
        flag = False
        logger.info('create a new file ftp_1511453.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        captureObj.clear_packets()
        captureObj.start_capture()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_1511453.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511453.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        captureObj.stop_capture()
        output2 = captureObj.export_captured_packets()
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511453.txt", str(output), re.S|re.I) and \
            re.search(r"Src=\[172\.16\.3\.103\],\s*Dst=\[172\.16\.4\.104\]", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_22_WireMode_2580_tc_1511455(Test):
    uuid = "SOSAIOT-TC-57461"
    description= show_testcase_info(Parameter.TESTPLAN, '1511455', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511455')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_bypass(self):
        logger.info('config interface x2 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    @repeat_method(3)
    def test_02_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' >  /home/ftp_1511455_bypass.txt"
        flag = False
        logger.info('create a new file ftp_1511455_bypass.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_1511455_bypass.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511455_bypass.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511455_bypass.txt", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    def test_03_change_x2_wiremode_bypass_to_inspect(self):
        logger.info('change x2 wiremode bypass to inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change x2 wiremode bypass to inspect failed")

    @repeat_method(3)
    def test_04_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' > /home/ftp_1511455_inspect.txt"
        flag = False
        logger.info('create a new file ftp_1511455_inspect.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_1511455_inspect.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511455_inspect.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511455_inspect.txt", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    def test_05_change_x2_wiremode_bypass_to_secure(self):
        logger.info('change x2 wiremode bypass to secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change x2 wiremode bypass to secure failed")

    @repeat_method(3)
    def test_06_download_file_use_ftp(self):
        logger.info('download file from pc4 use ftp...')
        cmd = "echo 'aaaaa' > /home/ftp_1511455_secure.txt"
        flag = False
        logger.info('create a new file ftp_1511455_secure.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l /home')
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_1511455_secure.txt'+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_1511455_secure.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_1511455_secure.txt", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")


class Test_23_WireMode_2580_tc_1511458(Test):
    uuid = "SOSAIOT-TC-57464"
    description= show_testcase_info(Parameter.TESTPLAN, '1511458', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511458')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unassign_x2_x3_and_check_mac_address(self):
        logger.info('unassign x2 x3 and check mac address...')
        global mac_x2
        global mac_x3
        interfaceObj.unassign_interface(interface = 'X2')
        interfaceObj.unassign_interface(interface = 'X3')
        mac_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        mac_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(mac_x2)
        logger.info(mac_x3)
        Assertion.assert_equal(True, True, "ERR: unassign x2 x3 and check mac address failed")

    def test_02_config_interface_x2_wiremode_secure(self):
        logger.info('config interface x2 to wiremode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode secure failed")

    def test_03_check_interface_x2_x3_status(self):
        logger.info('check interface x2 x3 status...')
        flag = False
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        type_x3 = output_x3['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        logger.info(type_x2)
        logger.info(type_x3)
        if type_x2 == 'secure' and type_x3 == 'secure':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 x3 status failed")

    def test_04_check_mac_address_not_overridden(self):
        logger.info('check mac address not overridden...')
        flag = False
        output_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        output_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(output_x2)
        logger.info(output_x3)
        logger.info(mac_x2)
        logger.info(mac_x3)
        if str(output_x2) == str(mac_x2) and str(output_x3) == str(mac_x3):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check mac address not overridden failed")


class Test_24_WireMode_2580_tc_1511472(Test):
    uuid = "SOSAIOT-TC-57478"
    description= show_testcase_info(Parameter.TESTPLAN, '1511472', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511472')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_bypass(self):
        logger.info('config interface x2 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")
   
    def test_02_capture_packets_and_check(self):
        logger.info('capture packets and check...')
        flag = False
        logger.info('start capture....')
        captureObj.clear_packets()
        captureObj.start_capture()
        cmd = 'ping -c 10 {}'.format(Parameter.PC4_ETH0)
        pc3_ssh.send_command(cmd)
        sleep(5)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if not re.search(r".*172.16.4.104.*172.16.3.103.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from pc3 ping pc4 and capture packets failed")


class Test_25_WireMode_2580_tc_1511473(Test):
    uuid = "SOSAIOT-TC-57479"
    description= show_testcase_info(Parameter.TESTPLAN, '1511473', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511473')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")
   
    def test_02_capture_packets_and_check(self):
        logger.info('capture packets and check...')
        flag = False
        logger.info('start capture....')
        captureObj.clear_packets()
        captureObj.start_capture()
        cmd = 'ping -c 10 {}'.format(Parameter.PC4_ETH0)
        pc3_ssh.send_command(cmd)
        sleep(5)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r".*172.16.4.104.*172.16.3.103.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from pc3 ping pc4 and capture packets failed")


class Test_26_WireMode_2580_tc_1511476(Test):
    uuid = "SOSAIOT-TC-57482"
    description= show_testcase_info(Parameter.TESTPLAN, '1511476', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511476')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_and_x3(self):
        logger.info('config interface x2 and x3...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            
        }
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            
        }
        rc = interfaceObj.config_interface(**x2)
        rc &= interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 and x3 failed")


class Test_27_WireMode_2580_tc_1511482(Test):
    uuid = "SOSAIOT-TC-57488"
    description= show_testcase_info(Parameter.TESTPLAN, '1511482', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511482')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        interfaceObj.unassign_interface(interface = 'X3')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    def test_02_unassign_interface_x2_and_check(self):
        logger.info('unassign interface x2 and check...')
        flag = False
        interfaceObj.unassign_interface(interface = 'X2')
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']
        type_x3 = output_x2['interfaces'][0]['ipv4']['ip_assignment']
        logger.info(type_x2)
        logger.info(type_x3)
        if not type_x2 and not type_x3:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: unassign interface x2 and check failed")


class Test_28_WireMode_2580_tc_1511487(Test):
    uuid = "SOSAIOT-TC-57493"
    description= show_testcase_info(Parameter.TESTPLAN, '1511487', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511487')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unassign_x2_x3_and_check_mac_address(self):
        logger.info('unassign x2 x3 and check mac address...')
        global mac_x2
        global mac_x3
        mac_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        mac_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(mac_x2)
        logger.info(mac_x3)
        Assertion.assert_equal(True, True, "ERR: unassign x2 x3 and check mac address failed")

    def test_02_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    def test_03_check_interface_x2_x3_status(self):
        logger.info('check interface x2 x3 status...')
        flag = False
        output_x2 = interfaceObj.get_interface_status(name = 'X2')
        output_x3 = interfaceObj.get_interface_status(name = 'X3')
        type_x2 = output_x2['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        type_x3 = output_x3['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type']
        logger.info(type_x2)
        logger.info(type_x3)
        if type_x2 == 'inspect' and type_x3 == 'inspect':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check interface x2 x3 status failed")

    def test_04_check_mac_address_not_overridden(self):
        logger.info('check mac address not overridden...')
        flag = False
        output_x2 = interfaceObj.get_interface_mac(interface = 'X2')
        output_x3 = interfaceObj.get_interface_mac(interface = 'X3')
        logger.info(output_x2)
        logger.info(output_x3)
        logger.info(mac_x2)
        logger.info(mac_x3)
        if str(output_x2) == str(mac_x2) and str(output_x3) == str(mac_x3):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check mac address not overridden failed")


class Test_29_WireMode_2580_tc_1511488(Test):
    uuid = "SOSAIOT-TC-57494"
    description= show_testcase_info(Parameter.TESTPLAN, '1511488', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511488')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")

    @repeat_method(3)
    def test_02_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(30)
        flag = False
        cmd = 'rm -rf {}/klez.h.bin'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd))
        pc3_ssh.send_command(cmd)
        output = pc3_ssh.send_command('ls -l {}'.format(Parameter.TMP_PATH))
        logger.info(output)
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '{}/klez.h.bin'.format(Parameter.TMP_PATH) +' root ' + Parameter.PC4_ETH0 + \
             ' {}/klez.h.bin'.format(Parameter.TMP_PATH)  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l {}'.format(Parameter.TMP_PATH)
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_30_WireMode_2580_tc_1511491(Test):
    uuid = "SOSAIOT-TC-57497"
    description= show_testcase_info(Parameter.TESTPLAN, '1511491', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511491')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_inspect(self):
        logger.info('config interface x2 to wiremode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode inspect failed")
   
    def test_02_capture_packets_and_check(self):
        logger.info('capture packets and check...')
        flag = False
        logger.info('start capture....')
        captureObj.clear_packets()
        captureObj.start_capture()
        cmd = 'ping -c 10 {}'.format(Parameter.PC4_ETH0)
        pc3_ssh.send_command(cmd)
        sleep(5)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r".*172.16.4.104.*172.16.3.103.*", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: from pc3 ping pc4 and capture packets failed")


class Test_31_WireMode_2580_tc_1511499(Test):
    uuid = "SOSAIOT-TC-57505"
    description= show_testcase_info(Parameter.TESTPLAN, '1511499', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511499')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode_bypass(self):
        logger.info('config interface x2 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': True,        
            'stateful_inspection': False,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_02_disable_x2_and_check_x3_status(self):
        logger.info('disable x2 and check x3 status...')
        flag = False
        interfaceObj.disable_interface(name = 'X2')
        output = interfaceObj.get_interface_report_status()
        logger.info(output[3])
        if re.search(r"status\':\s\'No link", str(output[3]), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: disable x2 and check x3 status failed")


class Test_32_WireMode_2580_tc_1511500(Test):
    uuid = "SOSAIOT-TC-57506"
    description= show_testcase_info(Parameter.TESTPLAN, '1511500', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1511500')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_x2_and_check_x3_status(self):
        logger.info('enable x2 and check x3 status...')
        flag = False
        interfaceObj.enable_interface(name = 'X2')
        sleep(10)
        output = interfaceObj.get_interface_report_status()
        logger.info(output[3])
        if re.search(r"status\':\s\'1 Gbps Full Duplex", str(output[3]), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable x2 and check x3 status failed")

