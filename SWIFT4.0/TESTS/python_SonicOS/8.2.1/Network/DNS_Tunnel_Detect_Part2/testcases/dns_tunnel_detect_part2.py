from definition.settings import *
from definition.utils import *


# Expect:[GUI] Enable the option "Enable DNS Tunnel Detection"
class TestDNSTunnel_TC1(Test):
    uuid = "SOSAIOT-TC-51934"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=False)
        Assertion.assert_equal(res, True, 'ERR: enable dns tunnel detection option failed.')


# Expect: [GUI] Enable option "Block All The Clients DNS Traffic "
class TestDNSTunnel_TC2(Test):
    uuid = "SOSAIOT-TC-51935"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=True)
        Assertion.assert_equal(res, True, 'ERR: enable block all option failed.')


# Expect: [GUI] Disable the option "Enable DNS Tunnel Detection"
class TestDNSTunnel_TC3(Test):
    uuid = "SOSAIOT-TC-51704"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=False, block=True)
        Assertion.assert_equal(res, True, 'ERR: disable "Enable DNS Tunnel Detection" option failed.')


# Expect: [GUI] Disable option "Block All The Clients DNS Traffic" and disable option "Enable DNS Tunnel Detection"
class TestDNSTunnel_TC4(Test):
    uuid = "SOSAIOT-TC-51936"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=False, block=False)
        Assertion.assert_equal(res, True, 'ERR: disable both options failed.')


# Expect: [GUI-White list] Add button test: White List
class TestDNSTunnel_TC7(Test):
    uuid = "SOSAIOT-TC-51937"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_add_white_list_button(self):
        resp = ''
        add_res = dnssecurityapi.add_dns_tunnel_white_list(ip=PC1_ETH1_IP)
        if add_res:
            resp = dnssecurityapi.show_dns_white_tunnel_list()
        else:
            logger.error('add dns tunnel white list failed.')
        Assertion.assert_regular(str(resp), PC1_ETH1_IP, 'check add white list button failed.')


# Expect: [GUI-White list] Delete button test: Delete the selected White List
class TestDNSTunnel_TC8(Test):
    uuid = "SOSAIOT-TC-51938"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_del_white_list_button(self):
        resp = ''
        del_res = dnssecurityapi.delete_dns_tunnel_white_list(ips=[PC1_ETH1_IP])
        if del_res:
            resp = dnssecurityapi.show_dns_white_tunnel_list()
        else:
            logger.error('delete signal dns tunnel white list failed')
        Assertion.assert_not_regular(str(resp), PC1_ETH1_IP, "ERR: delete client from dns tunnel white list failed.")


# Expect: [GUI-White list] Delete All button test: Delete All White List
class TestDNSTunnel_TC9(Test):
    uuid = "SOSAIOT-TC-51939"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']
    clients = [PC1_ETH1_IP, PC2_ETH1_IP, PC3_ETH1_IP]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_multi_client_in_white_list(self):
        tag = []
        for client in self.clients:
            add_res = dnssecurityapi.add_dns_tunnel_white_list(ip=client)
            logger.info(f'add client in white list result: {add_res}')
        resp = dnssecurityapi.show_dns_white_tunnel_list()
        resp = json.dumps(resp)
        for client in self.clients:
            res = True if client in resp else False
            tag.append(res)
            logger.info(f'add {client} result: {res}')
        res = all(tag) if tag else False
        Assertion.assert_equal(res, True, 'ERR: add multi client in white list failed.')

    def test_verify_delete_all_button(self):
        del_res = dnssecurityapi.delete_dns_tunnel_white_list(ips=self.clients)
        logger.info(f'delete all clients in white list result: {del_res}')
        resp = dnssecurityapi.show_dns_white_tunnel_list()
        resp = json.dumps(resp)
        if del_res:
            tag = []
            for client in self.clients:
                check_res = True if client not in resp else False
                tag.append(check_res)
            res = all(tag)
        else:
            res = False
        Assertion.assert_equal(res, True, 'ERR: delete multi clients failed')


