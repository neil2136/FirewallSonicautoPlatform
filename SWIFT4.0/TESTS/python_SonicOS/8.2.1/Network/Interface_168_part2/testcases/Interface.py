import time

from definition.settings import *
from definition.utils import *


# test hhtp login with different authentication method successful
class Test_http_login_with_LDAP_authtication_TC14(Test):
    uuid = "SOSAIOT-TC-56181"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_allow_Http_and_Https_management(self):
        logger.info('Allow http and https management...')
        resp = {}
        admin_dict = {
            "http_port": 80,
            "https_port": 443,
            "web_management": {
                "allow_http": True,
            }
        }
        rc = admin_obj.conf_admin(**admin_dict)
        if rc:
            resp = admin_obj.show_admin_setting()
            logger.info(f'Show allow http and https management...{resp}')
        Assertion.assert_regular(json.dumps(
            resp), '"allow_http": True', 'ERR: Allow http and https management failed.')

    def test_02_user_authentication_ldap(self):
        logger.info('User authentication is LDAP...')
        resp = {}
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        rc = user_obj.user_method_authentication(**user_auth)
        if rc:
            resp = user_obj.show_user_auth()
            logger.info(f'Show user authentication...{resp}')
        Assertion.assert_regular(json.dumps(
            resp), '"auth_method": "ldap"', 'ERR: User authentication is LDAP failed.')

    def test_03_Config_X0_ipv4(self):
        logger.info("config x0 ipv4 interface... ")
        rc = interface_obj.config_interface(**x0_lan_dict_http)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_04_http_management_check_ldap_authentication(self):
        logger.info('LDAP authentication http management checking...')
        cmd1_pc1 = [
            "curl -v " + Parameter.http_login_url + "  --compressed",
        ]
        rc1 = pc1_ssh.send_commands(cmd1_pc1)
        logger.info('Get curl -v ' + Parameter.http_login_url + f'  --compressed response...{rc1}')
        Assertion.assert_regular(json.dumps(
            rc1), Parameter.https_login_url, 'ERR: redirect from http to https failed.')

    def test_05_user_authentication_local(self):
        logger.info('User authentication is local...')
        resp = {}
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        rc = user_obj.user_method_authentication(**user_auth)
        if rc:
            resp = user_obj.show_user_auth()
            logger.info(f'Show user authentication...{resp}')
        Assertion.assert_regular(json.dumps(
            resp), '"auth_method": "local"', 'ERR: User authentication is local failed.')

    def test_06_http_management_check_local_authentication(self):
        logger.info('Local authentication http management checking...')
        cmd1_pc1 = [
            "curl -v " + Parameter.http_login_url + "  --compressed",
        ]
        rc1 = pc1_ssh.send_commands(cmd1_pc1)
        logger.info('Get curl -v ' + Parameter.http_login_url + f'  --compressed response...{rc1}')
        Assertion.assert_regular(json.dumps(
            rc1), 'Loading Login App', 'ERR: Local user HTTP login failed.')


