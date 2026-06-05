import json
from definition.settings import *
from definition.utils import *


# Excepted: The remote VPN host cannot access the Web server on the local LAN.
class TestTC01_Deny_http_service_on_incoming_traffic_to_the_lan_zone(Test):
    uuid = "SOSAIOT-TC-54624"
    description = show_testcase_info(TESTPLAN, 'tc01', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_verify_http_traffic_from_remote_to_local_lan_zone_pc2_eth1_before_add_deny_accessrule(self):
        output = PC3_Login.send_command(f'curl --connect-timeout 5  http://{PC2_ETH1_IP}')
        logger.info(f'output is:{output}')
        flag = True if "auto_vpn_access_test_tag" in output else False
        Assertion.assert_equal(flag, True, "ERR: check http traffic failed")

    def test_03_add_deny_access_rule_from_vpn_host_to_lan_http_server(self):
        res = accessruleapi.add_accessrule(**accessrule_dict)
        Assertion.assert_equal(res, True, "ERR: add deny access rule failed")

    def test_04_verify_http_traffic_from_remote_to_local_lan_zone_pc2_eth1_after_add_deny_accessrule(self):
        output = PC3_Login.send_command(f'curl --connect-timeout 5 http://{PC2_ETH1_IP}')
        logger.info(f'output is:{output}')
        flag = True if f"Failed to connect to {PC2_ETH1_IP} port 80" in output else False
        Assertion.assert_equal(flag, True, "ERR: verify http traffic failed")

    def test_05_delete_custom_deny_access_rule(self):
        res = accessruleapi.delete_accessrule_by_name('vpnhost_httpserver')
        Assertion.assert_equal(res, True, "ERR: delete custom deny access rule failed")


# Excepted: The remote VPN host cannot access the Web server on the local dmz.
class TestTC13_Deny_http_service_on_incoming_traffic_to_the_dmz_zone(Test):
    uuid = "SOSAIOT-TC-54625"
    description = show_testcase_info(TESTPLAN, 'tc13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_x2_from_lan_zone_to_dmz_zone(self):
        edit_x2_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**edit_x2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to dmz zone failed")

    @repeat_method(2)
    def test_03_check_local_and_remote_vpn_status(self):
        time.sleep(10)
        (res1, status1) = vpnbasesettingapi.get_vpn_status('localvpn')
        (res2, status2) = r_vpnbasesettingapi.get_vpn_status('remotevpn')
        logger.info(f'local vpn status:{res1},{status1},remote vpn status is:{res2},{status2}')
        flag = True if (res1 and res2) and (status1 == 'up' and status2 == 'up') else False
        Assertion.assert_equal(flag, True, "ERR: check local and remote vpn failed.")

    def test_04_verify_http_traffic_from_remote_to_local_lan_zone_pc2_eth1_before_add_deny_accessrule(self):
        output = PC3_Login.send_command(f'curl http://{PC2_ETH1_IP}')
        logger.info(f'output is:{output}')
        flag = True if "auto_vpn_access_test_tag" in output else False
        Assertion.assert_equal(flag, True, "ERR: verify http traffic failed")

    def test_05_add_deny_access_rule_from_vpn_host_to_dmz_http_server(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["to"] = "DMZ"
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add deny access rule failed")

    def test_06_verify_http_traffic_from_remote_to_local_lan_zone_pc2_eth1_after_add_deny_accessrule(self):
        output = PC3_Login.send_command(f'curl http://{PC2_ETH1_IP}')
        logger.info(f'output is:{output}')
        flag = True if f"Failed to connect to {PC2_ETH1_IP} port 80" in output else False
        Assertion.assert_equal(flag, True, "ERR: verify http traffic failed")

    def test_07_delete_custom_deny_access_rule(self):
        res = accessruleapi.delete_accessrule_by_name('vpnhost_httpserver')
        Assertion.assert_equal(res, True, "ERR: delete custom deny access rule failed")

    def test_08_change_x2_from_dmz_zone_to_lan_zone(self):
        edit_x2_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**edit_x2_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to lan zone failed")


# Excepted: The remote VPN host can connect to FTP server on the local LAN zone.
class TestTC03_Allow_ftp_service_on_incoming_traffic_to_the_LAN_zone(Test):
    uuid = "SOSAIOT-TC-54626"
    description = show_testcase_info(TESTPLAN, 'tc03', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_allow_access_rule_from_vpn_host_to_lan_ftp_server(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["action"] = "allow"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "vpnhost_ftpserver"
        rule_dict["access_rules"][0]["ipv4"]["service"] = {"name": "FTP"}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add access rule failed")

    def test_03_get_accessule_hit_time_in_tsr_before_send_ftp_traffic(self):
        getaccessrule = diagnosticapi.get_tsr_accessrule_part()
        # logger.info(f'getaccessrule is:{getaccessrule}')
        hittimebefore = get_accessrule_hit_time_in_tsr(getaccessrule, 'vpnhost_ftpserver')
        logger.info(f'hittimebefore is:{hittimebefore}')
        ParamCases.tc03hittimebefore = hittimebefore
        flag = True if hittimebefore else False
        Assertion.assert_equal(flag, True, "ERR: get custom accessrule hit time from tsr failed")

    def test_04_verify_ftp_traffic_from_remote_to_local_lan_zone_pc2_eth1(self):
        cmd = f'python3 {SCRIPTS_PATH}/get_file_via_ftp.py -host {PC2_ETH1_IP} -user root -pwd password'
        logger.info(f'start login pc via ftp cmd: {cmd}')
        loginoutput = PC3_Login.send_command(cmd)
        logger.info(f'loginoutput is:{loginoutput}')
        Assertion.assert_regular(loginoutput, '230 Login successful.', "ERR: verify ftp traffic failed.")

    def test_05_get_accessule_hit_time_in_tsr_after_send_ftp_traffic_and_check_if_hit_custom_accessrule(self):
        time.sleep(5)
        getaccessrule = diagnosticapi.get_tsr_accessrule_part()
        # logger.info(f'getaccessrule is:{getaccessrule}')
        hittimeafter = get_accessrule_hit_time_in_tsr(getaccessrule, 'vpnhost_ftpserver')
        logger.info(f'ParamCases.tc03hitimebefore is:{ParamCases.tc03hittimebefore}')
        logger.info(f'hittimeafter is:{hittimeafter}')
        flag = True if hittimeafter != ParamCases.tc03hittimebefore else False
        Assertion.assert_equal(flag, True, "ERR: get custom accessrule hit time from tsr and check hit custom "
                                           "accessrule failed")

    def test_06_delete_custom_deny_access_rule(self):
        res = accessruleapi.delete_accessrule_by_name('vpnhost_ftpserver')
        Assertion.assert_equal(res, True, "ERR: delete custom deny access rule failed")


# Excepted: The local LAN host cannot connect to the FTP server on the remote LAN.
class TestTC07_Deny_ftp_service_on_incoming_traffic_to_the_LAN_zone(Test):
    uuid = "SOSAIOT-TC-54627"
    description = show_testcase_info(TESTPLAN, 'tc07', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_deny_access_rule_from_vpn_host_to_lan_ftp_server(self):
        rule_dict = copy.deepcopy(accessrule_dict)
        rule_dict["access_rules"][0]["ipv4"]["action"] = "deny"
        rule_dict["access_rules"][0]["ipv4"]["name"] = "vpnhost_ftpserver"
        rule_dict["access_rules"][0]["ipv4"]["service"] = {"name": "FTP"}
        res = accessruleapi.add_accessrule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: add deny access rule failed")

    def test_03_get_accessule_hit_time_in_tsr_before_send_ftp_traffic(self):
        getaccessrule = diagnosticapi.get_tsr_accessrule_part()
        hittimebefore = get_accessrule_hit_time_in_tsr(getaccessrule, 'vpnhost_ftpserver')
        logger.info(f'hittimebefore is:{hittimebefore}')
        ParamCases.tc07hittimebefore = hittimebefore
        flag = True if hittimebefore else False
        Assertion.assert_equal(flag, True, "ERR: get custom accessrule hit time from tsr failed")

    def test_04_verify_ftp_traffic_from_remote_to_local_lan_zone_pc2_eth1(self):
        cmd = f'python3 {SCRIPTS_PATH}/get_file_via_ftp.py -host {PC2_ETH1_IP} -user root -pwd password'
        logger.info(f'start login pc via ftp cmd: {cmd}')
        loginoutput = PC3_Login.send_command(cmd)
        logger.info(f'loginoutput is:{loginoutput}')
        Assertion.assert_regular(loginoutput, 'Connection refused', "ERR: verify ftp traffic failed.")

    def test_05_get_accessule_hit_time_in_tsr_after_send_ftp_traffic_and_check_if_hit_custom_accessrule(self):
        time.sleep(5)
        getaccessrule = diagnosticapi.get_tsr_accessrule_part()
        hittimeafter = get_accessrule_hit_time_in_tsr(getaccessrule, 'vpnhost_ftpserver')
        logger.info(f'ParamCases.tc07hitimebefore is:{ParamCases.tc07hittimebefore}')
        logger.info(f'hittimeafter is:{hittimeafter}')
        flag = True if hittimeafter != ParamCases.tc07hittimebefore else False
        Assertion.assert_equal(flag, True, "ERR: get custom accessrule hit time from tsr and check hit custom "
                                           "accessrule failed")