# Expect: [FC:Detect/Block] Option "DNS tunnel detection" disabled, option "Block All The Clients DNS Traffic " disabled
class TestDNSTunnel_TC21(Test):
    uuid = "SOSAIOT-TC-51711"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=False, block=False)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection option failed.')

    def test_02_start_iodline_server_on_pc3(self):
        pc3_login.send_command('killall iodined')
        time.sleep(5)
        server_path = f'{install_iodine_path}/bin/iodined'
        pc3_login.send_command(f'chmod u+x {server_path}')
        logger.info("start iodine server on pc3...")
        output = pc3_login.send_command(f'{server_path} -P password {Parameter.DNS_IP} test.com')
        pid = pc3_login.send_command('pidof iodined')
        logger.info(f'iodined pid: {pid}')
        Assertion.assert_regular(output, "Listening to dns*", "ERR: setup iodline server on pc3 failed.")

    def test_03_run_iodine_on_pc1(self):
        res = run_iodine_on_client(pc=pc1_login)
        Assertion.assert_equal(res, True, 'ERR: run tools on PC1 failed.')

    def test_04_verify_client_not_detected(self):
        res = check_client_not_detected()
        Assertion.assert_equal(res, True, 'ERR: check "Detected Suspicious Clients Information" table failed')


# Expect:  [FC:Detect/Block] Option "DNS tunnel detection" disabled, option "Block All The Clients DNS Traffic" enabled
class TestDNSTunnel_TC22(Test):
    uuid = "SOSAIOT-TC-51712"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=False, block=True)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection option failed.')

    def test_02_send_traffic_through_dns_tunnel(self):
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, True, 'ERR: traffic through dns tunnel pass.')

    def test_03_verify_client_not_detected(self):
        res = check_client_not_detected()
        Assertion.assert_equal(res, True, 'ERR: check "Detected Suspicious Clients Information" table failed')


# Expect:[FC:Detect/block] Option "DNS tunnel detection" enabled, option "Block All The Clients DNS Traffic" disabled
class TestDNSTunnel_TC23(Test):
    uuid = "SOSAIOT-TC-51713"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=False)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection option failed.')

    def test_02_send_traffic_through_dns_tunnel(self):
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, True, 'ERR: traffic through dns tunnel pass.')

    @repeat_method(6)
    def test_03_verify_client_is_detected(self):
        time.sleep(59)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(json.dumps(resp), PC1_ETH1_IP,
                                 'ERR: check "Detected Suspicious Clients Information" table failed')

    def test_04_verify_dns_traffic_not_dropped(self):
        res = check_dns_pkts(status="Forwarded")
        Assertion.assert_equal(res, True, 'ERR: verify client dns traffic not drop failed.')


#Expect: [FC: Block checkbox] Test the Block checkbox on "Detected Suspicious Clients Information" table: Option "Block All The Clients DNS Traffic" disabled.
class TestDNSTunnel_TC26(Test):
    uuid = "SOSAIOT-TC-51716"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_client_block_checkbox(self):
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(json.dumps(resp), '"block": "Disable"', 'ERR: Test the Block checkbox on "Detected Suspicious Clients Information" table failed.')


# Expect:[FC:Detect/block] Option "DNS tunnel detection" enabled, option "Block All The Clients DNS Traffic" enabled
class TestDNSTunnel_TC24(Test):
    uuid = "SOSAIOT-TC-51714"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_dns_tunnel_detection(self):
        res = dnssecurityapi.set_dns_tunnel(enable=True, block=True)
        Assertion.assert_equal(res, True, 'ERR: set dns tunnel detection option failed.')

    def test_02_enable_dns_security_log_gui(self):
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

    @repeat_method(5)
    def test_03_send_traffic_through_dns_tunnel(self):
        time.sleep(10)
        res = pc1_login.ping(ip=Parameter.DNS_IP, num=10)
        Assertion.assert_equal(res, False, 'ERR: traffic through dns tunnel pass.')

    @repeat_method(6)
    def test_04_verify_client_is_detected(self):
        time.sleep(59)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(json.dumps(resp), PC1_ETH1_IP,
                                 'ERR: check "Detected Suspicious Clients Information" table failed')

    @repeat_method(3)
    def test_05_check_log(self):
            resp = logmonitorapi.get_log(id=1594)
            Assertion.assert_regular(str(resp), "Drop DNS Packets Via Suspicious DNS Tunnel", "ERR: check log failed.")

    def test_06_check_client_dns_traffic_should_drop(self):
        res = check_dns_pkts(status="Dropped")
        Assertion.assert_equal(res, True, 'ERR: check client dns traffic failed.')


# Expect: [FC: Block checkbox] Test the Block checkbox on "Detected Suspicious Clients Information" table: Option "Block All The Clients DNS Traffic" enabled.
class TestDNSTunnel_TC25(Test):
    uuid = "SOSAIOT-TC-51715"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_client_block_checkbox(self):
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(json.dumps(resp), '"block": "Enable"', 'ERR: Test the Block checkbox on "Detected Suspicious Clients Information" table failed.')