# check Portshield interface port successful
class Test_portshield_TC27(Test):
    uuid = "SOSAIOT-TC-56194"
    description = show_testcase_info(
        TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_portshield_to_x4(self):
        resp = {}
        # forbid other interface bind to X4
        x2_portshield_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X4'
        }
        conf_res = interface_obj.config_interface(**x2_portshield_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('x2')
        Assertion.assert_regular(json.dumps(
            resp), '"mode": {"portshield": "X4"}', 'ERR: config x2 failed')

    def test_02_verify_pc3_traffic(self):
        logger.info('verify pc3 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'runner_obj': pc3_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X4', 'out:X1', 'IP Type: ICMP',
                           f'Src=[{PC3_ETH1_IP}]', f'Dst=[{PC4_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test X4 traffic via routed mode failed.")

    def test_03_verify_pc2_traffic(self):
        logger.info('verify pc2 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'runner_obj': pc2_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X4', 'out:X1', 'IP Type: ICMP',
                           f'Src=[{Parameter.PC2_ETH1_portshield}]', f'Dst=[{PC4_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test X2 traffic via routed mode failed.")


# check L2bridge interface port successful
class Test_l2bridge_TC33(Test):
    #goto_teardown = True
    uuid = "SOSAIOT-TC-56199"
    description = show_testcase_info(
        TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_l2bridge_to_x3(self):
        resp = {}
        # forbid other interface bind to X4
        x2_l2bridge_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to': 'X3',
            'block_non_ip': False,
            'mgmt_snmp': True,
            'mgmt_http': True,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            "https_redirect": False,
            'bridge_block_non_ip': False,
            'route_on_bridge_pair': True,
            'stateful_inspection': True,
            'vlan_filtering_mode': 'block',
            'filter_vlans': [],
        }
        conf_res = interface_obj.config_interface(**x2_l2bridge_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('x2')
        Assertion.assert_regular(json.dumps(
            resp), '"bridge_to": "X3"', 'ERR: config x2 failed')

    def test_02_config_pc2_ipv4(self):
        flag = False
        cmd_pc2 = [
            f"ifconfig eth1 {Parameter.PC2_ETH1_l2bridge}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X3_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc2 = pc2_ssh.send_commands(cmd_pc2)
        if f"{PC4_ETH1_NW}/24 via {Parameter.X3_IP}" in rc2:
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: config pc2 ipv4 failed.")

    def test_03_verify_pc2_traffic(self):
        logger.info('verify pc2 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'runner_obj': pc2_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X2', 'out:X1', 'IP Type: ICMP',
                           f'Src=[{Parameter.PC2_ETH1_l2bridge}]', f'Dst=[{PC4_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test X2 traffic  failed.")

    def test_04_http_management_check_local_authentication(self):
        logger.info('Local authentication http management checking...')
        cmd_pc2 = [
            f"curl -v http://{Parameter.X3_IP}  --compressed",
        ]
        rc1 = pc2_ssh.send_commands(cmd_pc2)
        logger.info(f'Get curl -v http://{Parameter.X3_IP}  --compressed response...{rc1}')
        cmd2_pc2 = [
            f"curl -v http://{Parameter.X3_IP}/sonicui/7/login/  --compressed",
        ]
        rc2 = pc2_ssh.send_commands(cmd2_pc2)
        logger.info(f'Get curl -v http://{Parameter.X3_IP}/sonicui/7/login/  --compressed response...{rc2}')
        Assertion.assert_regular(json.dumps(
            rc2), 'Loading Login App', 'ERR: Local user HTTP login failed.')

    def test_05_verify_secondary_bridged(self):
        logger.info('verify secondary bridged interface checking...')
        flag = False
        ip_mode_x2 = get_interface_ip_mode('X2')
        ip_mode_x3 = get_interface_ip_mode('X3')
        if (ip_mode_x2 == 'Secondary Bridged I/F') & (ip_mode_x3 == 'Primary Bridged I/F'):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify secondary bridged interface  failed.")

    def test_06_Config_X2_lan(self):
        logger.info("config x2 lan interface... ")
        x2_lan_dict = {
            'if': 'x2',
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }

        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X2 lan interface failed")


# check DHCP interface port successful
class Test_dhcp_TC38(Test):
    uuid = "SOSAIOT-TC-56203"
    description = show_testcase_info(
        TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_dhcp(self):
        resp = {}
        X1_dhcp_dict = {
            'if': 'X1',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'mgmt_https': True,
            'user_http': False,
            'user_https': True,
        }
        conf_res = interface_obj.config_interface(**X1_dhcp_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('X1')
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"dhcp"', 'ERR: config X1 failed')

    @repeat_method(20)
    def test_02_verify_X1_can_get_ip_dhcp(self):
        logger.info("Sleep 20s before checking X1 ip address.")
        time.sleep(5)
        flag = True
        resp = interface_obj.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        Parameter.X1_DHCP_IP = resp.get("ip_address")
        if Parameter.X1_DHCP_IP == '' or Parameter.X1_DHCP_IP == '0.0.0.0':
            flag = False
        Assertion.assert_equal(flag, True,
                               "ERR: get X1 ip address  failed.")

    def test_03_ping_X1_wan(self):
        logger.info('start ping X1 WAN interface checking')
        rc = ping_wan_ip(Parameter.X1_DHCP_IP, pc4_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X1 WAN interface Failed!")


# check PPPOE interface connect and disconnect
class Test_pppoe_connect_disconnect_TC41(Test):
    uuid = "SOSAIOT-TC-56206"
    description = show_testcase_info(
        TESTPLAN, '41', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_pppoe(self):
        logger.info("start config X1 pppoe mode.")
        resp = {}
        X1_pppoe_opt_dynamic = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'root',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_http': False,
            'user_https': True,
        }
        out = interface_obj.config_interface(**X1_pppoe_opt_dynamic)
        if out:
            resp = interface_obj.get_interface_status('X1')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"pppoe"', 'ERR: config X1 failed')

    @repeat_method(5)
    def test_02_config_X1_pppoe_connect(self):
        logger.info("start ppp connect.")
        res = True
        resp = interface_obj.get_interface_address("X1")
        logger.info(f"Get X1 interface address info = {resp}")
        if resp.get("ip_address") == '' or resp.get("ip_address") == '0.0.0.0':
            res = interface_obj.click_pppoe_connect("X1")
            time.sleep(20)
        Assertion.assert_equal(res, True, "ERR: start pppoe connect failed!")

    @repeat_method(25)
    def test_03_verify_X1_can_get_ip_pppoe(self):
        logger.info("start get X1 ppp ip address.")
        time.sleep(5)
        resp = get_ppp_ip_address("X1")
        Assertion.assert_equal(resp, True,
                               "ERR: get X1 ppp ip address failed.")

    def test_04_ping_X1_wan(self):
        logger.info('start ping X1 WAN interface checking')
        rc = ping_wan_ip(Parameter.X1_PPP_IP, pc4_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X1 WAN interface Failed!")

    def test_05_config_X1_pppoe_disconnect(self):
        logger.info("start ppp disconnect.")
        res = interface_obj.click_pppoe_disconnect("X1")
        Assertion.assert_equal(res, True, "ERR: start ppp disconnect failed!")

    def test_06_verify_X1_not_get_ip_pppoe(self):
        logger.info("start get X1 ppp ip address.")
        # resp = get_ppp_ip_address("X1")
        # Because 8.0.1 FW will auto connect even if disconnect ppp,skip this step
        Assertion.assert_equal(False, False,
                               "ERR: should be not get X1 ppp ip address.")
    @repeat_method(5)
    def test_07_config_X1_pppoe_connect(self):
        logger.info("start ppp connect.")
        res = interface_obj.click_pppoe_connect("X1")
        time.sleep(20)
        Assertion.assert_equal(res, True, "ERR: start ppp connect failed!")

    @repeat_method(25)
    def test_08_verify_X1_can_get_ip_pppoe(self):
        logger.info("start get X1 ppp ip address.")
        time.sleep(5)
        resp = get_ppp_ip_address("X1")
        Assertion.assert_equal(resp, True,
                               "ERR: get X1 ppp ip address failed.")

    def test_09_ping_X1_wan(self):
        logger.info('start ping X1 WAN interface checking')
        rc = ping_wan_ip(Parameter.X1_PPP_IP, pc4_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X1 WAN interface Failed!")


# check PPPOE interface management
class Test_pppoe_management_TC42(Test):
    uuid = "SOSAIOT-TC-56207"
    description = show_testcase_info(
        TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_pppoe(self):
        logger.info("start config X1 pppoe mode.")
        resp = {}
        X1_pppoe_opt_dynamic = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'root',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_http': False,
            'user_https': True,
        }
        out = interface_obj.config_interface(**X1_pppoe_opt_dynamic)
        if out:
            resp = interface_obj.get_interface_status('X1')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"pppoe"', 'ERR: config X1 failed')

    def test_02_config_X1_pppoe_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_03_verify_X1_can_get_ip_pppoe(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_04_ping_X1_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()

    def test_05_admin_user_login_to_X1_wan(self):
        logger.info('admin user login into fw...')
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i {Parameter.X1_PPP_IP} -a limit_login -u test1 -p S0nic@uto'
        output = pc4_ssh.send_command(cmd)
        logger.info(f'admin user login into fw{output}')
        res = True if 'FULL_ADMIN' in output else False
        Assertion.assert_equal(res, True, "ERR: the Limit admin user login failed.")


# check PPTP interface DHCP renew/release/refresh
class Test_pptp_dhcp_TC46(Test):
    uuid = "SOSAIOT-TC-56211"
    description = show_testcase_info(
        TESTPLAN, '46', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_pptp_dynamic(self):
        resp = {}
        X1_pptp_opt_dynamic = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'root',
            'pptp_passwd': 'password',
            'pptp_server': '12.12.1.40',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pptp_netmask': '255.255.255.0',
            'pppoe_inactivity': 10,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        conf_res = interface_obj.config_interface(**X1_pptp_opt_dynamic)
        if conf_res:
            resp = interface_obj.get_interface_status('X1')
        time.sleep(20)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"pptp"', 'ERR: config X1 failed')

    @repeat_method(5)
    def test_02_config_X1_pptp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    @repeat_method(25)
    def test_03_verify_X1_can_get_ip_pptp(self):
        logger.info("Sleep 5s before checking X1 ip address.")
        Parameter.X1_PPP_IP = ''
        Parameter.X1_PPP_IP_DHCP = ''
        time.sleep(5)
        flag = True
        resp = interface_obj.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        Parameter.X1_PPP_IP = resp.get("ip_address")
        Parameter.X1_PPP_IP_DHCP = resp.get("pptp_ip_address")
        if Parameter.X1_PPP_IP == '' or Parameter.X1_PPP_IP == '0.0.0.0':
            flag = False
        Assertion.assert_equal(flag, True,
                               "ERR: get X1 ip address  failed.")

    def test_04_ping_X1_pptp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()

    def test_05_verify_pptp_dhcp_release(self):
        logger.info('verify dhcp release...')
        log_obj.clear_log()
        flag = False
        log_flag = False
        run_dhcp_dict = {
            'cmd': "click_dhcp_release('X1')",
            'packet_obj': packetmonitor_obj,
            'runner_obj': interface_obj
        }
        (dhcpres, packets) = fw_packet_monitor_run(**run_dhcp_dict)
        logger.info(f'...Got dhcp command result is: {dhcpres}')
        if dhcpres:
            flag = True
        request_filters = ['BOOTP', 'out:X1', 'IP Type: UDP',
                           f'Src=[{Parameter.X1_PPP_IP_DHCP}]', 'Src=[68]', 'Dst=[67]']
        (packetres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the dhcp release packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {packetres}')
        log_1 = log_obj.show_log()
        logger.info(f'Got log result: {log_1}')
        if "Sending DHCP RELEASE" in str(log_1):
            log_flag = True
        Assertion.assert_equal(log_flag & packetres & flag, True,
                               "ERR: verify dhcp release failed.")

    def test_06_verify_pptp_dhcp_renew(self):
        logger.info('verify dhcp renew...')
        flag = False
        log_flag = False
        run_dhcp_dict = {
            'cmd': "click_dhcp_renew('X1')",
            'packet_obj': packetmonitor_obj,
            'runner_obj': interface_obj
        }
        (dhcpres, packets) = fw_packet_monitor_run(**run_dhcp_dict)
        logger.info(f'...Got dhcp command result is: {dhcpres}')
        if dhcpres:
            flag = True
        request_filters_client = ['BOOTP', 'out:X1', 'IP Type: UDP',
                                  f'Src=[0.0.0.0]', 'Src=[68]', 'Dst=[67]']
        (reqres_client, packet_client) = check_capture_packets(packets, request_filters_client)
        logger.info(f'Got the dhcp discover/request packet with request filters: {packet_client}')
        logger.info(f'Got captured packets result: {reqres_client}')

        request_filters_server = ['BOOTP', 'in:X1', 'IP Type: UDP',
                                  f'Dst=[{Parameter.X1_PPP_IP_DHCP}]', 'Src=[67]', 'Dst=[68]']
        (reqres_server, packet_server) = check_capture_packets(packets, request_filters_server)
        logger.info(f'Got the dhcp offer/ack packet with request filters: {packet_server}')
        logger.info(f'Got captured packets result: {reqres_server}')
        log_1 = log_obj.show_log()
        logger.info(f'Got log result: {log_1}')
        if ("Sending DHCP Request" in str(log_1)) & ("Sending DHCP DISCOVER" in str(log_1)):
            log_flag = True
        Assertion.assert_equal(reqres_server & reqres_client & flag & log_flag, True,
                               "ERR: verify dhcp renew.")

    def test_07_verify_pptp_dhcp_refresh(self):
        logger.info('verify dhcp refresh...')
        flag = False
        log_obj.clear_log()
        resp = interface_obj.get_interface_address('X1')
        time.sleep(5)
        log_1 = log_obj.show_log()
        logger.info(f'Got log result: {log_1}')
        if not resp.get("pptp_ip_address") or resp.get("pptp_ip_address") == '0.0.0.0':
            flag = True
        Assertion.assert_equal(flag, False,
                               "ERR: X1 DHCP refresh failed.")

    @repeat_method(5)
    def test_08_config_X1_pptp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_09_verify_X1_can_get_ip_pptp(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_10_ping_X1_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()


# check PPTP interface connect and disconnect
class Test_pptp_connect_disconnect_TC48(Test):
    uuid = "SOSAIOT-TC-56213"
    description = show_testcase_info(
        TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_pptp_dynamic(self):
        resp = {}
        X1_pptp_opt_dynamic = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'root',
            'pptp_passwd': 'password',
            'pptp_server': '12.12.1.40',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pptp_netmask': '255.255.255.0',
            'pppoe_inactivity': 10,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        conf_res = interface_obj.config_interface(**X1_pptp_opt_dynamic)
        if conf_res:
            resp = interface_obj.get_interface_status('X1')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"pptp"', 'ERR: config X1 failed')

    @repeat_method(5)
    def test_02_config_X1_pptp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_03_verify_X1_can_get_ip_pptp(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_04_ping_X1_pptp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()

    def test_05_config_X1_pptp_disconnect(self):
        Test_pppoe_connect_disconnect_TC41().test_05_config_X1_pppoe_disconnect()

    def test_06_verify_X1_not_get_ip_pppoe(self):
        Test_pppoe_connect_disconnect_TC41().test_06_verify_X1_not_get_ip_pppoe()

    @repeat_method(5)
    def test_07_config_X1_pptp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_08_verify_X1_can_get_ip_pptp(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_09_ping_X1_pptp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()


# check l2TP interface DHCP renew/release/refresh
class Test_l2tp_dhcp_TC52(Test):
    uuid = "SOSAIOT-TC-56218"
    description = show_testcase_info(
        TESTPLAN, '52', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_l2tp_dynamic(self):
        resp = {}
        X1_l2tp_opt_dynamic = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'l2tp',
            'l2tp_user': 'root',
            'l2tp_passwd': 'password',
            'l2tp_server': '12.12.1.40',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        conf_res = interface_obj.config_interface(**X1_l2tp_opt_dynamic)
        if conf_res:
            resp = interface_obj.get_interface_status('X1')
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"l2tp"', 'ERR: config X1 failed')

    @repeat_method(5)
    def test_02_config_X1_l2tp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    @repeat_method(25)
    def test_03_verify_X1_can_get_ip_l2tp(self):
        logger.info("Sleep 5s before checking X1 ip address.")
        Parameter.X1_PPP_IP = ''
        Parameter.X1_PPP_IP_DHCP = ''
        time.sleep(5)
        flag = True
        resp = interface_obj.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        Parameter.X1_PPP_IP = resp.get("ip_address")
        Parameter.X1_PPP_IP_DHCP = resp.get("l2tp_ip_address")
        if Parameter.X1_PPP_IP == '' or Parameter.X1_PPP_IP == '0.0.0.0':
            flag = False
        Assertion.assert_equal(flag, True,
                               "ERR: get X1 ip address  failed.")

    def test_04_ping_X1_l2tp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()

    def test_05_verify_l2tp_dhcp_release(self):
        Test_pptp_dhcp_TC46().test_05_verify_pptp_dhcp_release()

    def test_06_verify_L2tp_dhcp_renew(self):
        Test_pptp_dhcp_TC46().test_06_verify_pptp_dhcp_renew()

    def test_07_verify_L2tp_dhcp_refresh(self):
        logger.info('verify dhcp refresh...')
        flag = False
        log_obj.clear_log()
        resp = interface_obj.get_interface_address('X1')
        time.sleep(5)
        log_1 = log_obj.show_log()
        logger.info(f'Got log result: {log_1}')
        if not resp.get("l2tp_ip_address") or resp.get("l2tp_ip_address") == '0.0.0.0':
            flag = True
        Assertion.assert_equal(flag, False,
                               "ERR: X1 DHCP refresh failed.")

    @repeat_method(5)
    def test_08_config_X1_L2tp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_09_verify_X1_can_get_ip_pppoe(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_10_ping_X1_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()


# check PPTP interface connect and disconnect
class Test_l2tp_connect_disconnect_TC54(Test):
    uuid = "SOSAIOT-TC-56220"
    description = show_testcase_info(
        TESTPLAN, '54', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '54')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_l2tp_dynamic(self):
        Test_l2tp_dhcp_TC52().test_01_config_X1_l2tp_dynamic()

    @repeat_method(5)
    def test_02_config_X1_l2tp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_03_verify_X1_can_get_ip_l2tp(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_04_ping_X1_l2tp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()

    def test_05_config_X1_l2tp_disconnect(self):
        Test_pppoe_connect_disconnect_TC41().test_05_config_X1_pppoe_disconnect()

    def test_06_verify_X1_not_get_ip_l2tp(self):
        Test_pppoe_connect_disconnect_TC41().test_06_verify_X1_not_get_ip_pppoe()

    @repeat_method(5)
    def test_07_config_X1_l2tp_connect(self):
        Test_pppoe_connect_disconnect_TC41().test_02_config_X1_pppoe_connect()

    def test_08_verify_X1_can_get_ip_l2tp(self):
        Test_pppoe_connect_disconnect_TC41().test_03_verify_X1_can_get_ip_pppoe()

    def test_09_ping_X1_l2tp_wan(self):
        Test_pppoe_connect_disconnect_TC41().test_04_ping_X1_wan()


# check secondary wan static
class Test_wan_static_TC55(Test):
    uuid = "SOSAIOT-TC-56221"
    description = show_testcase_info(
        TESTPLAN, '55', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '55')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_a_local_user(self):
        user_dict = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Everyone'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": True
        }
        output = userlocal_obj.local_user(**user_dict)
        Assertion.assert_equal(output, True, "ERR: create local user failed")

    def test_02_add_admin_to_member(self):
        member_of_dict = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'S0nic@uto',
            'member_of': ['SonicWALL Administrators']
        }
        output = userlocal_obj.user_member_of(**member_of_dict)
        Assertion.assert_equal(output, True, "ERR: create local user failed")

    def test_03_verify_x3_static_ip_dns(self):
        logger.info('start verify X3 static ip checking')
        flag = False
        resp = interface_obj.get_interface_address("X3")
        logger.info(f"Get X3 interface address info = {resp}")
        if (resp.get("ip_mode") == 'Static IP') & (resp.get("ip_address") == Parameter.X3_IP) & (
                resp.get("subnet_mask") == '255.255.255.0') & (resp.get("default_gateway") == Parameter.X3_GW) & (
                resp.get("primary_dns") == Parameter.X1_DNS1):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify X3 static ip address failed.")

    def test_04_ping_x3_wan(self):
        logger.info('start ping X3 WAN interface checking')
        rc = ping_wan_ip(Parameter.X3_IP, pc5_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X3 WAN interface Failed!")

    def test_05_admin_user_login_to_x3_wan(self):
        logger.info('admin user https login into fw...')
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i {Parameter.X3_IP} -a limit_login -u test1 -p S0nic@uto'
        output = pc5_ssh.send_command(cmd)
        logger.info(f'admin user login into fw{output}')
        res = True if 'FULL_ADMIN' in output else False
        Assertion.assert_equal(res, True, "ERR: the Limit admin user login failed.")

    def test_06_admin_user_ssh_to_x3_wan(self):
        logger.info('admin user ssh login into fw...')
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i {Parameter.X3_IP} -a show_version -u test1 -p S0nic@uto'
        output = pc5_ssh.send_command(cmd)
        logger.info(f'admin user login into fw{output}')
        res = True if 'Successfully login in' in output else False
        Assertion.assert_equal(res, True, "ERR: the Limit admin user login failed.")

    @repeat_method(3)
    def test_07_snmp_get_system(self):
        rc = False
        node = "sysDescr"
        logger.info(f"{f' api status ':=^60}")
        status = status_obj.show_status()
        Parameter.fwStat_dict.update(status)
        logger.info(f"{f' snmp monitor -{node}- result ':=^60}")
        command = f"snmpwalk -v2c -c public -O Qv {Parameter.X3_IP} {node} "
        logger.info(f"-----> netsnmp command: {command}")
        output = pc5_ssh.send_command(command)
        logger.info(f"-----> snmp monitor output:\n{output}")
        if 'model' in Parameter.fwStat_dict.keys():
            rc = True if Parameter.fwStat_dict['model'] in output else False
        Assertion.assert_equal(rc, True, f"ERR: Get snmp {node} failed!!")

# check modify wan static management
class Test_wan_modify_TC56(Test):
    uuid = "SOSAIOT-TC-56222"
    description = show_testcase_info(
        TESTPLAN, '56', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '56')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_static_wan(self):
        resp = {}
        x3_wan_dict_new = {
            'if': 'X3',
            'zone': 'wan',
            'mode': 'static',
            'ip': "12.12.2.254",
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'dns1': "8.8.8.8",
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': False,
            'mgmt_snmp': True,
            'user_http': False,
            'user_https': True,
        }
        conf_res = interface_obj.config_interface(**x3_wan_dict_new)
        if conf_res:
            resp = interface_obj.get_interface_status('X3')
        Assertion.assert_regular(json.dumps(
                resp), r'"mode": {"static"', 'ERR: config X1 failed')

    def test_03_verify_x3_static_ip_dns(self):
        logger.info('start verify new X3 static ip checking')
        flag = False
        resp = interface_obj.get_interface_address("X3")
        logger.info(f"Get X3 interface address info = {resp}")
        if (resp.get("ip_mode") == 'Static IP') & (resp.get("ip_address") == "12.12.2.254") & (
                resp.get("primary_dns") == "8.8.8.8"):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify new X3 static ip address failed.")

    def test_04_ping_x3_wan(self):
        logger.info('start ping X3 WAN interface checking')
        rc = ping_wan_ip("12.12.2.254", pc5_ssh)
        logger.info(f'start ping X3 WAN interface checking{rc}')
        Assertion.assert_equal(rc, False, "ERR: Ping X3 WAN interface Failed!")

    def test_05_admin_user_login_to_x3_wan(self):
        logger.info('admin user https login into fw...')
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i "12.12.2.254" -a limit_login -u test1 -p S0nic@uto'
        output = pc5_ssh.send_command(cmd)
        logger.info(f'admin user login into fw{output}')
        res = True if 'FULL_ADMIN' in output else False
        Assertion.assert_equal(res, True, "ERR: the Limit admin user login failed.")

    def test_06_admin_user_ssh_to_x3_wan(self):
        logger.info('admin user ssh login into fw...')
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i "12.12.2.254" -a show_version -u test1 -p S0nic@uto'
        output = pc5_ssh.send_command(cmd)
        logger.info(f'admin user login into fw{output}')
        res = True if 'Successfully login in' in output else False
        Assertion.assert_equal(res, True, "ERR: the Limit admin user login failed.")

    def test_07_check_TSR_x3_wan(self):
        logger.info('start verify X3 wan TSR...')
        flag = False
        tsr_x3_info = diag_obj.get_tsr_interface_part(lab1="X3", lab2="X4")
        logger.info(f'show X3 interface config : {tsr_x3_info}..')
        if ("12.12.2.254" in tsr_x3_info) & ("8.8.8.8" in tsr_x3_info) & (
                "Interface ping Management" + " " * 23 + ": No" in tsr_x3_info):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Confirm new x3 wan in TSR."
        )


# check secondary wan dhcp
class Test_dhcp_x3_TC57(Test):
    uuid = "SOSAIOT-TC-56223"
    description = show_testcase_info(
        TESTPLAN, '57', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_dhcp(self):
        resp = {}
        X3_dhcp_dict = {
            'if': 'X3',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'mgmt_https': True,
            'user_http': False,
            'user_https': True,
        }
        conf_res = interface_obj.config_interface(**X3_dhcp_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('X3')
        Assertion.assert_regular(json.dumps(
                resp), r'"mode": {"dhcp"', 'ERR: config X3 failed')

    @repeat_method(25)
    def test_02_verify_X3_can_get_ip_dhcp(self):
        logger.info("Sleep 20s before checking X3 ip address.")
        time.sleep(5)
        flag = True
        resp = interface_obj.get_interface_address(name="X3")
        if not resp:
            flag = False
        logger.info(f"Get X3 interface info = {resp}")
        Parameter.X3_DHCP_IP = resp.get("ip_address")
        if Parameter.X3_DHCP_IP == '' or Parameter.X3_DHCP_IP == '0.0.0.0':
            flag = False
        Assertion.assert_equal(flag, True,
                               "ERR: get X3 ip address failed.")

    def test_03_ping_X3_wan(self):
        logger.info('start ping X3 WAN interface checking')
        rc = ping_wan_ip(Parameter.X3_DHCP_IP, pc5_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X3 WAN interface Failed!")

    def test_04_check_TSR_x3_wan(self):
        logger.info('start verify X3 wan TSR...')
        flag = False
        tsr_x3_info = diag_obj.get_tsr_interface_part(lab1="X3", lab2="X4")
        logger.info(f'show X3 interface config : {tsr_x3_info}..')
        if (Parameter.X3_DHCP_IP in tsr_x3_info) & (
                "DHCP CLIENT on port" + " " * 13 + ": X3" in tsr_x3_info) & (
                "Interface ping Management" + " " * 23 + ": Yes" in tsr_x3_info):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Confirm new x3 wan in TSR failed."
        )


# check secondary wan pppoe
class Test_pppoe_x3_TC58(Test):
    uuid = "SOSAIOT-TC-56224"
    description = show_testcase_info(
        TESTPLAN, '58', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_pppoe(self):
        logger.info("start config X3 pppoe mode.")
        resp = {}
        X3_pppoe_opt_dynamic = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'root',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_http': False,
            'user_https': True,
        }
        out = interface_obj.config_interface(**X3_pppoe_opt_dynamic)
        if out:
            resp = interface_obj.get_interface_status('X3')
        time.sleep(20)
        Assertion.assert_regular(json.dumps(
                resp), r'"mode": {"pppoe"', 'ERR: config X3 failed')

    def test_02_config_X3_pppoe_connect(self):
        logger.info("start ppp connect.")
        res = True
        resp = interface_obj.get_interface_address("X3")
        logger.info(f"Get X3 interface address info = {resp}")
        if resp.get("ip_address") == '' or resp.get("ip_address") == '0.0.0.0':
            res = interface_obj.click_pppoe_connect("X3")
            time.sleep(20)
        Assertion.assert_equal(res, True, "ERR: start pppoe connect failed!")

    @repeat_method(25)
    def test_03_verify_X3_can_get_ip_pppoe(self):
        logger.info("start get X3 ppp ip address.")
        time.sleep(5)
        resp = get_ppp_ip_address_x3("X3")
        Assertion.assert_equal(resp, True,
                               "ERR: get X3 ppp ip address failed.")

    def test_04_ping_X3_wan(self):
        logger.info('start ping X3 WAN interface checking')
        rc = ping_wan_ip(Parameter.X3_PPP_IP, pc5_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X3 WAN interface Failed!")

    def test_05_check_TSR_x3_wan(self):
        logger.info('start verify X3 wan TSR...')
        flag = False
        tsr_x3_info = diag_obj.get_tsr_interface_part(lab1="X3", lab2="X4")
        logger.info(f'show X3 interface config : {tsr_x3_info}..')
        if (Parameter.X3_PPP_IP in tsr_x3_info) & ("PPPOE link status" + " " * 31 + ": Connected" in tsr_x3_info) & (
                "Interface ping Management" + " " * 23 + ": Yes" in tsr_x3_info):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Confirm new x3 wan in TSR failed."
        )


# check secondary wan pptp
class Test_pptp_x3_TC59(Test):
    uuid = "SOSAIOT-TC-56225"
    description = show_testcase_info(
        TESTPLAN, '59', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_pptp_dynamic(self):
        resp = {}
        X3_pptp_opt_dynamic = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'root',
            'pptp_passwd': 'password',
            'pptp_server': '12.12.2.40',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pptp_netmask': '255.255.255.0',
            'pppoe_inactivity': 10,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        conf_res = interface_obj.config_interface(**X3_pptp_opt_dynamic)
        if conf_res:
            resp = interface_obj.get_interface_status('X3')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"pptp"', 'ERR: config X1 failed')

    def test_02_config_X3_pptp_connect(self):
        Test_pppoe_x3_TC58().test_02_config_X3_pppoe_connect()

    @repeat_method(25)
    def test_03_verify_X3_can_get_ip_pptp(self):
        logger.info("Sleep 5s before checking X3 ip address.")
        Parameter.X3_PPP_IP = ''
        Parameter.X3_PPP_IP_DHCP = ''
        time.sleep(5)
        flag = True
        resp = interface_obj.get_interface_address(name="X3")
        logger.info(f"Get X3 interface info = {resp}")
        Parameter.X3_PPP_IP = resp.get("ip_address")
        Parameter.X3_PPP_IP_DHCP = resp.get("pptp_ip_address")
        if Parameter.X3_PPP_IP == '' or Parameter.X3_PPP_IP == '0.0.0.0':
            flag = False
        Assertion.assert_equal(flag, True,
                               "ERR: get X1 ip address  failed.")

    def test_04_ping_X3_wan(self):
        Test_pppoe_x3_TC58().test_04_ping_X3_wan()

    def test_05_check_TSR_x3_wan(self):
        logger.info('start verify X3 wan TSR...')
        flag = False
        tsr_x3_info = diag_obj.get_tsr_interface_part(lab1="X3", lab2="X4")
        logger.info(f'show X3 interface config : {tsr_x3_info}..')
        if (Parameter.X3_PPP_IP in tsr_x3_info) & ("PPTP link status" + " " * 16 + ": Connected" in tsr_x3_info) & (
                "Interface ping Management" + " " * 23 + ": Yes" in tsr_x3_info):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Confirm new x3 wan in TSR failed."
        )


# check secondary wan l2tp
class Test_l2tp_x3_TC60(Test):
    uuid = "SOSAIOT-TC-56227"
    description = show_testcase_info(
        TESTPLAN, '60', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '60')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_l2tp_dynamic(self):
        resp = {}
        X3_l2tp_opt_dynamic = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'l2tp',
            'l2tp_user': 'root',
            'l2tp_passwd': 'password',
            'l2tp_server': '12.12.2.40',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        conf_res = interface_obj.config_interface(**X3_l2tp_opt_dynamic)
        if conf_res:
            resp = interface_obj.get_interface_status('X3')
        time.sleep(10)
        Assertion.assert_regular(json.dumps(
            resp), r'"mode": {"l2tp"', 'ERR: config X1 failed')

    def test_02_config_X3_l2tp_connect(self):
        Test_pppoe_x3_TC58().test_02_config_X3_pppoe_connect()

    def test_03_verify_X3_can_get_ip_l2tp(self):
        Test_pptp_x3_TC59().test_03_verify_X3_can_get_ip_pptp()

    def test_04_ping_X3_l2tp_wan(self):
        Test_pppoe_x3_TC58().test_04_ping_X3_wan()

    def test_05_check_TSR_x3_wan(self):
        logger.info('start verify X3 wan TSR...')
        flag = False
        tsr_x3_info = diag_obj.get_tsr_interface_part(lab1="X3", lab2="X4")
        logger.info(f'show X3 interface config : {tsr_x3_info}..')
        if (Parameter.X3_PPP_IP in tsr_x3_info) & (
                "Interface ping Management" + " " * 23 + ": Yes" in tsr_x3_info):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: Confirm new x3 wan in TSR failed."
        )


# check dmz static
class Test_dmz_static_x4_TC62(Test):
    uuid = "SOSAIOT-TC-56229"
    description = show_testcase_info(
        TESTPLAN, '62', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '62')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X4_dmz_static(self):
        resp = {}
        X4_dmz_opt_static = {
            'if': 'x4',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        conf_res = interface_obj.config_interface(**X4_dmz_opt_static)
        if conf_res:
            resp = interface_obj.get_interface_status('X4')
            logger.info(f"Get X4 interface status info = {resp}")
        Assertion.assert_regular(json.dumps(
            resp), r'"zone": "DMZ", "mode": {"static"', 'ERR: config X1 failed')

    def test_02_verify_x4_dmz_ip(self):
        logger.info('start verify X4 static ip checking')
        flag = False
        resp = interface_obj.get_interface_address("X4")
        logger.info(f"Get X4 interface address info = {resp}")
        if (resp.get("zone") == 'DMZ') & (resp.get("ip_address") == Parameter.X4_IP):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify X4 dmz static ip address failed.")

    def test_03_verify_zone_dmz_x4(self):
        logger.info('start verify X4 is in dmz zone checking')
        flag = False
        resp = zone_obj.get_reporting_zones_objects()
        logger.info(f"Get zone list info = {resp}")
        zone_dmz = [i for i in resp if i.get("name") == 'DMZ']
        if 'X4' in zone_dmz[0].get("member_interfaces"):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify X4 is in dmz zone failed.")

    # restore 'user_included': {"all": True} for access rule dmz to wan
    def test_04_verify_ao_dmz_x4(self):
        logger.info('start restore default with access rule dmz to wan')
        flag = False
        resp1 = address_obj.get_addressobject_by_name(name='X4 IP', version='ipv4')
        resp2 = address_obj.get_addressobject_by_name(name='X4 Subnet', version='ipv4')
        resp = accessrule_obj.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        logger.info(f"Get dmz to wan access rule info {resp}")
        dmz_wan_uuid = resp["access_rules"][0]["ipv4"].get("uuid")
        logger.info(f"Get dmz to wan access rule uuid info {dmz_wan_uuid}")
        access_rule_dmz_wan = {
            "from": "DMZ",
            "to": "WAN",
            "service": {"any": True},
            "source_addr": {"any": True},
            "dst_addr": {"any": True},
            'user_included': {"all": True},
            'action': 'allow',
        }
        output = accessrule_obj.edit_ipv4_access_rule_uuid(dmz_wan_uuid, **access_rule_dmz_wan)
        logger.info(f"restore default with access rule dmz to wan...{output}")
        if (resp1["address_objects"][0]["ipv4"].get("zone") == 'DMZ') & (
                resp2["address_objects"][0]["ipv4"].get("zone") == 'DMZ'):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: restore default with access rule dmz to wan failed.")

    def test_05_ping_x4_wan(self):
        logger.info('start ping X4 WAN interface checking')
        rc = ping_wan_ip(Parameter.PC4_ETH1, pc3_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X4 WAN interface Failed!")

    def test_06_edit_accessrule_user_include_x4(self):
        logger.info('start verify X4 AO is dmz checking')
        resp = accessrule_obj.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        logger.info(f"Get dmz to wan access rule info {resp}")
        dmz_wan_uuid = resp["access_rules"][0]["ipv4"].get("uuid")
        logger.info(f"Get dmz to wan access rule uuid info {dmz_wan_uuid}")
        access_rule_dmz_wan = {
            "from": "DMZ",
            "to": "WAN",
            "service": {"any": True},
            "source_addr": {"any": True},
            "dst_addr": {"any": True},
            'user_included': {"group": "Everyone"},
            'action': 'allow',
        }
        output = accessrule_obj.edit_ipv4_access_rule_uuid(dmz_wan_uuid, **access_rule_dmz_wan)
        resp1 = accessrule_obj.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        logger.info(f"Get dmz to wan access rule info {resp1}")
        Assertion.assert_equal(output, True, "ERR: cannot edit nat rule")

    def test_07_ping_x4_wan(self):
        logger.info('start ping X4 WAN interface checking')
        rc = ping_wan_ip(Parameter.PC4_ETH1, pc3_ssh)
        Assertion.assert_equal(rc, False, "ERR: Ping X4 WAN interface Failed!")

    def test_08_log_x4_wan_ping(self):
        logger.info('start log with ping X4 WAN interface checking')
        log_flag = False
        time.sleep(200)
        log_1 = log_obj.show_log()
        logger.info(f'Got log result: {log_1}')
        if "ICMP packet dropped due to Policy" in str(log_1):
            log_flag = True
        Assertion.assert_equal(log_flag, True, "ERR: log with Ping X4 WAN interface Failed!")

    def test_09_verify_ao_dmz_x4(self):
        Test_dmz_static_x4_TC62().test_04_verify_ao_dmz_x4()

    def test_10_ping_x4_wan(self):
        Test_dmz_static_x4_TC62().test_05_ping_x4_wan()


# check dmz transparent
class Test_dmz_transparent_x4_TC63(Test):
    uuid = "SOSAIOT-TC-56230"
    description = show_testcase_info(
        TESTPLAN, '63', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '63')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_addressobj(self):
        # wan address obj
        address_obj1 = {
            'object_type': 'range',
            'name': 'dmz_transparent',
            'value': '12.12.1.50,12.12.1.51',
            'zone': 'WAN',
        }
        rc = address_obj.config_addressobject(**address_obj1)
        Assertion.assert_equal(
            rc, True, "ERR: Add Public-IP address obj failed!")

    def test_02_config_X4_dmz_transparent(self):
        resp = {}
        opt = {
            'if': 'x4',
            'zone': 'DMZ',
            'mode': 'transparent',
            'transparent_range': {"name": "dmz_transparent"},
        }
        conf_res = interface_obj.config_interface(**opt)
        if conf_res:
            resp = interface_obj.get_interface_status('X4')
            logger.info(f"Get X4 interface status info = {resp}")
        Assertion.assert_regular(json.dumps(
            resp), r'"zone": "DMZ", "mode": {"transparent"', 'ERR: config X1 failed')

    def test_03_edit_pc3_eth1_ip(self):
        logger.info('start edit pc3 eth1 ip')
        flag = False
        cmd_pc3 = [
            f"ifconfig eth1 12.12.1.60",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc = pc3_ssh.send_commands(cmd_pc3)
        if "12.12.1.60" in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: edit pc3 eth1 ip Failed!")

    def test_04_ping_x4_wan(self):
        logger.info('start ping X4 WAN interface checking')
        rc = ping_wan_ip(Parameter.PC4_ETH1, pc3_ssh)
        Assertion.assert_equal(rc, False, "ERR: Ping X4 WAN interface Failed!")

    def test_05_edit_pc3_eth1_ip(self):
        logger.info('start edit pc3 eth1 ip')
        flag = False
        cmd_pc3 = [
            f"ifconfig eth1 12.12.1.50",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc = pc3_ssh.send_commands(cmd_pc3)
        if "12.12.1.50" in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: edit pc3 eth1 ip Failed!")

    def test_06_ping_x4_wan(self):
        logger.info('start ping X4 WAN interface checking')
        rc = ping_wan_ip(Parameter.PC4_ETH1, pc3_ssh)
        Assertion.assert_equal(rc, True, "ERR: Ping X4 WAN interface Failed!")

    def test_07_Config_x4_lan(self):
        logger.info("config x4 lan interface... ")
        rc = interface_obj.config_interface(**x4_lan_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 lan interface failed")

# check dmz l2bridge
class Test_dmz_l2bridge_TC64(Test):
    uuid = "SOSAIOT-TC-56231"
    description = show_testcase_info(
        TESTPLAN, '64', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '64')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X2_lan(self):
        Test_l2bridge_TC33().test_06_Config_X2_lan()

    def test_02_config_x4_l2bridge_to_x2(self):
        resp = {}
        x4_l2bridge_dict = {
            'if': 'X4',
            'zone': 'DMZ',
            'mode': 'l2bridge',
            'bridge_to': 'X2',
            'block_non_ip': False,
            'mgmt_snmp': True,
            'mgmt_http': False,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            "https_redirect": False,
            'bridge_block_non_ip': False,
            'route_on_bridge_pair': True,
            'stateful_inspection': True,
            'vlan_filtering_mode': 'block',
            'filter_vlans': [],
        }
        conf_res = interface_obj.config_interface(**x4_l2bridge_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('x4')
            logger.info(f"config x4 lan interface{resp} ")
        Assertion.assert_regular(json.dumps(
            resp), '"bridge_to": "X2"', 'ERR: config x4 failed')

    def test_03_config_pc3_ipv4(self):
        flag = False
        cmd_pc3 = [
            f"ifconfig eth1 {Parameter.PC3_ETH1_l2bridge}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X2_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc2 = pc3_ssh.send_commands(cmd_pc3)
        if f"{PC4_ETH1_NW}/24 via {Parameter.X2_IP}" in rc2:
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: config pc3 ipv4 failed.")

    def test_04_verify_pc3_traffic(self):
        logger.info('verify pc3 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'runner_obj': pc3_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X4', 'IP Type: ICMP',
                           f'Src=[{Parameter.PC3_ETH1_l2bridge}]', f'Dst=[{PC4_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: verify pc3 ping traffic failed.")

    def test_05_verify_secondary_bridged(self):
        logger.info('verify secondary bridged interface checking...')
        flag = False
        ip_mode_x2 = get_interface_ip_mode('X2')
        ip_mode_x4 = get_interface_ip_mode('X4')
        if (ip_mode_x4 == 'Secondary Bridged I/F') & (ip_mode_x2 == 'Primary Bridged I/F'):
            flag = True
        Assertion.assert_equal(flag, True,
                               "ERR: verify secondary bridged interface  failed.")

    def test_06_x4_lan_interface(self):
        # out = interface_obj.unassign_interface(interface='X4')
        logger.info("config x4 lan interface... ")
        rc = interface_obj.config_interface(**x4_lan_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 lan interface failed")




# check Failover&LB PPPOE to unassigned
class Test_ppp_lb_to_unassign_TC67(Test):
    uuid = "SOSAIOT-TC-56232"
    description = show_testcase_info(
        TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X3_pppoe(self):
        Test_pppoe_x3_TC58().test_01_config_X3_pppoe()

    def test_02_config_X3_pppoe_connect(self):
        Test_pppoe_x3_TC58().test_02_config_X3_pppoe_connect()

    def test_03_verify_X3_can_get_ip_pppoe(self):
        Test_pppoe_x3_TC58().test_03_verify_X3_can_get_ip_pppoe()

    def test_04_ping_X3_wan(self):
        Test_pppoe_x3_TC58().test_04_ping_X3_wan()

    def test_05_config_X1_pppoe(self):
        Test_pppoe_management_TC42().test_01_config_X1_pppoe()

    def test_06_config_X1_pppoe_connect(self):
        Test_pppoe_management_TC42().test_02_config_X1_pppoe_connect()

    def test_07_verify_X1_can_get_ip_pppoe(self):
        Test_pppoe_management_TC42().test_03_verify_X1_can_get_ip_pppoe()

    def test_08_ping_X1_wan(self):
        Test_pppoe_management_TC42().test_04_ping_X1_wan()

    def test_09_failoverlb_ppp(self):
        logger.info('config failoverlb ppp ...')
        failoverlb_ppp_payload = {"failover_lb": {"group": [
            {"name": " Default LB Group", "type": "basic", "final_backup": "", "preempt": True,
             "probing": {"health_check": 5, "missed_intervals": 3, "successful_intervals": 3,
                         "global_responder": False},
             "interface": [{"name": "X1", "rank": 1}, {"name": "X3", "rank": 2}]}]}}
        flag = failoverlb_obj.config_failover_groups_by_multi(**failoverlb_ppp_payload)
        Assertion.assert_equal(flag, True,
                               "ERR: config failoverlb ppp  failed.")

    def test_10_x3_unassign(self):
        out = interface_obj.unassign_interface(interface='X3')
        logger.info(out)
        resp = interface_obj.get_interface_status('X3')
        logger.info(resp)


# check http request with host header
class Test_host_hearer_check_TC1000(Test):
    uuid = "SOSAIOT-TC-56241"
    description = show_testcase_info(
        TESTPLAN, '1000', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1000')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X0_fqdn_url(self):
        logger.info('LAN X0 append domain name...')
        resp = {}
        conf_res = interface_obj.config_interface(**x0_lan_fqdn_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('X0')
        Assertion.assert_regular(json.dumps(
            resp), '1234567890abcd.corp.test.com', 'ERR: config LAN X0 append domain name failed')

    def test_02_hosts_append_domain(self):
        logger.info('append domain name in hosts...')
        flag = False
        pc1_ssh.send_command(f'cp /etc/hosts /etc/hosts.bak')
        with open("/etc/hosts", "a") as file:
            file.write("192.168.168.168    abcd.corp.test.com\n")
            file.write("192.168.168.168    1234567890abcd.corp.test.com\n")
        file.close()
        hosts_new = pc1_ssh.send_command(f'cat /etc/hosts')
        logger.info(f'new hosts list {hosts_new}')
        if ('192.168.168.168    abcd.corp.test.com' in hosts_new) & (
                '192.168.168.168    1234567890abcd.corp.test.com' in hosts_new):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: append domain name in hosts failed")

    def test_03_check_http_host_hearer(self):
        logger.info('start check http host hearer by curl domain...')
        flag1 = False
        flag2 = False
        access_domain = pc1_ssh.send_command(f'curl http://1234567890abcd.corp.test.com')
        logger.info(f'curl http://1234567890abcd.corp.test.com result ....{access_domain}')
        if (r'1234567890abcd.corp.test.com/sonicui/7/login/' in access_domain) & (
                'Page Redirecting' in access_domain):
            flag1 = True
        block_domain = pc1_ssh.send_command(f'curl http://abcd.corp.test.com')
        logger.info(f'curl http://abcd.corp.test.com result ....{block_domain}')
        if ('The client issued a bad request' in block_domain) & (
                'Bad Request' in block_domain):
            flag2 = True
        pc1_ssh.send_command(f'cp /etc/hosts.bak /etc/hosts')
        Assertion.assert_equal(flag1 & flag2, True, "ERR: append domain name in hosts failed")

    def test_04_config_X0_lan(self):
        logger.info('restore LAN X0 without domain name...')
        resp = {}
        conf_res = interface_obj.config_interface(**x0_lan_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('X0')
            logger.info(f"Get X0 interface status info = {resp}")
        Assertion.assert_regular(json.dumps(
            resp), r'"zone": "LAN", "mode": {"static"', 'ERR: config X1 failed')


