from definition.settings import *
from definition.utils import *


# In Default Setting,Check DPI Tag in syslog when UDP traffic is "Connection Closed"
class TestAppRule_TC101(Test):
    uuid = "SOSAIOT-TC-54814"
    description = show_testcase_info(
        TESTPLAN, '1520001', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520001')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_udp_traffic(self):
        res = send_udp_traffic()
        Assertion.assert_equal(res, True, "ERR: send udp traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ('Connection Closed', 'udp/8080', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


#  In Default Setting,Only enable App Rules without entry,Check DPI Tag in syslog when HTTP traffic is "Connection Closed"
class TestAppRule_TC106(Test):
    uuid = "SOSAIOT-TC-54819"
    description = show_testcase_info(
        TESTPLAN, '1520006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520006')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ('http', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


# When App Control=0; App Rules=0 without entry; Open and close HTTPS connection , check DPI tag in syslog and GUI log
class TestAppRule_TC111(Test):
    uuid = "SOSAIOT-TC-54824"
    description = show_testcase_info(
        TESTPLAN, '1520011', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520011')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


 # When App Control=0; App Rules=0, Enable GAV/IPS/Anti-Spware. Open and close HTTPS connection, check DPI tag in syslog and GUI log
class TestAppRule_TC126(Test):
    uuid = "SOSAIOT-TC-54836"
    description = show_testcase_info(
        TESTPLAN, '1520026', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520026')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_gav(self):
        gav_params = {
            'enable_GAV': True,
        }
        rc = gav_api.config_gav(**gav_params)
        Assertion.assert_equal(rc, True, "ERR: config GAV in security service failed")

    def test_02_config_Anti_Spyware(self):
        res = spy_api.config_antispyware(**spy_params_d)
        Assertion.assert_equal(res, True, 'ERR: config anti spyware settings failed.')

    def test_03_enable_IPS(self):
        ips_global = {
            'intrusion_prevention': {
                'enable': True,
                'signature_group': {
                    'high_priority': {
                        'prevent_all': True,
                        'detect_all': True,
                        'log_redundancy': {}
                    },
                    'medium_priority': {
                        'prevent_all': False,
                        'detect_all': True,
                        'log_redundancy': {}
                    },
                    'low_priority': {
                        'prevent_all': False,
                        'detect_all': True,
                        'log_redundancy': {}
                    }
                }
            }
        }
        rc = ips_api.config_IPS_global(**ips_global)
        Assertion.assert_equal(rc, True, "ERR: enable ips failed")

    def test_04_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_05_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When CFS Enabled=0; Flow with URL, Open and close https connection , check message ID and confirm whether DPI tag is in syslog
class TestCFS_TC119(Test):
    uuid = "SOSAIOT-TC-54830"
    description = show_testcase_info(
        TESTPLAN, '1520019', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520019')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When CFS Enabled=0; Flow without URL, Open and close https connection , check message ID and confirm whether DPI tag is in syslog
class TestCFS_TC120(Test):
    uuid = "SOSAIOT-TC-54831"
    description = show_testcase_info(
        TESTPLAN, '1520020', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520020')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_configure_x2(self):
        x2_dict = {
            'if': 'x2',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        (rc1, msg1) = if_v4_api.config_interface(msg=True, **x2_dict)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Configure VLAN failed!")

    def test_03_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        cmd_list = ['route del default',
                    f'route add default gw {Parameter.X2_IP}',
                    'curl -v https://www.baidu.com']
        res = pc3_login.send_commands(cmd_list)
        Assertion.assert_regular(res, "baidu", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'https', PC3_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# In Default Setting,Only enable App Rules without entry,Check DPI Tag in syslog when UDP traffic is "Connection Closed"
class TestAppRule_TC102(Test):
    uuid = "SOSAIOT-TC-54815"
    description = show_testcase_info(
        TESTPLAN, '1520002', description=True)['title']
    res_for_test_tc123 = ContextVar('res_for_test_tc123')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520002')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_app_rule(self):
        app_dict = {
            'enable': True,
            'log_redundancy': {}
        }
        res = app_rule_api.config_apprule_setting(**app_dict)
        Assertion.assert_equal(res, True, 'ERR: enable app rule failed.')

    def test_02_send_udp_traffic(self):
        res = send_udp_traffic()
        Assertion.assert_equal(res, True, "ERR: send udp traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", 'Connection Closed', 'udp/8080', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        self.res_for_test_tc123.set(res)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


#  In Default Setting,Only enable App Rules without entry,Check DPI Tag in syslog when HTTP traffic is "Connection Closed"
class TestAppRule_TC107(Test):
    uuid = "SOSAIOT-TC-54820"
    description = show_testcase_info(
        TESTPLAN, '1520007', description=True)['title']
    res_for_test_tc124 = ContextVar('res_for_test_tc124')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520007')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_configure_syslog_server(self):
        syslog_dict = {
            'name': 'syslog_server',
            'format': 'enhanced-syslog',
            'profile': 0
        }
        res = syslog_api.edit_syslog_server(**syslog_dict)
        Assertion.assert_equal(res, True, "ERR: Config syslog setting failed")

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'http',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        self.res_for_test_tc124.set(res)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# In Default Setting,Enable App Rules and create entry,Check DPI Tag in syslog when UDP traffic is "Connection Closed"
class TestAppRule_TC103(Test):
    uuid = "SOSAIOT-TC-54816"
    description = show_testcase_info(
        TESTPLAN, '1520003', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520003')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_creat_match_object(self):
        res = match_api.config_matchobject(**match_obj_base)
        Assertion.assert_equal(res, True, 'ERR: creat match object failed.')

    def test_02_create_matched_app_rule(self):
        res = app_rule_api.add_apprule(**app_rule_base)
        Assertion.assert_equal(res, True, 'ERR: add matched app rule failed.')

    def test_03_send_udp_traffic(self):
        res = send_udp_traffic()
        Assertion.assert_equal(res, True, "ERR: send udp traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ('Connection Closed', 'udp/8080',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


#  In Default Setting,Enable App Rules and create entry,Check DPI Tag in syslog when HTTP traffic is "Connection Closed"
class TestAppRule_TC108(Test):
    uuid = "SOSAIOT-TC-54821"
    description = show_testcase_info(
        TESTPLAN, '1520008', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520008')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Recv failure: Connection reset by peer", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", 'http', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=0; App Rules=1 with entry, Open and close HTTPS connection , check DPI tag in syslog and GUI log
class TestAppRule_TC112(Test):
    uuid = "SOSAIOT-TC-54825"
    description = show_testcase_info(
        TESTPLAN, '1520012', description=True)['title']
    res_for_test_tc129 = ContextVar('res_for_test_tc129')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520012')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(
            f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(
            res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'https',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        self.res_for_test_tc129.set(res)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


# In Default Setting,Enable App Rules and create entry,Remove entry. Then check DPI Tag in syslog when UDP traffic is "Connection Closed"
class TestAppRule_TC104(Test):
    uuid = "SOSAIOT-TC-54817"
    description = show_testcase_info(
        TESTPLAN, '1520004', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520004')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_del_app_rule(self):
        res = app_rule_api.delete_apprule_object_byname('http')
        Assertion.assert_equal(res, True, 'ERR: del app rule failed.')

    def test_03_send_udp_traffic(self):
        res = send_udp_traffic()
        Assertion.assert_equal(res, True, "ERR: send udp traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ('Connection Closed', 'udp/8080',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)

        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")

# In Default Setting,Enable App Rules and create entry,Remove entry. Then check DPI Tag in syslog when HTTP traffic is "Connection Closed"


class TestAppRule_TC109(Test):
    uuid = "SOSAIOT-TC-54822"
    description = show_testcase_info(
        TESTPLAN, '1520009', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520009')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(
            res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'http',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")

#  Continue above test case, restart FW,check DPI Tag in syslog when UDP traffic is "Connection Closed"


class TestAppRule_TC105(Test):
    uuid = "SOSAIOT-TC-54818"
    description = show_testcase_info(
        TESTPLAN, '1520005', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520005')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_reboot(self):
        rc = setting_api.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    def test_02_send_udp_traffic(self):
        res = send_udp_traffic()
        Assertion.assert_equal(res, True, "ERR: send udp traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ('Connection Closed', 'udp/8080',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


# Continue above test case, restart FW,check DPI Tag in syslog when HTTP traffic is "Connection Closed"
class TestAppRule_TC110(Test):
    uuid = "SOSAIOT-TC-54823"
    description = show_testcase_info(
        TESTPLAN, '1520010', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520010')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(
            res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", "Connection Closed", 'http',
                        PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


#  When App Rules with one created entry =1,Select App Rule Entry's Exclusion Source AO to be LAN PC, Open and close HTTP connection ,check DPI tag in syslog and GUI log
class TestAppRule_TC117(Test):
    uuid = "SOSAIOT-TC-54828"
    description = show_testcase_info(
        TESTPLAN, '1520017', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520017')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_exclusion_list(self):
        logger.info('=> create a ao for exclusion list')
        ao_dict = {
            'object_type': 'host',
            'name': PC1_ETH2_IP,
            'zone': 'LAN',
            'value': PC1_ETH2_IP
        }
        add_ao_res = ao_api.config_addressobject(**ao_dict)
        logger.info(f'add address object result: {add_ao_res}')

        update_dict = {
            "name": "http",
            "exclusion": {"address": {"name": ao_dict['name']}, "service": {}},
        }
        app_rule_dict = copy.deepcopy(app_rule_base)
        app_rule_dict["app_rules"]["policy"][0].update(update_dict)
        res = app_rule_api.edit_app_rule("http", **app_rule_dict)
        Assertion.assert_equal(res, True, 'ERR: add matched app rule failed.')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(
            res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", 'http', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(
            res, True, "ERR: verify syslog on server failed.")


#  When App Rules with one created entry =1,Select App Rule Entry's Action Objects to be BYPASS DPI, Open and close HTTP connection ,check DPI tag in syslog and GUI log
class TestAppRule_TC118(Test):
    uuid = "SOSAIOT-TC-54829"
    description = show_testcase_info(
        TESTPLAN, '1520018', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520018')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_edit_app_rule(self):
        update_dict = {
            "name": "http",
            "exclusion": {"address": {}},
            "action_object": "Bypass DPI",
        }
        app_rule_dict = copy.deepcopy(app_rule_base)
        app_rule_dict["app_rules"]["policy"][0].update(update_dict)
        res = app_rule_api.edit_app_rule("http", **app_rule_dict)
        Assertion.assert_equal(res, True, 'ERR: add matched app rule failed.')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl {Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Welcome to Nginx", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("m=537", 'http', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; App Rules=1 with entry, Open and close HTTPS connection , check DPI tag in syslog and GUI log
class TestAppCtrl_TC114(Test):
    uuid = "SOSAIOT-TC-54827"
    description = show_testcase_info(
        TESTPLAN, '1520014', description=True)['title']
    res_for_test_tc125 = ContextVar('res_for_test_tc125')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520014')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_configure_syslog_server(self):
        syslog_dict = {
            'name': 'syslog_server',
            'format': 'arcSight',
            'profile': 0
        }
        res = syslog_api.edit_syslog_server(**syslog_dict)
        Assertion.assert_equal(res, True, "ERR: Config syslog setting failed")

    def test_02_config_app_control(self):
        logger.info('=> enable app control global')
        res = app_control_api.config_appcontrol_global_settings(**ac_global)
        Assertion.assert_equal(res, True, "ERR: config app control failed")

    def test_03_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        self.res_for_test_tc125.set(res)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; App Rules=0 without entry; Open and close HTTPS connection , check DPI tag in syslog and GUI log
class TestAppCtrl_TC113(Test):
    uuid = "SOSAIOT-TC-54826"
    description = show_testcase_info(
        TESTPLAN, '1520013', description=True)['title']
    res_for_test_tc127 = ContextVar('res_for_test_tc127')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520013')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_configure_syslog_server(self):
        syslog_dict = {
            'name': 'syslog_server',
            'format': 'webtrends',
            'profile': 0
        }
        res = syslog_api.edit_syslog_server(**syslog_dict)
        Assertion.assert_equal(res, True, "ERR: Config syslog setting failed")

    def test_02_disable_app_rule(self):
        app_dict = {
            'enable': False,
            'log_redundancy': {}
        }
        res = app_rule_api.config_apprule_setting(**app_dict)
        Assertion.assert_equal(res, True, 'ERR: disable app rule failed.')

    def test_03_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res = syslog_check(syslog_file, search_tuple)
        self.res_for_test_tc127.set(res)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When CFS Enabled=1; Flow with URL, Open and close https connection , check message ID and confirm whether DPI tag is in syslog
class TestCFS_TC121(Test):
    uuid = "SOSAIOT-TC-54832"
    description = show_testcase_info(
        TESTPLAN, '1520021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520021')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_content_filtering_service(self):
        cfs_settings_dict = {'enable': True}
        output = content_filter_api.edit_cfs_setting(**cfs_settings_dict)
        Assertion.assert_equal(output, True, "ERR: enable Content Filtering Service failed")

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple1 = ('https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=1')
        res1 = syslog_check(syslog_file, search_tuple1)
        Assertion.assert_equal(res1, True, "ERR: verify syslog on server failed.")

    def test_04_disable_content_filtering_service(self):
        cfs_settings_dict = {'enable': False}
        output = content_filter_api.edit_cfs_setting(**cfs_settings_dict)
        Assertion.assert_equal(output, True, "ERR: enable Content Filtering Service failed")


#  When CFS Enabled=1; Flow without URL, Open and close https connection , check message ID and confirm whether DPI tag is in syslog
class TestCFS_TC122(Test):
    uuid = "SOSAIOT-TC-54832"
    description = show_testcase_info(
        TESTPLAN, '1520021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520021')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        cmd_list = ['route del default',
                    f'route add default gw {Parameter.X2_IP}',
                    f'curl http://{Parameter.httpserver_ip}']
        res = pc3_login.send_commands(cmd_list)
        Assertion.assert_regular(
            res, "baidu", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple2 = ('m=97', 'dpi=1')
        res2 = syslog_check(syslog_file, search_tuple2)
        Assertion.assert_equal(res2, True, "ERR: verify syslog on server failed.")

    def test_03_disable_content_filtering_service(self):
        cfs_settings_dict = {'enable': False}
        output = content_filter_api.edit_cfs_setting(**cfs_settings_dict)
        Assertion.assert_equal(output, True, "ERR: enable Content Filtering Service failed")


#  Syslog Format in default mode, check DPI tag in syslog
class TestSyslogMode_TC123(Test):
    uuid = "SOSAIOT-TC-54833"
    description = show_testcase_info(
        TESTPLAN, '1520023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520023')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_log_enhanced(self):
        res = TestAppRule_TC102().res_for_test_tc123.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


#  Syslog Format in enhanced mode, check DPI tag in syslog
class TestSyslogMode_TC124(Test):
    uuid = "SOSAIOT-TC-54834"
    description = show_testcase_info(
        TESTPLAN, '1520024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520024')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_log_enhanced(self):
        res = TestAppRule_TC107.res_for_test_tc124.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


# Syslog Format in ArcSight mode, check DPI tag in syslog
class TestSyslogMode_TC125(Test):
    uuid = "SOSAIOT-TC-54835"
    description = show_testcase_info(
        TESTPLAN, '1520025', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520025')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_log_ArcSight(self):
        res = TestAppCtrl_TC114.res_for_test_tc125.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")

# Syslog Format in WebTrends mode, check DPI tag in syslog


class TestSyslogMode_TC127(Test):
    uuid = "SOSAIOT-TC-54837"
    description = show_testcase_info(
        TESTPLAN, '1520027', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520027')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_syslog_WebTrends(self):
        res = TestAppCtrl_TC113.res_for_test_tc127.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


# When App Control=1; Enable App Control only on No zones, Open and close https connnection to FW, check DPI tag in syslog and GUI log
class TestAppCtrl_TC128(Test):
    uuid = "SOSAIOT-TC-54840"
    description = show_testcase_info(
        TESTPLAN, '1520028', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520028')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_app_control_for_lan(self):
        res = zone_api.switch_app_control_on_zone('LAN', False)
        Assertion.assert_equal(res, True, "ERR: disable app control for wan failed")

    def test_02_disable_app_control_for_wan(self):
        res = zone_api.switch_app_control_on_zone('WAN', False)
        Assertion.assert_equal(res, True, "ERR: disable app control for wan failed")

    def test_03_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, 'dpi=0')
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on LAN zones, Open and close HTTPS connection from or to LAN Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC129(Test):
    uuid = "SOSAIOT-TC-54841"
    description = show_testcase_info(
        TESTPLAN, '1520029', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520029')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_02_check_syslog_WebTrends(self):
        res = TestAppRule_TC112.res_for_test_tc129.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


# When App Control=1; Enable App Control only on LAN zones, Open and close HTTPS connection between other zones except LAN Zone, check DPI tag in syslog and GUI log
class TestAppCtrl_TC130(Test):
    uuid = "SOSAIOT-TC-54842"
    description = show_testcase_info(
        TESTPLAN, '1520030', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520030')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, PC2_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on DMZ zones, Open and close HTTPS connection from or to DNZ Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC131(Test):
    uuid = "SOSAIOT-TC-54843"
    description = show_testcase_info(
        TESTPLAN, '1520031', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520031')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    def test_02_enable_app_control_for_dmz(self):
        res = zone_api.switch_app_control_on_zone('DMZ', True)
        Assertion.assert_equal(res, True, "ERR: enable app control for dmz failed")

    def test_03_send_http_traffic(self):
        pc3_login.send_command(f'echo "" > {syslog_file}')
        pc3_login.send_command(f'curl https://{Parameter.httpserver_ip}')

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, PC2_ETH2_IP, "dpi=1")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on DMZ zones, Open and close HTTPS connection between other zones except DMZ Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC132(Test):
    uuid = "SOSAIOT-TC-54844"
    description = show_testcase_info(
        TESTPLAN, '1520032', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520032')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on WAN zones, Open and close HTTPS connection from or to WAN Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC135(Test):
    uuid = "SOSAIOT-TC-54845"
    description = show_testcase_info(
        TESTPLAN, '1520035', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520035')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_disable_app_control_for_dmz(self):
        res = zone_api.switch_app_control_on_zone('DMZ', False)
        Assertion.assert_equal(
            res, True, "ERR: disable app control for dmz failed")

    def test_02_enable_app_control_for_wan(self):
        res = zone_api.switch_app_control_on_zone('WAN', True)
        Assertion.assert_equal(res, True, "ERR: enable app control for wan failed")

    def test_03_send_https_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, PC2_ETH2_IP, "dpi=1")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on WAN zones, Open and close HTTPS connection between other zones except WAN Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC136(Test):
    uuid = "SOSAIOT-TC-54846"
    description = show_testcase_info(
        TESTPLAN, '1520036', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520036')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_http_traffic(self):
        cmd_list = [f"route add -net 13.13.1.0/24 gateway {Parameter.FIREWALL}",
                    f'echo "" > {syslog_file}',
                    f'curl https://{Parameter.dmz_httpserver}']
        res = pc1_login.send_commands(cmd_list)
        Assertion.assert_regular(res, "https", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on Customer zones, Open and close HTTPS connection from or to Customer Zone, check DPI tag in syslog and GUI log
class TestAppCtrl_TC141(Test):
    uuid = "SOSAIOT-TC-54847"
    description = show_testcase_info(
        TESTPLAN, '1520041', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520041')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': 'custom',
            'security_type': 'trusted',
            'interface_trust': True,
            "app_control": True
        }
        trusted_dict = {"zones": [base_dict]}
        (res, msg) = zone_api.add_zone_object(msg=True, **trusted_dict)
        if res is False:
            res = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(res, True, "ERR: add custom zone failed")

    def test_02_disable_app_control_for_wan(self):
        res = zone_api.switch_app_control_on_zone('WAN', False)
        Assertion.assert_equal(res, True, "ERR: disable app control for wan failed")

    def test_03_edit_x2_as_custom_zone(self):
        x2_dict = {
            'if': 'x2',
            'zone': 'custom',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        (rc1, msg1) = if_v4_api.config_interface(msg=True, **x2_dict)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Configure VLAN failed!")

    def test_04_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_05_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, PC2_ETH2_IP, "dpi=1")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1; Enable App Control only on Customer zones, Open and close HTTPS connection between other zones except Customer Zone , check DPI tag in syslog and GUI log
class TestAppCtrl_TC142(Test):
    uuid = "SOSAIOT-TC-54848"
    description = show_testcase_info(
        TESTPLAN, '1520042', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520042')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc1_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_02_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC1_ETH2_IP, PC2_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1 ,Enable App Control Exclusion List and Use IPS Exclusion List,Open and close HTTP connection ,check DPI tag in syslog and GUI log
class TestAppCtrl_TC116(Test):
    uuid = "SOSAIOT-TC-54839"
    description = show_testcase_info(
        TESTPLAN, '1520016', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520016')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_create_IPS_Exclusion_List(self):
        logger.info('=> create a ao for exclusion list')
        ao_dict = {
            'object_type': 'host',
            'name': PC3_ETH2_IP,
            'zone': 'LAN',
            'value': PC3_ETH2_IP
        }
        add_ao_res = ao_api.config_addressobject(**ao_dict)
        logger.info(f'add address object result: {add_ao_res}')

        logger.info('=> add this added ao to IPS global exclusion list')
        exclusion_list = {
            'exclusion_address': 'object',
            'enable_list': True,
            'exclusion_name': ao_dict['name']
        }
        confres = ips_api.config_exclusion_list(**exclusion_list)
        logger.info(f'config IPS exclusion list result: {confres}')

        resp = ips_api.get_exclusion_list_global()
        Assertion.assert_regular(json.dumps(resp), f'"name": "{PC3_ETH2_IP}"', 
                                 'ERR: create IPS exclusion list failed')

    def test_02_enable_ac_exclusion_list(self):
        ac_dict = {'ips': True}
        confres = app_control_api.config_ac_exclusion(**ac_dict)
        logger.info(f'enable app control global exclusion to IPS result: {confres}')
        resp = app_control_api.get_appcontrol_exlusion_list()
        Assertion.assert_regular(json.dumps(resp), '"ips": true', 
                                 'ERR: config ac exclusion to IPS failed')

    def test_03_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_04_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https', PC3_ETH2_IP, PC2_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")


# When App Control=1 ,Enable App Control Exclusion List and Use App Control Exclusion AO,Open and close HTTP connection ,check DPI tag in syslog and GUI log
class TestAppCtrl_TC115(Test):
    uuid = "SOSAIOT-TC-54838"
    description = show_testcase_info(
        TESTPLAN, '1520015', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1520015')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_enable_ac_exclusion_list(self):
        ac_dict = {'object_name': PC3_ETH2_IP}
        confres = app_control_api.config_ac_exclusion(**ac_dict)
        logger.info(f'enable app control global exclusion to IPS result: {confres}')
        resp = app_control_api.get_appcontrol_exlusion_list()
        Assertion.assert_regular(json.dumps(resp), f'"name": "{PC3_ETH2_IP}"',
                                  'ERR: config ac exclusion to IPS failed')

    def test_02_send_http_traffic(self):
        logger.info("clear the syslog file on PC1")
        pc1_login.send_command(f'echo "" > {syslog_file}')
        res = pc3_login.send_command(f'curl -v https://{Parameter.httpserver_ip}')
        Assertion.assert_regular(res, "Connected to .* port 443", "ERR: send http traffic failed.")

    @repeat_method(5)
    def test_03_check_syslog(self):
        time.sleep(10)
        search_tuple = ("Connection Closed", 'https',PC3_ETH2_IP, PC2_ETH2_IP, "dpi=0")
        res = syslog_check(syslog_file, search_tuple)
        Assertion.assert_equal(res, True, "ERR: verify syslog on server failed.")