# Expect: [FC: Block test] Verify only DNS traffic will be blocked
class TestDNSTunnel_TC30(Test):
    uuid = "SOSAIOT-TC-51720"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_icmp_traffic_not_blocked(self):
        pc1_login.send_command(f'route add -host {Parameter.X1_DNS1} gw {Parameter.FIREWALL}')
        res = pc1_login.ping(Parameter.X1_DNS1)
        Assertion.assert_equal(res, True, 'ERR: icmp traffic is blocked')


# Expect: [FC: White list] Add the dns tunnel client into white list at first
class TestDNSTunnel_TC31(Test):
    uuid = "SOSAIOT-TC-51721"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_pc1_to_white_list(self):
        res = dnssecurityapi.add_dns_tunnel_white_list(ip=PC1_ETH1_IP)
        Assertion.assert_equal(res, True, 'ERR: add pc1 eth1 to white list failed')

    def test_02_del_added_white_list(self):
        res = dnssecurityapi.delete_dns_tunnel_white_list(ips=[PC1_ETH1_IP])
        Assertion.assert_equal(res, True, 'ERR: del failed.')


# Expect: [FC: White list] Maximum add: add 128 IP into white list and simulate DNS tunnel traffic from these IP
class TestDNSTunnel_TC34(Test):
    uuid = "SOSAIOT-TC-51940"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_128_white_entries(self):
        tag = []
        for i in range(128):
            res = dnssecurityapi.add_dns_tunnel_white_list(ip=f'192.168.168.{i+1}')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: add dns tunnel white list failed.")


# Expect:  [Boundary test] Test boundary of IP address when add IP address into white list
class TestDNSTunnel_TC37(Test):
    uuid = "SOSAIOT-TC-51726"
    description = show_testcase_info(TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '37')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_add_129th_ip_to_white_list(self):
        res, msg = dnssecurityapi.add_dns_tunnel_white_list(ip='192.168.168.254', msg=True)
        logger.info(f'error message: {msg}')
        Assertion.assert_equal(res, False, "ERR: test boundary of IP address failed.")


# Expect: [FC: White list] Maximum delete: add 128 IP into white list and simulate DNS tunnel traffic from these IP, then delete all white list
class TestDNSTunnel_TC35(Test):
    uuid = "SOSAIOT-TC-51724"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_delete_all(self):
        clients = [f'192.168.168.{i+1}' for i in range(128)]
        res = dnssecurityapi.delete_dns_tunnel_white_list(ips=clients)
        Assertion.assert_equal(res, True, 'ERR: delete all failed.')


# Expect: [Error test] Add two duplicate IP address into white list
class TestDNSTunnel_TC36(Test):
    uuid = "SOSAIOT-TC-51725"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_one_white_list_entry(self):
        res = dnssecurityapi.add_dns_tunnel_white_list(ip='192.1.1.1')
        Assertion.assert_equal(res, True, "ERR：add failed.")

    def test_02_add_duplicate_white_list_entry(self):
        res, msg = dnssecurityapi.add_dns_tunnel_white_list(ip='192.1.1.1', msg=True)
        logger.info(f'add duplicate ip address result: {res}')
        Assertion.assert_regular(str(msg), 'Already exists', 'ERR: verify add duplicate IP failed.')


# Expect: [Error test] Add a whilte list with invalid IP address
class TestDNSTunnel_TC38(Test):
    uuid = "SOSAIOT-TC-51727"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_invaild_ip(self):
        res,msg = dnssecurityapi.add_dns_tunnel_white_list(ip='192.168.168.256',msg=True)
        logger.info(f'error message: {msg}')
        Assertion.assert_equal(res, False, "ERR: add failed.")


# Expect: [Navigate test] Add a white list but leave IP empty
class TestDNSTunnel_TC39(Test):
    uuid = "SOSAIOT-TC-51728"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_ip_empty(self):
        res, msg = dnssecurityapi.add_dns_tunnel_white_list(ip='', msg=True)
        logger.info(f'error message: {msg}')
        Assertion.assert_equal(res, False, "ERR: add failed.")


