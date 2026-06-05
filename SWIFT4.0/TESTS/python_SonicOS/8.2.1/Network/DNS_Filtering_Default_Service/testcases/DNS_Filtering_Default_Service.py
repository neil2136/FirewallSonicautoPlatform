from definition.settings import *


class TestDNS_Filtering_Default_Service_001(Test):
    uuid = "SOSAIOT-TC-51579"
    description= show_testcase_info(Parameter.TESTPLAN, '001', description=True)['title']
    goto_teardown = True
    jira = 'Gen7-44568'

    def test_000_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '001')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_001_create_dns_rule(self):
        add_rule = {
            "dns_policies": [
                {
                    "name": "New_rule",
                    "priority": {
                        "manual": 1
                    },
                    "enable": True,
                    "source": {
                        "address": {
                            "any": True
                        }
                    },
                    "service": {
                        "name": "DNS (Name Service) UDP"
                    },
                    "from": "X0",
                    "action": {
                        "filter_profile": "Default Profile"
                    }
                }
            ]
        }
        rc = dnsrule_obj.add_dns_rule(**add_rule)
        Assertion.assert_equal(rc, True, "ERR: Create_dns_rule failed")

    def test_01_Check_dns_base_use_CLI(self):
        flag = False
        cmds = [
            'con',
            'show dns base',
            'exit'
        ]
        rc = fw_cli.do_cli_commands(cmds, tag=1)
        if Parameter.dns_Neustar1 in str(rc) and Parameter.dns_Neustar2 in str(rc) and Parameter.dns_Neustar2 in str(rc):
            flag = True
        else:
            logger.error('DNS base info is wrong.')
        Assertion.assert_equal(flag, True, "ERR: Check_dns_base_use_CLI failed.")

    def test_02_disable_dns_server_inherit(self):
        cmds = [
            'con',
            'no dns server inherit',
            'commit',
            'exit'
        ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: Disable_dns_server_inherit use CLI failed")

    def test_03_vefiry_DNS_Server_settings_in_tsr(self):
        flag = False
        tsr_content = down_tsr_obj.get_tsr_part('Network', lab1='DNS')
        logger.info(tsr_content)
        if Parameter.dns_Neustar1 in tsr_content and Parameter.dns_Neustar2 in tsr_content and Parameter.dns_Neustar2 in tsr_content:
            flag = True
        else:
            logger.error('Fail to get related tsr')
        Assertion.assert_equal(flag, True, "ERR: Verify forged ip in tsr failed")


class TestDNS_Filtering_Default_Service_002(Test):
    uuid = "SOSAIOT-TC-51408"
    description= show_testcase_info(Parameter.TESTPLAN, '002', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '002')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_packet_monitor(self):
        result = list()
        found = 0
        result.append(packet_obj.stop_capture())
        time.sleep(3)
        result.append(packet_obj.clear_packets())
        time.sleep(3)
        result.append(packet_obj.clear_packets())
        time.sleep(3)
        result.append(packet_obj.start_capture())
        for i in result:
            if i == True:
                found += 1
        Assertion.assert_equal(found, 4, "ERR: Config packet monitor failed")

    @repeat_method(3)
    def test_02_check_dns_query_from_packet(self):
        foundit = 0
        logger.info('Do dig to verify dns query')
        diag_command = 'dig www.baidu.com @'+ Parameter.FIREWALL
        logger.info(diag_command)
        for i in range(2):
            os.system(diag_command)
        logger.info('Export capture...')
        ret = packet_obj.export_captured_packets(format='text')
        logger.info(ret)
        Neustar_server = '156.154.54.200'
        match1 = re.search(r'Packet\snumber:.*?out:X1.*?Src=\[' + Parameter.X1_IP +'\].*?Dst=\[' + Neustar_server + '\].*?Packet\snumber', ret, re.I|re.S) 
        if match1:
            foundit += 1
        else:
            logger.error('Failed to match echo_request X1-X0 packet')
        Assertion.assert_equal(foundit, 1, "ERR: check_dns_query_from_packet failed")