from definition.init_param import *


class Test_01_Port_Scanning_tc_1(Test):
    uuid = "SOSAIOT-TC-52952"
    description= show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        logCategoryObj.logging_level(level = 'alert')
        systemlogObj.clear_log()
        cmd = 'nmap -vv --scanflags SYNFIN {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP SYN/FIN packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_02_Port_Scanning_tc_2(Test):
    uuid = "SOSAIOT-TC-52957"
    description= show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sN SYNFIN {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP Null Flag dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_03_Port_Scanning_tc_5(Test):
    uuid = "SOSAIOT-TC-52958"
    description= show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_stealth_mode(self):
        logger.info('enable stealth mode on firewall advance...')
        ad = {
            'stealth_mode': True,
            'control_plane_flood_protection': False,
        }
        rc = advanceObj.config_advance(**ad)
        Assertion.assert_equal(rc, True, "ERR: enable stealth mode failed")

    def test_02_enable_log_event(self):
        logger.info('enable log event 888...')
        le = {
            "log": {
                "event": [
                    {
                        "id": 888,
                        "name": "TCP Connection Does Not Exist",
                        "category": "Network",
                        "group": "TCP",
                        "priority_level": "debug",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {
                            "redundancy_interval": 60
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**le)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: enable log event failed")


    def test_03_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        cmd_upload = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '{}/nemesis '.format(binPath) +' root ' + PC3_DMZ_IP + \
             ' /home '  + ' password 22'
        logger.info('run cmd in pc1:{}'.format(cmd_upload))
        local_host.send_command(cmd_upload)
        logCategoryObj.logging_level(level = 'debug')
        systemlogObj.clear_log()
        pc3_ssh.send_command('chmod 777 /home/nemesis ')
        cmd = '/home/nemesis tcp -v -fSA -D {}'.format(WAN_IP)
        pc3_ssh.send_command(cmd)
        sleep(2)
        pc3_ssh.send_command(cmd)
        sleep(2)
        pc3_ssh.send_command(cmd)
        sleep(2)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP packet received on non-existent/closed connection; TCP packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


    def test_03_disable_stealth_mode(self):
        logger.info('disable stealth mode on firewall advance...')
        ad = {
            'stealth_mode': False,
            'control_plane_flood_protection': False,
        }
        rc = advanceObj.config_advance(**ad)
        Assertion.assert_equal(rc, True, "ERR: disable stealth mode failed")


class Test_04_Port_Scanning_tc_7(Test):
    uuid = "SOSAIOT-TC-52959"
    description= show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sF {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP FIN packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")



class Test_05_Port_Scanning_tc_9(Test):
    uuid = "SOSAIOT-TC-52960"
    description= show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sT {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP connection dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_06_Port_Scanning_tc_12(Test):
    uuid = "SOSAIOT-TC-52953"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_log_event(self):
        logger.info('enable log event 522...')
        le = {
            "log": {
                "event": [
                    {
                        "id": 522,
                        "name": "Malformed IP Packet",
                        "category": "Network",
                        "group": "IP",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {
                            "redundancy_interval": 60
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        rc = logSettingObj.enable_event(**le)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: enable log event failed")

    def test_03_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sS -f {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'Malformed or unhandled IP packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_07_Port_Scanning_tc_15(Test):
    uuid = "SOSAIOT-TC-52954"
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sV --version_trace {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP Connection Abort', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_08_Port_Scanning_tc_16(Test):
    uuid = "SOSAIOT-TC-52955"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sO --version_trace {}'.format(WAN_IP)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'Malformed or unhandled IP packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_09_Port_Scanning_tc_18(Test):
    uuid = "SOSAIOT-TC-52956"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc3...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -vv -sW {}'.format(WAN_IP)
        pc3_ssh.send_command(cmd)
        sleep(5)
        output = pc3_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP packet received on non-existent/closed connection; TCP packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")