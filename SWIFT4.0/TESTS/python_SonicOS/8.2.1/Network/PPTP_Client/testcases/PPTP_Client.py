from definition.global_v import *


class TestPPTPClient_01(Test):
    uuid = "SOSAIOT-TC-57183"
    description= show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_X1_PPTP(self):
        x1_pptp_opts = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'test',
            'pptp_passwd': 'password',
            'pptp_server': PC2_ETH1_IP,
            'pptp_ip': '172.17.1.100',
            'pptp_netmask': Parameter.MASK,
            'pptp_gateway': '172.17.1.1',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        out = interface_obj.config_interface(**x1_pptp_opts)
        Assertion.assert_equal(out,True,"ERR: Configure X1 as PPTP failed!")

    def test_02_verify_X1(self):
        flag = False
        for i in range(1,5):
            time.sleep(3)
            x1_ip = interface_obj.get_interface_address("X1")["ip_address"]
            if x1_ip != '0.0.0.0':
                if re.match(r'1.190.201.\d+',x1_ip,re.I):
                    logger.info("PPTP ip is :" + x1_ip)
                    flag = True
                    break
            else:
               logger.info("X1 failed to get PPTP ip...")
        Assertion.assert_equal(flag,True,"ERR: Verify X1 as PPTP mode failed!")


class TestPPTPClient_02(Test):
    uuid = "SOSAIOT-TC-57185"
    description= show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_try_to_download_tsr(self):
        rc = system_obj.download_tsr()
        logger.info(rc)
        file_size = 0
        if os.path.exists('/tmp/techSupport'):
            file_size = os.path.getsize("/tmp/techSupport")
            logger.info("tsr file size is " + str(file_size))
            if file_size:
                pass
            else:
                Assertion.assert_equal(False, True, "ERR: Download tsr failed")
        else:
            Assertion.assert_equal(False, True, "ERR: Download tsr failed")

    def test_03_Verify_tsr(self):
        flag = False 
        if os.path.exists("/tmp/techSupport"):
            tsr_content = os.popen('cat /tmp/techSupport').read()
            start = "#Network\s*:\s*Interfaces_START"
            end = "#Network\s*:\s*Interfaces_END"
            match = re.search(r'' + start + '(.*?)' + end + '', tsr_content, re.I|re.S)
            if match:
                output1 = match.group(1)
                start1 = "Interface\s*Name\s*:\s*X1"
                end1 = "Interface(?:\s*Name)?\s*:\s*X2(?:\s*-\s*Not configured)?"
                match1 = re.search(r'' + start1 + '(.*?)' + end1 + '', tsr_content, re.I|re.S)
                if match1:
                    output1 = match1.group(1)
                    logger.info(output1)
                    if re.search(r'PPTP\sclient\sstatus\s*:\sEnabled.*1\.190\.201\.\d+',output1, re.I|re.S|re.M):
                        flag = True
            else:
                logger.info("Not found the target tsr content part")
        else:
            logger.info("download tsr file fail")
        Assertion.assert_equal(flag, True, "ERR: Verify tsr failed")
           

class TestPPTPClient_03(Test):
    uuid = "SOSAIOT-TC-57184"
    description= show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_X1_dhcp(self):
        x1_dhcp = {
            'if': 'x1',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        output = interface_obj.config_interface(**x1_dhcp)
        Assertion.assert_equal(output, True, "ERR: Configure X1 status to DHCP failed")
    
    @repeat_method(3)
    def test_02_verify_X1(self):
        flag = False
        for i in range(1,5):
            time.sleep(3)
            x1_ip = interface_obj.get_interface_address("X1")["ip_address"]
            if x1_ip != '0.0.0.0':
                if re.match(r'172.17.1.\d+',x1_ip,re.I):
                    logger.info("DHCP ip is :" + x1_ip)
                    flag = True
                    break
            else:
               logger.info("X1 failed to get DHCP ip...")
        Assertion.assert_equal(flag,True,"ERR: Verify X1 as DHCP mode failed!")
