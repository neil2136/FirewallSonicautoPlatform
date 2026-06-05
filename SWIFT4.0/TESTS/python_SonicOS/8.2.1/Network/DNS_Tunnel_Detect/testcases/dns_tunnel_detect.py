from definition.settings import *
from definition.utils import *


# Expect： [Log Setting] Enable GUI display for "Drop DNS Packets Via Suspicious DNS Tunnel" and "DNS Tunnel Attack"
class TestDNSTunnel_TC13(Test):
    uuid = "SOSAIOT-TC-51705"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_security_log_gui(self):
        event_dict_1593 = {'log': {
            "event": [
                {
                    "id": 1593,
                    "name": "DNS Tunnel Attack",
                    "category": "Network",
                    "group": "DNS Security",
                    "priority_level": "warning",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 0
                    },
                    "syslog": {
                        "redundancy_interval": 0
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
        }}
        event_dict_1594 = {'log': {
            "event": [
                {
                    "id": 1594,
                    "name": "Drop DNS Packets Via Suspicious DNS Tunnel",
                    "category": "Network",
                    "group": "DNS Security",
                    "priority_level": "warning",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 0
                    },
                    "syslog": {
                        "redundancy_interval": 0
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
        }}
        res1 = logsettingsapi.edit_event(event_id=1593, **event_dict_1593)
        res2 = logsettingsapi.edit_event(event_id=1594, **event_dict_1594)
        Assertion.assert_equal(
            res1 & res2, True, 'Enable GUI display of log settings failed.')


# Expect: [FC:Tool test] Iodine tool test
class TestDNSTunnel_TC20(Test):
    uuid = "SOSAIOT-TC-51710"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_set_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=False)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection failed.')

    @repeat_method(3)
    def test_02_start_iodline_server_on_pc3(self):
        cls_res = logmonitorapi.clear_log()
        logger.info(f'clear log monitor result: {cls_res}')
        pc3_login.send_command('killall iodined')
        server_path = f'{install_iodine_path}/bin/iodined'
        pc3_login.send_command(f'chmod u+x {server_path}')
        logger.info("start iodine server on pc3...")
        output = pc3_login.send_command(f'{server_path} -P password {Parameter.DNS_IP} test.com')
        pid = pc3_login.send_command('pidof iodined')
        logger.info(f'iodined pid: {pid}')
        Assertion.assert_regular(output, "Listening to dns*", "ERR: setup iodline server on pc3 failed.")

    @repeat_method(3)
    def test_03_start_iodline_client_on_pc1(self):
        time.sleep(10)
        pc1_login.send_command('killall iodine')
        client_path = f'{install_iodine_path}/bin/iodine'
        pc1_login.send_command(f'chmod u+x {client_path}')
        logger.info("start iodline client on pc1...")
        output = pc1_login.send_command(f'{client_path} -P password -r {PC3_ETH1_IP} test.com')
        Assertion.assert_regular(output, 'Connection setup complete*', "ERR: start DNS tunnel on PC1(client) failed.")

    @repeat_method(3)
    def test_04_start_iodline_client_on_pc2(self):
        time.sleep(10)
        pc2_login.send_command('killall iodine')
        client_path = f'{install_iodine_path}/bin/iodine'
        pc2_login.send_command(f'chmod u+x {client_path}')
        logger.info("start iodline client on pc2...")
        output = pc2_login.send_command(f'{client_path} -P password -r {PC3_ETH1_IP} test.com')
        Assertion.assert_regular(output, 'Connection setup complete*', "start DNS tunnel on PC2(client) failed.")

    def test_05_check_dns_tunnel_status(self):
        res = False
        output1 = pc1_login.send_command('ifconfig')
        m = re.search('10.0.0.\d', output1, re.M | re.I)
        if m:
            logger.info(f'pc1 dns tunnel established succeed.\ngot tunnel ip address is {m.group()}')
            res = True
            logger.info('ping from pc1...')
            res &= pc1_login.ping(ip=Parameter.DNS_IP, num=10)
            logger.info('ping from pc2...')
            res &= pc2_login.ping(ip=Parameter.DNS_IP, num=10)
        else:
            logger.error('pc1 not got dns tunnel ip address')
        Assertion.assert_equal(res, True, "ERR: dns tunnel is not up")

    @repeat_method(6)
    def test_06_check_suspicious_client(self):
        time.sleep(50)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(PC1_ETH1_IP, str(resp),
                                 'ERR: check "Detected Suspicious Clients Information" table failed')

    @repeat_method(5)
    def test_07_check_log(self):
        time.sleep(5)
        resp = logmonitorapi.get_log(id=1593)
        Assertion.assert_regular(json.dumps(resp), "Find DNS tunnel attack", "ERR: check log failed.")


# "Expect: [FC: Block test] Test the main control of option 'Block All The Clients DNS Traffic':  Disable all"
class TestDNSTunnel_TC28(Test):
    uuid = "SOSAIOT-TC-51718"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_dns_tunnel_traffic_should_pass(self):
        time.sleep(5)
        res1 = pc1_login.ping(ip=Parameter.DNS_IP, num=20)
        res2 = pc2_login.ping(ip=Parameter.DNS_IP, num=20)
        Assertion.assert_equal(res1 & res2, True, 'ERR: dns traffic are dropped.')


# 'Expect: [FC: Block test] Disable option "Block All The Clients DNS Traffic" when some clients are "Blocking"  and some clients are not, and then enable option "Block All The Clients DNS Traffic" again'
class TestDNSTunnel_TC29(Test):
    uuid = "SOSAIOT-TC-51719"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(5)
    def test_01_enable_signal_client_block_checkbox(self):
        time.sleep(5)
        res = dnssecurityapi.enable_dns_tunnel_client_block_checkbox(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, 'ERR: enable block checkbox failed.')

    @repeat_method(3)
    def test_02_verify_clients_dns_tunnel_traffic(self):
        time.sleep(5)
        logger.info('pc1 dns tunnel traffic should be block')
        res1 = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        logger.info('pc2 dns tunnel traffic should pass')
        res2 = pc2_login.ping(Parameter.DNS_IP)
        Assertion.assert_equal((not res1) & res2, True, 'ERR：verify dns tunnel clients traffic failed.')

    @repeat_method(5)
    def test_03_disable_client_block_checkbox(self):
        time.sleep(5)
        res = dnssecurityapi.disable_dns_tunnel_client_block_checkbox(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, 'ERR: disable block checkbox failed.')

    @repeat_method(3)
    def test_04_verify_traffic_pass_after_disable(self):
        time.sleep(5)
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, True, 'ERR：verify dns tunnel clients traffic failed.')

    def test_05_enable_block_all(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=True)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection failed.')

    @repeat_method(5)
    def test_06_check_client_block_checkbox_status(self):
        time.sleep(10)
        resp = dnssecurityapi.show_detected_client()
        resp = json.dumps(resp)
        res1 = '"block": "Enable"' in resp and PC1_ETH1_IP in resp
        res2 = '"block": "Enable"' in resp and get_pc2_eth1_ip() in resp
        Assertion.assert_equal(res1 & res2, True, 'ERR: verify clients block checkbox status failed.')

    @repeat_method(3)
    def test_07_verify_dns_tunnel_traffic(self):
        cls_res = logmonitorapi.clear_log()
        logger.info(f'clear log monitor result: {cls_res}')
        time.sleep(10)
        logger.info('pc1 dns tunnel traffic should be block')
        res1 = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        logger.info('pc2 dns tunnel traffic should be block')
        res2 = pc2_login.ping(Parameter.DNS_IP)
        Assertion.assert_equal(res1 | res2, False, 'verify dns tunnel clients traffic failed.')


# Expect: [FC: Block test] Test the main control of option "Block All The Clients DNS Traffic": Enable all
class TestDNSTunnel_TC27(Test):
    uuid = "SOSAIOT-TC-51717"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_block_all(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=True)
        Assertion.assert_equal(res, True, 'set dns tunnel detection failed.')

    def test_02_check_client_detected_method(self):
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular('"detection_method": "Corner DNS Type"', json.dumps(resp),
                                 'ERR: client detected method is not Corner DNS')

    def test_03_check_client_block_checkbox_status(self):
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular('"block": "Enable"', json.dumps(resp), 'ERR: client block checkbox status is disable')

    def test_04_verify_dns_tunnel_traffic_should_be_block(self):
        time.sleep(5)
        res1 = pc1_login.ping(ip=Parameter.DNS_IP, num=20)
        res2 = pc2_login.ping(ip=Parameter.DNS_IP, num=20)
        Assertion.assert_equal(res1 | res2, False, 'ERR: dns traffic are not suspended.')


# Expect: [FC: White list] Add the dns tunnel client into white list after it has been detected
class TestDNSTunnel_TC32(Test):
    uuid = "SOSAIOT-TC-51722"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_client_into_white_list(self):
        res = dnssecurityapi.add_dns_tunnel_white_list(ip=PC1_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: add dns tunnel white list failed.")

    @repeat_method(3)
    def test_02_check_client_iodine_status(self):
        pc1_login.send_command('killall iodine')
        time.sleep(3)
        path = f'{install_iodine_path}/bin/iodine'
        logger.info("start iodline client...")
        output = pc1_login.send_command(f'{path} -P password -r {PC3_ETH1_IP} test.com')
        Assertion.assert_regular(output, 'Connection setup complete', "ERR: start DNS tunnel on PC1(client) failed.")

    def test_03_check_white_client_display(self):
        logger.info('check client in white list not in detection list')
        resp1 = dnssecurityapi.show_detected_client()
        res1 = PC1_ETH1_IP not in json.dumps(resp1)
        logger.info('check client display in white list')
        resp2 = dnssecurityapi.show_dns_white_tunnel_list()
        res2 = PC1_ETH1_IP in json.dumps(resp2)
        Assertion.assert_equal(res1 & res2, True, 'ERR: check client in white list display failed.')

    def test_04_check_white_client_dns_traffic(self):
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, True, 'ERR: client in white list dns traffic dropped.')


# Expect: [FC: White list] Delete the dns tunnel client from white list when dns tunnel is running on this client PC      
class TestDNSTunnel_TC33(Test):
    uuid = "SOSAIOT-TC-51723"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_block_all(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=True)
        Assertion.assert_equal(res, True, 'set dns tunnel detection failed.')

    def test_02_delete_client_from_white_list(self):
        res = dnssecurityapi.delete_dns_tunnel_white_list(ips=[PC1_ETH1_IP])
        Assertion.assert_equal(res, True, "ERR: delete client from dns tunnel white list failed.")

    def test_03_run_traffic(self):
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, True, 'ERR: pc1 sent pkts failed.')

    @repeat_method(7)
    def test_04_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(PC1_ETH1_IP, str(resp), 'ERR: check client in detection list failed')

    @repeat_method(15)
    def test_05_check_client_traffic_through_tunnel(self):
        time.sleep(30)
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, False, 'ERR: traffic through dns tunnel are not blocked')