# Expect: [Verdict verify] Simulate tremendous DNS traffic to seduce wrong verdict
class TestDNSTunnel_TC45(Test):
    uuid = "SOSAIOT-TC-51941"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_simulate_tremendous_dns_traffic(self):
        pc1_login.send_command(f'python3 {script_file} dns_10000')
        Assertion.assert_equal(True, True, 'ERR: send dns traffic failed.')

    @repeat_method(7)
    def test_02_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(str(resp), PC1_ETH1_IP, 'ERR: check client in detection list failed')

    @repeat_method(15)
    def test_03_wait_client_release(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_not_regular(str(resp), PC1_ETH1_IP, "ERR: detected client flushed failed.")


# Expect:[Pcap simulate] Send malformed DNS pkts ratio test
class TestDNSTunnel_TC47(Test):
    uuid = "SOSAIOT-TC-51733"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_simulate_tremendous_dns_traffic(self):
        pc1_login.send_command(f'python3 {script_file} dns_10')
        Assertion.assert_equal(True, True, 'ERR: send dns traffic failed.')

    @repeat_method(7)
    def test_02_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(str(resp), PC1_ETH1_IP, 'ERR: check client in detection list failed')


# Expect: [Integrated] Test with DMZ zone
class TestDNSTunnel_TC57(Test):
    uuid = "SOSAIOT-TC-51735"
    description = show_testcase_info(TESTPLAN, '57', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_configure_x2_dmz(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(res, True, 'ERR: config x2 failed')

    def test_02_run_iodine_on_pc4(self):
        res = run_iodine_on_client(pc=pc4_login)
        Assertion.assert_equal(res, True, 'ERR: run tools on client failed.')

    @repeat_method(7)
    def test_03_check_client_in_detection_list(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_regular(str(resp), PC4_ETH1_IP, 'ERR: check client in detection list failed')

    @repeat_method(15)
    def test_04_wait_client_release(self):
        time.sleep(60)
        resp = dnssecurityapi.show_detected_client()
        Assertion.assert_not_regular(str(resp), PC4_ETH1_IP, "ERR: detected client flushed failed.")


# Expect： WAN zone does not support
class TestDNSTunnel_TC59(Test):
    uuid = "SOSAIOT-TC-51736"
    description = show_testcase_info(TESTPLAN, '59', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_configure_x2_wan(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        res = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(res, True, 'ERR: config x2 failed')

    def test_02_simulate_tremendous_dns_traffic(self):
        pc4_login.send_command(f'python3 {script_file} dns_10')
        Assertion.assert_equal(True, True, 'ERR: send dns traffic failed.')

    def test_03_check_client_in_detection_list(self):
        res = check_client_not_detected(client=PC4_ETH1_IP)
        Assertion.assert_equal(res, True, 'ERR: check client in detection list failed')


# Expect: CLI: Enable detect
class TestDNSTunnel_TC65(Test):
    uuid = "SOSAIOT-TC-51942"
    description = show_testcase_info(TESTPLAN, '65', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '65')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_detect(self):
        params = {
            'enable': True,
            'block-all': False,
            }
        res = dnscli.dns_tunnel_detection(**params)
        Assertion.assert_equal(res, True, "ERR: enable detect via CLI failed.")


# Expect: CLI: Enable block
class TestDNSTunnel_TC66(Test):
    uuid = "SOSAIOT-TC-51738"
    description = show_testcase_info(TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '66')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_block(self):
        params = {
            'enable': False,
            'block-all': True,
            }
        res = dnscli.dns_tunnel_detection(**params)
        Assertion.assert_equal(res, True, "ERR: enable detect via CLI failed.")


# Expect: CLI:White list add
class TestDNSTunnel_TC68(Test):
    uuid = "SOSAIOT-TC-51739"
    description = show_testcase_info(TESTPLAN, '68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '68')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_whitelist(self):
        tunnel_white_list = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
        res = dnscli.add_tunnel_white_list_entry(*tunnel_white_list)
        Assertion.assert_equal(res, True, 'ERR: add white list via CLI failed.')


# Expect: CLI: White list delete
class TestDNSTunnel_TC69(Test):
    uuid = "SOSAIOT-TC-51740"
    description = show_testcase_info(TESTPLAN, '69', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '69')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_whitelist(self):
        tunnel_white_list = ['1.1.1.1']
        res = dnscli.del_tunnel_white_list_entry(*tunnel_white_list)
        Assertion.assert_equal(res, True, "ERR: del white list via CLI failed.")


# Expect: CLI: White list delete all
class TestDNSTunnel_TC70(Test):
    uuid = "SOSAIOT-TC-51741"
    description = show_testcase_info(TESTPLAN, '70', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '70')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_del_all_whitelist(self):
        res = dnscli.del_tunnel_white_list_entry('all')
        Assertion.assert_equal(res, True, "ERR: del all white list via CLI failed.")


# Expect: CLI: diag dns security settings: The minimum DNS packet number for DNS Tunnel detection
class TestDNSTunnel_TC72(Test):
    uuid = "SOSAIOT-TC-51742"
    description = show_testcase_info(TESTPLAN, '72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '72')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_show_dns_tunnel_min(self):
        out_put = diagcli.show_advance('dns-security')
        Assertion.assert_regular(out_put, 'dns-tunnel-minimum.* 100', 'ERR: diag show min num failed. ')


# Expect:CLI: diag dns security settings: The ratio threshold for corner DNS types
class TestDNSTunnel_TC73(Test):
    uuid = "SOSAIOT-TC-51743"
    description = show_testcase_info(TESTPLAN, '73', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '73')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_show_dns_tunnel_ratio(self):
        out_put = diagcli.show_advance('dns-security')
        Assertion.assert_regular(out_put, '.*ratio-threshold 10', 'ERR: diag show min num failed. ')


# Expect:CLI: diag dns security settings: The number threshold for normal DNS types
class TestDNSTunnel_TC74(Test):
    uuid = "SOSAIOT-TC-51744"
    description = show_testcase_info(TESTPLAN, '74', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '74')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_show_dns_tunnel_num(self):
        out_put = diagcli.show_advance('dns-security')
        Assertion.assert_regular(out_put, '.*number-threshold 1000', 'ERR: diag show min num failed. ')


# Expect: [Diag page settings] Modify the value of option: The minimum DNS packet number for DNS Tunnel detect
class TestDNSTunnel_TC75(Test):
    uuid = "SOSAIOT-TC-51745"
    description = show_testcase_info(TESTPLAN, '75', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '75')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_conf_dns_tunnel_min(self):
        param = {
            'dns-tunnel-minimum-packet-number': 101
        }
        res = diagcli.diag_conf_dns_tunnel(**param)
        Assertion.assert_equal(res, True, 'ERR: diag conf dns tunnel min num failed. ')


# Expect: [Diag page settings] Modify the value of option: The ratio threshold for corner DNS types
class TestDNSTunnel_TC76(Test):
    uuid = "SOSAIOT-TC-51746"
    description = show_testcase_info(TESTPLAN, '76', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '76')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_conf_dns_tunnel_min(self):
        param = {
            'dns-tunnel-ratio-threshold': 11
        }
        res = diagcli.diag_conf_dns_tunnel(**param)
        Assertion.assert_equal(res, True, 'ERR: diag conf dns tunnel failed.')


# Expect: [Diag page settings] Modify the value of option: The number threshold for normal DNS types
class TestDNSTunnel_TC77(Test):
    uuid = "SOSAIOT-TC-51747"
    description = show_testcase_info(TESTPLAN, '77', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '77')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_diag_conf_dns_tunnel_ratio(self):
        param = {
            'dns-tunnel-number-threshold': 1001
        }
        res = diagcli.diag_conf_dns_tunnel(**param)
        Assertion.assert_equal(res, True, 'ERR: diag conf dns tunnel num threshold failed.')


# Expect: TSR: Check DNS Tunnel part in TSR
class TestDNSTunnel_TC84(Test):
    uuid = "SOSAIOT-TC-51751"
    description = show_testcase_info(TESTPLAN, '84', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '84')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_download_tsr(self):
        tsr_file = '/tmp/cyuan_tsr.txt'
        diagapi.download_tsr(filepath=tsr_file)
        res = os.path.exists(tsr_file)
        Assertion.assert_equal(res, True, 'ERR: download tsr file failed.')

    def test_02_check_dns_tunnel(self):
        n1 = pc1_login.send_command("""cat -n /tmp/cyuan_tsr.txt | grep "DNS Security_START" | awk '{print $1}'""").strip()
        n2 = pc1_login.send_command("""cat -n /tmp/cyuan_tsr.txt | grep "DNS Security_END" | awk '{print $1}'""").strip()
        data = pc1_login.send_command(f"head -{n2} /tmp/cyuan_tsr.txt | tail -{int(n2)-int(n1)}")
        logger.info(data)
        res = "Enable DNS Tunnel Detection: 1" in data and "Block All The Clients DNS Traffic: 1" in data
        Assertion.assert_equal(res, True, "ERR: check dns tunnel settings in tsr failed.")
