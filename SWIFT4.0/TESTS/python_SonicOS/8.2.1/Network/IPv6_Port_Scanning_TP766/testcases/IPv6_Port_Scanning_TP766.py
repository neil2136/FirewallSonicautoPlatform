from definition.init_param import *


class Test_01_IPv6_Port_Scanning_TP766_tc_1529658(Test):
    uuid = "SOSAIOT-TC-52899"
    description= show_testcase_info(Parameter.TESTPLAN, '1529658', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529658')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        logCategoryObj.logging_level(level = 'alert')
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv --scanflags SYNFIN {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP SYN/FIN packet dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_02_IPv6_Port_Scanning_TP766_tc_1529663(Test):
    uuid = "SOSAIOT-TC-52904"
    description= show_testcase_info(Parameter.TESTPLAN, '1529663', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529663')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sN SYNFIN {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP Null Flag dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_03_IPv6_Port_Scanning_TP766_tc_1529664(Test):
    uuid = "SOSAIOT-TC-52905"
    description= show_testcase_info(Parameter.TESTPLAN, '1529664', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529664')
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
        logger.info('start port scanning on pc2...')
        flag = False
        logCategoryObj.logging_level(level = 'debug')
        systemlogObj.clear_log()
        cmd = 'python3 {}/definition/send_tcp.py SA {}'.format(TESTPATH, WAN_IPV6)
        for i in range(3):
            output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP packet received on non-existent/closed connection; TCP packet dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")

    def test_04_disable_stealth_mode(self):
        logger.info('disable stealth mode on firewall advance...')
        ad = {
            'stealth_mode': False,
            'control_plane_flood_protection': False,
        }
        rc = advanceObj.config_advance(**ad)
        Assertion.assert_equal(rc, True, "ERR: disable stealth mode failed")


class Test_04_IPv6_Port_Scanning_TP766_tc_1529665(Test):
    uuid = "SOSAIOT-TC-52906"
    description= show_testcase_info(Parameter.TESTPLAN, '1529665', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529660')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sF {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP FIN packet dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_05_IPv6_Port_Scanning_TP766_tc_1529666(Test):
    uuid = "SOSAIOT-TC-52907"
    description= show_testcase_info(Parameter.TESTPLAN, '1529666', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529666')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sT {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP connection dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_06_IPv6_Port_Scanning_TP766_tc_1529659(Test):
    uuid = "SOSAIOT-TC-52900"
    description= show_testcase_info(Parameter.TESTPLAN, '1529659', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529659')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_log_event(self):
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

    @repeat_method(3)
    def test_02_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'python3 {}/definition/send_tcp.py S {}'.format(TESTPATH, WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(10)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP Flag\(s\):\s+SYN.*TCP packet dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_07_IPv6_Port_Scanning_TP766_tc_1529660(Test):
    uuid = "SOSAIOT-TC-52901"
    description= show_testcase_info(Parameter.TESTPLAN, '1529660', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529660')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sV --version-intensity 9 {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP Connection Abort', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_08_IPv6_Port_Scanning_TP766_tc_1529661(Test):
    uuid = "SOSAIOT-TC-52902"
    description= show_testcase_info(Parameter.TESTPLAN, '1529661', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529661')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sO -sV {}'.format(WAN_IPV6)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'Malformed or unhandled IP packet dropped', str(rc), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")


class Test_09_IPv6_Port_Scanning_TP766_tc_1529662(Test):
    uuid = "SOSAIOT-TC-52903"
    description= show_testcase_info(Parameter.TESTPLAN, '1529662', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529662')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_port_scanning_and_verify_log(self):
        logger.info('start port scanning on pc2...')
        flag = False
        systemlogObj.clear_log()
        cmd = 'nmap -6 -vv -sW {}'.format(WAN_IPV6)
        pc2_ssh.send_command(cmd)
        sleep(5)
        output = pc2_ssh.send_command(cmd)
        logger.info(output)
        sleep(5)
        rc = systemlogObj.get_log()
        logger.info(rc)
        if re.search(r'TCP packet received on non-existent/closed connection; TCP packet dropped', str(rc), re.I|re.DOTALL) != None:
            flag =True
        Assertion.assert_equal(flag, True, "ERR: start port scanning and verify log failed")