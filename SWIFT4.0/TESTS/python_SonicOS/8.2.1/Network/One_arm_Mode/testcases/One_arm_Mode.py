from definition.settings import *
# from definition.utils import *


class TestGUITC01(Test):
    uuid = "SOSAIOT-TC-56922"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_x2_is_one_arm(self):
        output = interfaceapi.get_interface_status("X2")
        res = False
        try:
            base_dict = output['interfaces'][0]['ipv4']
            res = base_dict['one_arm_mode'] and base_dict['one_arm_peer'] == PC2_ETH2_IP
        except Exception as e:
            logger.error(f"check x2 json failed:\n{e}")
        Assertion.assert_equal(res, True, "ERR: check x2 is one arm interface failed")

    def test_02_verify_ping_to_pc3_passed(self):
        res = PC1_login.ping_from_eth(PC3_ETH1_IP, 'eth2', 5)
        Assertion.assert_equal(res, True, f"ERR: check mgmt ping failed")


class TestGUITC02(Test):
    uuid = "SOSAIOT-TC-56923"
    description = show_testcase_info(TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_to_wan_one_arm(self):
        rc = interfaceapi.config_interface(**x2_wan_arm_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_check_x2_is_one_arm(self):
        TestGUITC01().test_01_check_x2_is_one_arm()


class TestGUITC05(Test):
    uuid = "SOSAIOT-TC-56924"
    description = show_testcase_info(TESTPLAN, '05', description=True)['title']
    new_peer_ip = '99.99.99.99'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_to_lan_one_arm(self):
        x2_dict = copy.deepcopy(x2_lan_arm_dict)
        x2_dict['one_arm_peer'] = self.new_peer_ip
        rc = interfaceapi.config_interface(**x2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_check_x2_is_one_arm(self):
        output = interfaceapi.get_interface_status("X2")
        res = False
        try:
            base_dict = output['interfaces'][0]['ipv4']
            res = base_dict['one_arm_peer'] == self.new_peer_ip \
                  and base_dict['management']['https'] \
                  and base_dict['user_login']['https']
        except Exception as e:
            logger.error(f"check x2 json failed:\n{e}")
        Assertion.assert_equal(res, True, "ERR: check x2 is one arm interface failed")


class TestGUITC06(Test):
    uuid = "SOSAIOT-TC-56925"
    description = show_testcase_info(TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_to_pppoe(self):
        pppoe_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'autotest',
            'pppoe_passwd': 'password',
            'pppoe_service': '',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': False,
            'pppoe_ip': '11.22.33.44',
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
        }
        rc = interfaceapi.config_interface(**pppoe_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to pppoe failed")

    def test_02_config_x2_to_dhcp(self):
        dhcp_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'dhcp',
            'force_discover_interval': False,
            'initiate_renewals_with_discover': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
        }
        rc = interfaceapi.config_interface(**dhcp_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to dhcp failed")

    def test_03_config_x2_to_lan_one_arm(self):
        rc = interfaceapi.config_interface(**x2_lan_arm_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_04_check_x2_is_one_arm(self):
        TestGUITC01().test_01_check_x2_is_one_arm()


class TestGUITC07(Test):
    uuid = "SOSAIOT-TC-56926"
    description = show_testcase_info(TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_one_arm_route(self):
        res = False
        output = routepolicyapi.get_route_policy()
        match_list = [
            "interface': 'X2",
            "source': {'any': True}",
            "destination': {'any': True}",
            "gateway': {'name': 'X2 one-arm Peer'}",
        ]
        if output:
            for route in output['route_policies']:
                match_result = [x in str(route) for x in match_list]
                logger.info(f'match result is: {match_result}')
                if all(match_result) and len(match_result) == 4:
                    logger.info(f'get match route: {route}')
                    res = True
                    break
        else:
            logger.info('can not get route list via api.')
        Assertion.assert_equal(res, True, "ERR: check one arm route failed")


class TestTrafficTC08(Test):
    uuid = "SOSAIOT-TC-56927"
    description = show_testcase_info(TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_x2_is_one_arm(self):
        output = interfaceapi.get_interface_status("X2")
        res = False
        try:
            base_dict = output['interfaces'][0]['ipv4']
            res = base_dict['one_arm_mode'] and base_dict['one_arm_peer'] == PC2_ETH2_IP
        except Exception as e:
            logger.error(f"check x2 json failed:\n{e}")
        Assertion.assert_equal(res, True, "ERR: check x2 is one arm interface failed")

    @repeat_method(5)
    def test_02_verify_pc1_ping_to_pc3_passed(self):
        logger.info('wait for 10s to valid configure...')
        time.sleep(10)
        res = PC1_login.ping_from_eth(PC3_ETH1_IP, 'eth2', 5)
        Assertion.assert_equal(res, True, f"ERR: check pc1 ping to pc3 failed")


class TestGUITC23(Test):
    uuid = "SOSAIOT-TC-56933"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_one_arm_in_acl(self):
        res = False
        getres = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='LAN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['from'] == 'X2' and rule['ipv4']['to'] == 'X2':
                    logger.info(f'get target rule successful: {rule}')
                    res = True
                    break
        except exception as e:
            logger.info(f'get lan to wan acl failed: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: check X2 to X2 in acl failed...")


class TestTCPSYNfloodTC31(Test):
    uuid = "SOSAIOT-TC-56936"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_check_one_arm_in_syn_flood(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        logger.info('wait for 10s to send hpings...')
        time.sleep(10)
        output = PC1_login.send_command(f'hping3 -S -i u500 {PC3_ETH1_IP} -c 1000')
        logger.info(f'send hping result:\n {output}')

        logger.info('wait for 10s to check log...')
        time.sleep(10)
        fw_logs = logapi.get_log(860)
        except_msg = 'Possible SYN Flood on IF X2'
        res = True if except_msg in str(fw_logs) else False
        Assertion.assert_equal(res, True, f"ERR: check syn flood in log failed")


class TestCLITC16(Test):
    uuid = "SOSAIOT-TC-56932"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']
    peer_ip = '192.168.20.222'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_one_arm_peer(self):
        output = interfacecli.config_one_arm_interface(interface='X2', peer=self.peer_ip)
        Assertion.assert_equal(output, True, "ERR: configure one arm peer failed")

    def test_02_check_one_arm_peer_in_interface(self):
        output = interfaceapi.get_interface_status(name='X2')
        res = True if self.peer_ip in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check one arm peer failed")


class TestDHCPTC25(Test):
    uuid = "SOSAIOT-TC-56934"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_one_arm_peer_in_dhcp_wan(self):
        output = interfaceapi.config_interface(**x2_dhcp_arm_dict)
        Assertion.assert_equal(output, True, "ERR: configure one arm peer failed")

    @repeat_method(5)
    def test_02_check_dhcp_ip_in_x2(self):
        logger.info('wait for 20s to check x2 ip...')
        time.sleep(20)
        output = interfaceapi.get_interface_address(name='X2')
        res = True if Parameter.X2_IP in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check dhcp ip in x2 failed")

    @repeat_method(5)
    def test_03_verify_pc1_ping_to_pc3_passed(self):
        logger.info('wait for 10s to valid configure...')
        time.sleep(10)
        res = PC1_login.ping_from_eth(PC3_ETH1_IP, 'eth2', 5)
        Assertion.assert_equal(res, True, f"ERR: check pc1 ping to pc3 failed")


# must config interface to wan zone
class TestGAVTC11(Test):
    uuid = "SOSAIOT-TC-56928"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_to_wan_one_arm(self):
        output = interfaceapi.config_interface(**x2_wan_arm_dict)
        Assertion.assert_equal(output, True, "ERR: Config X2 to static failed")

    def test_02_gav_configure(self):
        gav_dict = {
            'enable_GAV': True,
            'inbound_ftp': True,
        }
        output = gavapi.config_gav(**gav_dict)
        Assertion.assert_equal(output, True, "ERR: configure gav failed")

    @repeat_method(5)
    def test_03_verify_http_access_be_block_by_gav(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        logger.info('waiting for 10s to valid gav configure...')
        time.sleep(20)
        searchv4_web_cmd = [
            'echo '' > /tmp/gav.txt',
            f'curl http://{PC3_ETH1_IP}/Exploit.VBS.Agent.q.gz -o /tmp/gav.txt',
            'cat /tmp/spyware.txt'
        ]
        output = PC1_login.send_commands(searchv4_web_cmd)
        logger.info(output)

        logger.info('wait for 10s to check log...')
        time.sleep(10)
        fw_logs = logapi.get_log(809)
        except_msg = 'Gateway Anti-Virus Alert: AutoRun.L'
        res = True if except_msg in str(fw_logs) else False
        Assertion.assert_equal(res, True, "ERR: gav block from wan server failed.")


class TestSpywareTC12(Test):
    uuid = "SOSAIOT-TC-56930"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_spyware_configure(self):
        antispy_json = {
            'enable': True,
            'high_danger_prevent': True,
            'medium_danger_prevent': True,
            'low_danger_prevent': True,
            'high_danger_detect': True,
            'medium_danger_detect': True,
            'low_danger_detect': True,
        }
        output = spywareapi.config_antispyware(**antispy_json)
        Assertion.assert_equal(output, True, "ERR: configure spyware failed")

    @repeat_method(5)
    def test_02_verify_http_access_be_block_by_spyware(self):
        logger.info('waiting for 20s to valid spyware configure...')
        time.sleep(20)
        searchv4_web_cmd = [
            'echo '' > /tmp/spyware.txt',
            f'curl http://{PC3_ETH1_IP}/spy_3_449.bin -k -o /tmp/spyware.txt',
            'cat /tmp/spyware.txt'
        ]
        output = PC1_login.send_commands(searchv4_web_cmd)
        logger.info(output)

        logger.info('wait for 10s to check log...')
        time.sleep(10)
        fw_logs = logapi.get_log(794)
        except_msg = 'Anti-Spyware Prevention Alert: Malformed-rtf'
        res = True if except_msg in str(fw_logs) else False
        Assertion.assert_equal(res, True, "ERR: spyware block from wan server failed.")


class TestIPSTC13(Test):
    uuid = "SOSAIOT-TC-56929"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ips_configure(self):
        enable_ips_dict = {
            "intrusion_prevention": {
                "enable": True,
                "signature_group": {
                    "high_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    },
                    "low_priority": {
                        "detect_all": True,
                        "log_redundancy": {
                            "value": 60
                        },
                        "prevent_all": True
                    },
                    "medium_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    }
                }
            }
        }
        output = ipsapi.config_IPS_global(**enable_ips_dict)
        Assertion.assert_equal(output, True, "ERR: configure ips failed")

    @repeat_method(5)
    def test_02_verify_http_access_be_block_by_ips(self):
        logger.info('waiting for 20s to valid ips configure...')
        time.sleep(20)
        searchv4_web_cmd = [
            'echo '' > /tmp/ips.txt',
            f'curl --connect-timeout 5 http://{PC3_ETH1_IP}/IPS_5342_high_poc.xls -o /tmp/ips.txt',
        ]
        output = PC1_login.send_commands(searchv4_web_cmd)
        logger.info(output)

        logger.info('wait for 10s to check log...')
        time.sleep(10)
        fw_logs = logapi.get_log(609)
        except_msg = 'IPS Prevention Alert: BAD-FILES Microsoft Excel String Copy Buffer Overflow'
        res = True if except_msg in str(fw_logs) else False
        Assertion.assert_equal(res, True, "ERR: ips block from wan server failed.")


class TestDPISSL14(Test):
    uuid = "SOSAIOT-TC-56931"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_dpissl_client(self):
        client_dict = {
            'enable': True,
            'application_firewall': False,
            'intrusion_prevention': True,
            'gateway_anti_virus': True,
            'gateway_anti_spyware': True,
            'content_filter': True,
            'auth_server_for_decrypted_connections': False,
            'deployment_server_domains': False,
            'bypass_decryption': True,
            'audit_built_in_exclusion': False,
            'authenticate_server': False,
            'open_failed_connections': True,
        }
        output = clientsslapi.config_general_settings(**client_dict)
        Assertion.assert_equal(output, True, "ERR: configure dpissl client failed")

    def test_02_check_dpissl_function(self):
        logger.info('waiting for 20s to valid ips configure...')
        time.sleep(20)
        cmd = f'echo | openssl s_client -connect {PC3_ETH1_IP}:443 2>/dev/null'
        logger.info(f'send cmd : {cmd}')
        output = PC2_login.send_command(cmd)
        Assertion.assert_regular(output, 'SonicWALL Firewall DPI-SSL', "ERR: check certificate failed")
