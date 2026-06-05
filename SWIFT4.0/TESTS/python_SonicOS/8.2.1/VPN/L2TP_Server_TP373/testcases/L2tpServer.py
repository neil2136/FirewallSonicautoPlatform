from definition.settings import *
from definition.utils import *


# L2TP server configuration
class Test_ServerConfig_TC04(Test):
    uuid = "SOSAIOT-TC-54481"
    description = show_testcase_info(
        TESTPLAN, '1507828', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507828')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_L2TP_Server(self):
        l2tpsettings_dict = {
            'enable': True,
            'ip_pool': 'local',
            'ippool_begin': '192.168.22.10',
            'ippool_end': '192.168.22.50',
            'user_group': 'Everyone'
        }
        l2tpconfigres = l2tpapi.config_l2tpserver(msg=False, **l2tpsettings_dict)
        logger.info(f"config L2TP Server: {l2tpconfigres}")
        Assertion.assert_equal(l2tpconfigres, True, "ERR: configure L2TP Server failed")

    def test_03_config_GroupVpn(self):
        groupvpnsettings_dict = {
            'enable': True,
            'secret': 'password',
            'auth_mode': 'shared_secret',
            'ike_encryption': 'triple-des',
            'ike_auth': 'sha-1',
            'ipsec_encryption': 'triple_des',
            'ike_lifetime': 240,
            'ipsec_auth': 'sha_1',
            'ipsec_lifetime': 240,
            'client_authentication': 'allow_unauthenticated',
            'unauthenticated_group': 'Firewalled Subnets',
            'management_https': True,
            'management_ssh': True,
        }
        configres = vpnapi.edit_wangroup_vpn_policy(**groupvpnsettings_dict)
        logger.info(f"config GroupVpn: {configres}")
        Assertion.assert_equal(configres, True, "ERR: configure WAN Group VPN failed")


# L2TP client behind NAT
class Test_BehindNAT_TC16(Test):
    uuid = "SOSAIOT-TC-54478"
    description = show_testcase_info(
        TESTPLAN, '1507825', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507825')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_start_L2TP_Client_and_check_traffic(self):
        logger.info("########start L2TP Client#######")
        startres = start_L2TP_Client(PC4_Login)
        time.sleep(5)
        rtcheckres = check_route(PC4_Login)
        logger.info(f"check route through PPP: {rtcheckres}")
        if rtcheckres:
            res = PC4_Login.ping(Parameter.FIREWALL)
        else:
            res = False
            logger.info(f"there are no routes to {Parameter.FIREWALL} through l2tp tunnel")
        Assertion.assert_equal(startres & res, True, "ERR: check l2tp session fail")

    def test_03_check_l2tp_session(self):
        CaseParams.client_ip_tc18_def03 = get_ppp_address(PC4_Login)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        filter_tuple = ['test1',  CaseParams.client_ip_tc18_def03, 'X1']
        checkres = [x in str(sessionres) for x in filter_tuple]
        logger.info(checkres)
        Assertion.assert_equal(all(checkres), True, "ERR: check l2tp session fail")

    def test_04_disconnect_L2TP_Client_from_server_side(self):
        l2tpapi.disconnect_l2tp_client(CaseParams.client_ip_tc18_def03)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        flag = False if sessionres else True
        Assertion.assert_equal(flag, True, "ERR: disconnect l2tp cient fail")


# Accessing the L2TP Server page when L2TP Client was connected by VLAN
class Test_VlanClient_TC18(Test):
    uuid = "SOSAIOT-TC-54479"
    description = show_testcase_info(
        TESTPLAN, '1507826', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507826')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_start_L2TP_Client_and_check_traffic(self):
        logger.info("########start L2TP Client#######")
        startres = start_L2TP_Client(PC3_Login)
        time.sleep(5)
        rtcheckres = check_route(PC3_Login)
        logger.info(f"check route through PPP: {rtcheckres}")
        if rtcheckres:
            res = PC3_Login.ping(Parameter.FIREWALL)
        else:
            res = False
            logger.info(f"there are no routes to {Parameter.FIREWALL} through l2tp tunnel")
        Assertion.assert_equal(startres & res, True, "ERR: check l2tp session fail")

    def test_03_check_l2tp_session(self):
        client_ip = get_ppp_address(PC3_Login)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        filter_tuple = ['test3', client_ip, 'X2:V' + str(X2_VLAN1_ID)]
        checkres = [x in str(sessionres) for x in filter_tuple]
        logger.info(checkres)
        Assertion.assert_equal(all(checkres), True, "ERR: check l2tp session fail")

    def test_04_login_to_FW_from_l2tp_client(self):
        cmd1 = [f'python3 {script_path}/ui_login_fw.py '
                f'-url https://{Parameter.X2_VLAN1_IP}/sonicui/7/m/mgmt/vpn/l2tp-server '
                f'-user test3 -pwd test3']
        res1 = PC3_Login.send_commands(cmd1)
        flag = True if 'Login fw successful' in str(res1) else False
        Assertion.assert_equal(flag, True, "ERR: login to FW from l2tp client fail")


# "Enable IP header checksum enforcement" is enabled, connect L2TP client
class Test_ChecksumEnforcement_TC19(Test):
    uuid = "SOSAIOT-TC-54480"
    description = show_testcase_info(
        TESTPLAN, '1507827', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1507827')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_IP_header_checksum_enforcement(self):
        firewall_dict = {
            'ip checksum_enforcement': True,
            'control_plane_flood_protection': False
        }
        res = firewalladvanceapi.config_advance(**firewall_dict)
        Assertion.assert_equal(res, True, 'ERR: "Enable IP header checksum enforcement" failed')

    def test_03_start_L2TP_Client(self):
        Test_VlanClient_TC18().test_02_start_L2TP_Client_and_check_traffic()

    def test_04_check_l2tp_session(self):
        Test_VlanClient_TC18().test_03_check_l2tp_session()


# Function: L2TP server enable and disable
class Test_EnableAndDisable_TC06(Test):
    uuid = "SOSAIOT-TC-54484"
    description = show_testcase_info(
        TESTPLAN, '2202248', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2202248')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_L2TP_Server(self):
        l2tpconfigres = l2tpapi.enable_or_disable_l2ptpserver(msg=False, enable=False)
        logger.info(f"config L2TP Server: {l2tpconfigres}")
        Assertion.assert_equal(l2tpconfigres, True, "ERR: disable L2TP Server failed")

    def test_03_check_l2tp_session(self):
        time.sleep(5)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        flag = False if sessionres else True
        Assertion.assert_equal(flag, True, "ERR: check l2tp session fail")

    def test_04_check_traffic(self):
        res = PC3_Login.ping(Parameter.FIREWALL)
        Assertion.assert_equal(res, False, "ERR: check l2tp session fail")

    def test_05_enable_L2TP_Server(self):
        l2tpconfigres = l2tpapi.enable_or_disable_l2ptpserver(msg=False, enable=True)
        logger.info(f"config L2TP Server: {l2tpconfigres}")
        Assertion.assert_equal(l2tpconfigres, True, "ERR: Enable L2TP Server failed")

    @repeat_method(5)
    def test_06_reconnect_L2TP_Client(self):
        Test_VlanClient_TC18().test_02_start_L2TP_Client_and_check_traffic()

    def test_07_check_l2tp_session(self):
        Test_VlanClient_TC18().test_03_check_l2tp_session()


# L2TP client connect and disconnect
class Test_ConnectAndDisconnect_TC07(Test):
    uuid = "SOSAIOT-TC-54485"
    description = show_testcase_info(
        TESTPLAN, '2202249', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2202249')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disconnect_L2TP_Client_from_client_side(self):
        connectcmds = [
            'echo "d myvpn" > /var/run/xl2tpd/l2tp-control',
            'sleep 5',
            'grep xl2tpd /var/log/messages | tail -5'
        ]
        connectres = PC3_Login.send_commands(connectcmds)
        flag = True if "closed to 12.12.3.168" in str(connectres) else False
        logger.info(f"check if L2TP disconnected: {flag}")
        Assertion.assert_equal(flag, True, "ERR: l2tp client disconnect fail")

    def test_03_check_l2tp_session(self):
        time.sleep(60)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        flag = False if sessionres else True
        Assertion.assert_equal(flag, True, "ERR: check l2tp session fail")

    def test_04_check_traffic(self):
        res = PC3_Login.ping(Parameter.FIREWALL)
        Assertion.assert_equal(res, False, "ERR: check l2tp session fail")

    @repeat_method(5)
    def test_05_connect_L2TP_Client(self):
        time.sleep(60)
        Test_VlanClient_TC18().test_02_start_L2TP_Client_and_check_traffic()

    def test_06_check_l2tp_session(self):
        CaseParams.client_ip_tc07_def06 = get_ppp_address(PC3_Login)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        filter_tuple = ['test3', CaseParams.client_ip_tc07_def06, 'X2:V' + str(X2_VLAN1_ID)]
        checkres = [x in str(sessionres) for x in filter_tuple]
        logger.info(checkres)
        Assertion.assert_equal(all(checkres), True, "ERR: check l2tp session fail")

    def test_07_disconnect_L2TP_Client_from_server_side(self):
        logger.info(CaseParams.client_ip_tc07_def06)
        l2tpapi.disconnect_l2tp_client(CaseParams.client_ip_tc07_def06)
        sessionres = l2tpapi.show_active_l2tp_server_section()
        flag = False if CaseParams.client_ip_tc07_def06 in sessionres else True
        Assertion.assert_equal(flag, True, "ERR: disconnect l2tp cient fail")

    def test_08_check_traffic(self):
        res = PC3_Login.ping(Parameter.FIREWALL)
        Assertion.assert_equal(res, False, "ERR: check l2tp session fail")

    @repeat_method(5)
    def test_09_connect_L2TP_Client(self):
        Test_VlanClient_TC18().test_02_start_L2TP_Client_and_check_traffic()

    def test_10_check_l2tp_session(self):
        Test_VlanClient_TC18().test_03_check_l2tp_session()





