from definition.settings import *
from definition.utils import *


class Test_01_AuthDbgCommand_LogToConsole(Test):
    uuid = "SOSAIOT-TC-51306"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1708675')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_log_to_console(self):
        rs = send_cli_command(cli_dict["enable_log_to_console"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")

    def test_02_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_04_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_05_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if "AUTH:" in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: User Debug Log not appear in console")

    def test_06_stop_console_auth_print(self):
        rs = set_auth_level(0)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")


class Test_02_UserDbgCommand_AuthLevel(Test):
    uuid = "SOSAIOT-TC-51304"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1708674')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_04_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if "AUTH:" in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: User Debug Log not appear in console")

    def test_05_stop_console_auth_print(self):
        rs = set_auth_level(0)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_06_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_07_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_08_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if "AUTH:" not in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: User Debug Log appear in console")


class Test_03_UserDbgCommand_AddedIn_CLI(Test):
    uuid = "SOSAIOT-TC-51303"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515230')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_command_under_user(self):
        command_return = show_via_cli_command(cli_dict["show_user_command"])
        logger.info(f'command under user command result: {command_return}')
        rs = check_str_in_command(["auth-level", "ip-level", "ha-level", "connection-level"], command_return)
        Assertion.assert_equal(rs, True, "ERR: check command under user failed")

    def test_02_random_configure_user(self):
        rs = send_cli_command(cli_dict["random_configure_user"])
        logger.info(f'command under user command result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Configure user console log level failed")

    def test_03_check_dbg_user_info(self):
        command_return = show_via_cli_command(cli_dict["show_dbg_user"])
        logger.info(f'show dbg user info result: {command_return}')
        rs = check_str_in_command(["auth-level 2", "ip-level 3", "ha-level 4", "connection-level 3"], command_return)
        Assertion.assert_equal(rs, True, "ERR: Configure user console log level failed")

    def test_04_recover_user_level(self):
        rs = send_cli_command(cli_dict["recover_user_level"])
        logger.info(f'show dbg user info result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Recover the test environment failed")


class Test_04_UserDbgAuthLDAP_AddedIn_CLI(Test):
    uuid = "SOSAIOT-TC-51305"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515236')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_command_under_authldap(self):
        command_return = show_via_cli_command(cli_dict["show_auth_ldap_command"])
        logger.info(f'command under user command result: {command_return}')
        expect_dict = ["all", "args", "async", "auth-filter", "ber", "client", "conns", "daemon", "name-resolve",
                       "packets", "parse", "pkt-dump", "refs", "relay", "socket-dump", "tool", "tool-verbose", "trace"]
        rs = check_str_in_command(expect_dict, command_return)
        Assertion.assert_equal(rs, True, "ERR: check command under auth ldap failed")

    def test_02_random_configure_ldap(self):
        rs = send_cli_command(cli_dict["random_configure_auth"])
        logger.info(f'command under user command result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: configure auth ldap failed")

    def test_03_check_dbg_ldap_info(self):
        command_return = show_via_cli_command(cli_dict["show_dbg_auth"])
        logger.info(f'show dbg user info result: {command_return}')
        rs = check_str_not_in_command(["no ldap trace", "no ldap relay"], command_return)
        Assertion.assert_equal(rs, True, "ERR: configure auth ldap failed")

    def test_04_recover_ldap_settings(self):
        rs = send_cli_command(cli_dict["recover_auth_configure"])
        logger.info(f'show dbg user info result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Recover the test environment failed")


@paramunittest.parametrized(
    {'uuid': '1515232', 'open_command': 'set_conn_level_to_6', 'close_command': 'set_conn_level_to_0',
     'verify_content': "USRCON:"},
    {'uuid': '1515233', 'open_command': 'set_ha_level_to_6', 'close_command': 'set_ha_level_to_0',
     'verify_content': "USER HA:"},
    {'uuid': '1515234', 'open_command': 'set_ip_level_to_6', 'close_command': 'set_ip_level_to_0',
     'verify_content': "USRIP:"},
)
class Test_05_UserDbgCommand_LevelTest(Test):
    def setParameters(self, uuid, open_command, close_command, verify_content):
        self.uuid = uuid
        self.open_command = open_command
        self.close_command = close_command
        self.verify_content = verify_content
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_open_conn_log(self):
        rs = send_cli_command(cli_dict[self.open_command])
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set User Level failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_03_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_04_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Open Debug info failed")

    def test_05_stop_console_auth_print(self):
        rs = send_cli_command(cli_dict[self.close_command])
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set User Level failed")

    def test_06_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_07_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_08_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content not in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Close Debug info failed")


class Test_06_AuthDbgCommand_Cia(Test):
    uuid = "SOSAIOT-TC-51312"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515235')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_cia(self):
        rs = send_cli_command(cli_dict["set_cia_to_6"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Command cia to 6 failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_03_enable_sso(self):
        enable_third_party_api = {
            "sso_agent": True,
        }
        rs = usersetting.user_method_authentication(**enable_third_party_api)
        logger.info(f'enable_sso_agent_result:{rs}')
        Assertion.assert_equal(rs, True, "ERR:Enable SSO Agent Failed")

    def test_04_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_05_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if "CIA:" in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: CIA Debug info can't be found")

    def test_06_disable_cia(self):
        rs = send_cli_command(cli_dict["set_cia_to_0"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: show test case info failed")

    def test_07_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_08_disable_sso(self):
        enable_third_party_api = {
            "sso_agent": False,
        }
        rs = usersetting.user_method_authentication(**enable_third_party_api)
        logger.info(f'enable_sso_agent_result:{rs}')
        Assertion.assert_equal(rs, True, "ERR: Disable SSO Agent Failed")

    def test_09_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console Log failed")

    def test_10_verify_auth_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if "CIA:" not in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: CIA Debug info can be found")


class Test_07_Add_LDAPServer(Test):
    uuid = 'NonTC'

    def test_01_add_ldap_server(self):
        try:
            resp = user_ldap.del_ldap_server(Parameter.LDAP_SEVER)
            resp = user_ldap.del_ldap_server("ForestDnsZones.ldapqa.com")
        except:
            pass
        rs = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(rs, True, "ERR: Failed to add LDAP")

    def test_02_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_enable_log_to_console(self):
        rs = send_cli_command(cli_dict["enable_log_to_console"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")


@paramunittest.parametrized(
    {'uuid': '1515250', 'open_command': 'open_ldap_tool', 'close_command': 'close_ldap_tool',
     'verify_content': "ldapSyncConnDelCB", "method": "test_user"},
    {'uuid': '1515251', 'open_command': 'open_ldap_toolverbose', 'close_command': 'close_ldap_toolverbose',
     'verify_content': "ldapSyncConnDelCB", "method": "test_user"},
    {'uuid': '1515252', 'open_command': 'open_ldap_trace', 'close_command': 'close_ldap_trace',
     'verify_content': "ldap_create", "method": "test_user"},
    {'uuid': '1515246', 'open_command': 'open_ldap_parse', 'close_command': 'close_ldap_parse',
     'verify_content': "ldapSyncConnDelCB", "method": "test_user"},
    {'uuid': '1515237', 'open_command': 'open_ldap_all', 'close_command': 'close_ldap_all',
     'verify_content': "LDAP:", "method": "disable_enable_ldap_server"},
    {'uuid': '1515240', 'open_command': 'open_ldap_clients', 'close_command': 'close_ldap_clients',
     'verify_content': "ldapReadUsrsOrGrpsBegin:", "method": "import_user"},
    {'uuid': '1515243', 'open_command': 'open_ldap_daemon', 'close_command': 'close_ldap_daemon',
     'verify_content': "ldapHandlePipeRqsts:", "method": "import_user"},
    {'uuid': '1515238', 'open_command': 'open_ldap_args', 'close_command': 'close_ldap_args',
     'verify_content': "ldap_build_search_req ATTRS", "method": "delete_add_ldap_server"},
    {'uuid': '1515245', 'open_command': 'open_ldap_packets', 'close_command': 'close_ldap_packets',
     'verify_content': "Sending Bind Request", "method": "disable_enable_ldap_server"},
    {'uuid': '1515247', 'open_command': 'open_ldap_pktdump', 'close_command': 'close_ldap_pktdump',
     'verify_content': "0000:", "method": "disable_enable_ldap_server"},
    {'uuid': '1515249', 'open_command': 'open_ldap_socketdump', 'close_command': 'close_ldap_socketdump',
     'verify_content': "ldap_read:", "method": "disable_enable_ldap_server"},
)
class Test_08_AuthDbgCommand_LDAP01(Test):
    def setParameters(self, uuid, open_command, close_command, verify_content, method):
        self.uuid = uuid
        self.open_command = open_command
        self.close_command = close_command
        self.verify_content = verify_content
        self.method = method
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.open_command])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Open ldap all failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_03_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    @repeat_method(5)
    def test_04_verify_log_appear_in_the_console(self):
        rs1 = save_console_log_to_file(console_name_after_command)
        compare_result = compare_console_info()
        rs2 = True if self.verify_content in compare_result else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Debug info can't be found")

    def test_05_disable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.close_command])
        logger.info(f'disable ldap dbg result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: show test case info failed")

    def test_06_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_07_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    def test_08_verify_log_not_appear_in_the_console(self):
        rs1 = save_console_log_to_file(console_name_after_command)
        compare_result = compare_console_info()
        rs2 = True if self.verify_content not in compare_result else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Debug info can be found")


class Test_09_Add_LDAPServerNotAccess(Test):
    uuid = 'NonTC'

    def test_01_add_ldap_server(self):
        try:
            resp = user_ldap.del_ldap_server(Parameter.LDAP_SEVER)
            resp = user_ldap.del_ldap_server("ForestDnsZones.ldapqa.com")
        except:
            pass
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server_not_access)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_enable_log_to_console(self):
        rs = send_cli_command(cli_dict["enable_log_to_console"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")


@paramunittest.parametrized(
    {'uuid': '1515239', 'open_command': 'open_ldap_ber', 'close_command': 'close_ldap_ber',
     'verify_content': "ldapAsyncGotSrchResult:", "method": "schema_read_server"},
    {'uuid': '1515241', 'open_command': 'open_ldap_conns', 'close_command': 'close_ldap_conns',
     'verify_content': "ldapAsyncGotSrchResult:", "method": "test_connection"},
    {'uuid': '1515242', 'open_command': 'open_ldap_filter', 'close_command': 'close_ldap_filter',
     'verify_content': "ldapAsyncGotSrchResult:", "method": "schema_read_server"},
    {'uuid': '1515248', 'open_command': 'open_ldap_relay', 'close_command': 'close_ldap_relay',
     'verify_content': "ldapRelayOnIf", "method": "enable_relay"},
    {'uuid': '1515253', 'open_command': 'open_rad_account', 'close_command': 'close_rad_account',
     'verify_content': "RADSRVR:", "method": "enable_disable_radius_account"},
    {'uuid': '1515254', 'open_command': 'open_radius', 'close_command': 'close_radius',
     'verify_content': "RADIUS:", "method": "add_radius_server_and_test"},
    {'uuid': '1515255', 'open_command': 'open_sso_api', 'close_command': 'close_sso_api',
     'verify_content': "SSO-API:", "method": "enable_3rdParty_API"},
    {'uuid': '1515256', 'open_command': 'open_tacas', 'close_command': 'close_tacas',
     'verify_content': "TACACS+:", "method": "add_tacacs_server_and_delete"},
    {'uuid': '1515257', 'open_command': 'open_tsa', 'close_command': 'close_tsa',
     'verify_content': "TSA:", "method": "enable_terminal_service"}
)
class Test_10_AuthDbgCommand_LDAP02(Test):
    def setParameters(self, uuid, open_command, close_command, verify_content, method):
        self.uuid = uuid
        self.open_command = open_command
        self.close_command = close_command
        self.verify_content = verify_content
        self.method = method
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.open_command])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Open ldap all failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_03_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    def test_04_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_05_verify_log_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Debug info can't be found")

    def test_06_disable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.close_command])
        logger.info(f'disable ldap dbg result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: show test case info failed")

    def test_07_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_08_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    def test_09_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_10_verify_log_not_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content not in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Debug info can be found")


class Test_11_Add_LDAPServerwith_Domain(Test):
    uuid = 'NonTC'

    def test_01_add_ldap_server(self):
        try:
            resp = user_ldap.del_ldap_server(Parameter.LDAP_SEVER)
            resp = user_ldap.del_ldap_server("ForestDnsZones.ldapqa.com")
        except:
            pass
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        time.sleep(5)
        ldap_user = edit_ldap_hostname(ldap_server_with_domain)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")


@paramunittest.parametrized(
    {'uuid': '1515244', 'open_command': 'open_ldap_nameresolve', 'close_command': 'close_ldap_nameresolve',
     'verify_content': "LDAP_gethostbyname_r", "method": "test_connection_with_domain"},
)
class Test_12_AuthDbgCommand_LDAP03(Test):
    def setParameters(self, uuid, open_command, close_command, verify_content, method):
        self.uuid = uuid
        self.open_command = open_command
        self.close_command = close_command
        self.verify_content = verify_content
        self.method = method
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.open_command])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Open ldap all failed")

    def test_02_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_03_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    def test_04_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_05_verify_log_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Debug info can't be found")

    def test_06_disable_ldap_dbg(self):
        rs = send_cli_command(cli_dict[self.close_command])
        logger.info(f'disable ldap dbg result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: show test case info failed")

    def test_07_get_console_log_before_command(self):
        rs = save_console_log_to_file(console_name_before_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_08_generate_debug_log(self):
        rs = ldap_operation(self.method)
        Assertion.assert_equal(rs, True, f"ERR:{self.method} failed")

    def test_09_get_console_log_after_command(self):
        rs = save_console_log_to_file(console_name_after_command)
        Assertion.assert_equal(rs, True, "ERR: Get Console log failed")

    def test_10_verify_log_not_appear_in_the_console(self):
        compare_result = compare_console_info()
        rs = True if self.verify_content not in compare_result else False
        Assertion.assert_equal(rs, True, "ERR: Debug info can be found")


class Test_13_AuthDbgCommand_LogToSyslog(Test):
    uuid = "SOSAIOT-TC-51308"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1708675')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_log_to_syslog(self):
        rs = send_cli_command(cli_dict["enable_log_to_syslog"])
        rs &= send_cli_command(cli_dict["enable_syslog_anyserver"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")

    def test_02_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_get_syslog_before_command_all_syslog_server(self):
        rs1 = get_syslog_pc1("server1_syslog_before")
        rs2 = get_syslog_pc3("server2_syslog_before")
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Get Console Log failed")

    def test_04_verify_auth_appear_in_all_syslog_server(self):
        fw.api_login()
        fw.api_logout()
        time.sleep(10)
        get_log_1 = get_syslog_pc1("server1_syslog_after")
        get_log_1 = get_syslog_pc3("server2_syslog_after")
        compare_result1 = compare_console_info(file_before="server1_syslog_before", file_after="server1_syslog_after",
                                               verify_file='syslog')
        compare_result2 = compare_console_info(file_before="server2_syslog_before", file_after="server2_syslog_after",
                                               verify_file='syslog')
        rs1 = True if "AUTH:" in compare_result1 else False
        rs2 = True if "AUTH:" in compare_result2 else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: User Debug Log not appear in console")

    def test_05_enable_syslog_profile(self):
        rs = send_cli_command(cli_dict["enable_syslog_profile"])
        time.sleep(3)
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")

    def test_06_get_syslog_before_command_all_syslog_server(self):
        rs1 = get_syslog_pc1("server1_syslog_before")
        rs2 = get_syslog_pc3("server2_syslog_before")
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Get Console Log failed")

    def test_07_verify_auth_appear_in_all_syslog_server(self):
        fw.api_login()
        fw.api_logout()
        time.sleep(10)
        get_log_1 = get_syslog_pc1("server1_syslog_after")
        get_log_1 = get_syslog_pc3("server2_syslog_after")
        compare_result1 = compare_console_info(file_before="server1_syslog_before", file_after="server1_syslog_after",
                                               verify_file='syslog')
        compare_result2 = compare_console_info(file_before="server2_syslog_before", file_after="server2_syslog_after",
                                               verify_file='syslog')
        rs1 = True if "AUTH:" not in compare_result1 else False
        rs2 = True if "AUTH:" in compare_result2 else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: User Debug Log not appear in console")


class Test_14_AuthDbgCommand_LogToAnySyslogServer(Test):
    uuid = "SOSAIOT-TC-51334"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1708675')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_log_to_syslog(self):
        rs = send_cli_command(cli_dict["enable_syslog_anyserver"])
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")

    def test_02_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_get_syslog_before_command_all_syslog_server(self):
        rs1 = get_syslog_pc1("server1_syslog_before")
        rs2 = get_syslog_pc3("server2_syslog_before")
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Get Console Log failed")

    def test_04_verify_auth_appear_in_all_syslog_server(self):
        fw.api_login()
        fw.api_logout()
        time.sleep(10)
        get_log_1 = get_syslog_pc1("server1_syslog_after")
        get_log_1 = get_syslog_pc3("server2_syslog_after")
        compare_result1 = compare_console_info(file_before="server1_syslog_before", file_after="server1_syslog_after",
                                               verify_file='syslog')
        compare_result2 = compare_console_info(file_before="server2_syslog_before", file_after="server2_syslog_after",
                                               verify_file='syslog')
        rs1 = True if "AUTH:" in compare_result1 else False
        rs2 = True if "AUTH:" in compare_result2 else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: User Debug Log not appear in console")


class Test_15_AuthDbgCommand_LogToSepecifySyslogServer(Test):
    uuid = "SOSAIOT-TC-51335"
    description = show_testcase_info(TESTPLAN, uuid, description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1708675')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_enable_log_to_syslog(self):
        rs = send_cli_command(cli_dict["enable_syslog_profile"])
        logger.info(f'enable log to console result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Enable Log to Console failed")

    def test_02_open_user_log(self):
        rs = set_auth_level(6)
        logger.info(f'set auth level result: {rs}')
        Assertion.assert_equal(rs, True, "ERR: Set Auth Level failed")

    def test_03_get_syslog_before_command_all_syslog_server(self):
        rs1 = get_syslog_pc1("server1_syslog_before")
        rs2 = get_syslog_pc3("server2_syslog_before")
        Assertion.assert_equal(rs1 & rs2, True, "ERR: Get Console Log failed")

    def test_04_verify_auth_appear_in_all_syslog_server(self):
        fw.api_login()
        fw.api_logout()
        time.sleep(10)
        get_log_1 = get_syslog_pc1("server1_syslog_after")
        get_log_1 = get_syslog_pc3("server2_syslog_after")
        compare_result1 = compare_console_info(file_before="server1_syslog_before", file_after="server1_syslog_after",
                                               verify_file='syslog')
        compare_result2 = compare_console_info(file_before="server2_syslog_before", file_after="server2_syslog_after",
                                               verify_file='syslog')
        rs1 = True if "AUTH:" not in compare_result1 else False
        rs2 = True if "AUTH:" in compare_result2 else False
        Assertion.assert_equal(rs1 & rs2, True, "ERR: User Debug Log not appear in console")