# Expect: [FC: Node aging] Flushed if it deactivates in 15 mins. Stop sending DNS pkt   
class TestDNSTunnel_TC40(Test):
    uuid = "SOSAIOT-TC-51729"
    description = show_testcase_info(TESTPLAN, '40', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_config_pkt_monitor(self):
        pkt_moni_dict = {
            'monitor_filter': {
                'bidirectional': True,
                'destination_ports': '53',
                'ether_types': '',
                'interfaces': '',
                'ip_types': '',
                'status': {
                    'consumed': True,
                    'dropped': True,
                    'forwarded': True,
                    'generated': True
                }
            }
        }
        res = pktapi.conf_packmon(**pkt_moni_dict)
        Assertion.assert_equal(res, True, "ERR: configure pkt monitor Failed.")

    def test_02_check_client_dns_traffic_should_drop(self):
        cls_res = pktapi.clear_packets()
        logger.info(f'clear packet monitor result: {cls_res}')
        start_res = pktapi.start_capture()
        logger.info(f'start packet monitor result: {start_res}')
        pc1_login.send_command(f'python3 {script_file} dns_query')
        time.sleep(3)
        stop_res = pktapi.stop_capture()
        logger.info(f'stop packet monitor result: {stop_res}')
        packets = pktapi.export_captured_packets()
        res = check_dns_dropped_pkts(packets)
        Assertion.assert_equal(res, True, 'ERR: check client dns traffic failed.')

    @repeat_method(15)
    def test_03_check_if_client_release(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_not_regular(str(resp), PC1_ETH1_IP, "ERR: detected client flushed failed.")


# Expect: [Verdict verify] The number threshold for normal DNS types :  A, AAAA, CNAME default value is 1000
class TestDNSTunnel_TC42(Test):
    uuid = "SOSAIOT-TC-51730"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_dns_traffic(self):
        pc1_login.send_command(f'python3 {script_file} dns_1000')
        Assertion.assert_equal(True, True, 'ERR: send dns traffic failed.')

    @repeat_method(7)
    def test_02_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(str(resp), PC1_ETH1_IP, 'ERR: check client in detection list failed')

    @repeat_method(15)
    def test_03_wait_detected_client_flushed(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_not_regular(str(resp), PC1_ETH1_IP, 'ERR: detected client info flushed failed')


# Expect: [Verdict verify] The ratio threshold for corner DNS types: TXT, MX  default ratio is 10%
class TestDNSTunnel_TC43(Test):
    uuid = "SOSAIOT-TC-51731"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_dns_traffic(self):
        pc1_login.send_command(f'python3 {script_file} dns_10')
        Assertion.assert_equal(True, True, 'ERR: send dns traffic failed.')

    @repeat_method(7)
    def test_02_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(str(resp), PC1_ETH1_IP, 'ERR: check client in the detection list failed.')

    @repeat_method(15)
    def test_03_wait_detected_client_flushed(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_not_regular(str(resp), PC1_ETH1_IP, 'ERR: detected client info flushed failed')


# Expect: [Verdict verify] The minimum DNS packet number for DNS Tunnel detection: 100
class TestDNSTunnel_TC44(Test):
    uuid = "SOSAIOT-TC-51732"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_dns_traffic(self):
        pc1_login.send_command(f'python3 {script_file} dns_100')
        Assertion.assert_equal(True, True, "ERR: send dns traffic failed.")

    def test_02_check_client_in_detection_list(self):
        res = []
        for i in range(5):
            time.sleep(60)
            resp = dnssecurityapi.show_detected_client()
            if PC1_ETH1_IP in str(resp):
                res.append(False)
                break
            res.append(True)
        Assertion.assert_equal(all(res), True, 'ERR: check client in detection list failed')


# Expect: [Integrated] Verify CFS basic function when DNS tunnel is enabled
class TestDNSTunnel_TC64(Test):
    uuid = "SOSAIOT-TC-51737"
    description = show_testcase_info(TESTPLAN, '64', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '64')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(10, sleep=20)
    def test_01_check_cfs_status(self):
        time.sleep(10)
        resp = cfsapi.get_cfs_server_status()
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), 'Server is ready', 'ERR: CFS server is not ready')

    @repeat_method(10, sleep=20)
    def test_02_check_cfs_tool(self):
        diagapi.lookup_url_rating("baidu.com")
        resp = diagapi.get_url_rating_result()
        Assertion.assert_regular(json.dumps(resp), 'Search Engines and Portals',
                                 "ERR: check cfs function failed after enable dns tunnel detection")


# Restart: After rebooting, DNS tunnel function well
class TestDNSTunnel_TC82(Test):
    uuid = "SOSAIOT-TC-51749"
    description = show_testcase_info(TESTPLAN, '82', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '82')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_128_white_entries(self):
        tag = []
        for i in range(128):
            res = dnssecurityapi.add_dns_tunnel_white_list(ip=f'192.168.168.{i + 1}')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: add dns tunnel white list failed.")

    def test_02_restart_firewall(self):
        res = settingsapi.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot FW failed")

    def test_03_check_white_list(self):
        tag = []
        resp = str(dnssecurityapi.show_dns_white_tunnel_list())
        for i in range(128):
            res = True if f'192.168.168.{i + 1}' in resp else False
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: check white list failed after reboot")


# Prefs export and import test
class TestDNSTunnel_TC83(Test):
    uuid = "SOSAIOT-TC-51750"
    description = show_testcase_info(TESTPLAN, '83', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '83')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_exp_file(self):
        res = settingsapi.export_setting_exp(filepath=exp_file)
        logger.info('check exp file...')
        res = os.path.exists(exp_file)
        Assertion.assert_equal(res, True, 'ERR: export pref file failed')

    def test_02_restore_firewall(self):
        res = settingsapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, 'ERR: restore firewall failed')

    def test_03_import_exp_file(self):
        res = settingsapi.import_setting_exp(exp_file)
        Assertion.assert_equal(res, True, "ERR: import settings failed")

    def test_04_check_settings(self):
        tag = []
        resp = str(dnssecurityapi.show_dns_white_tunnel_list())
        for i in range(128):
            res = True if f'192.168.168.{i + 1}' in resp else False
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: check white list failed after restore")
