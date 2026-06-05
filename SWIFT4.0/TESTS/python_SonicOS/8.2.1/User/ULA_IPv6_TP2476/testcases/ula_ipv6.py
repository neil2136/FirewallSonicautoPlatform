from definition.settings import *

def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()

def verify_preemption_by_another_admin(url):
    # time.sleep(30)
    pc2.send_command('pkill firefox')
    time.sleep(10)
    cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ui_admin_preempt.py ' + '-url ' + f'{url}' + f' -user admin -pwd {Params.G_NEW_PASSWORD}'
    out = pc2.send_command(cmd)
    logger.info("response: \n" + out)
    Assertion.assert_not_regular(out, 'Exception', "Failed to to verify admin preempt")

def verify_logs(log_text, timeout=10):
    time.sleep(timeout)
    logs = log_monitor.export_log_txt()
    Assertion.assert_regular(json.dumps(logs), log_text, "Err: Did not find the logs")


class TC_00_ULA_Config(Test):
    uuid = "NonTC"

    def test_00_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['SonicWALL Administrators'],
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser1"', "ERR: failed to add Local User")
      
    def test_01_sslvpnserver_settings_with_port_enabled(self):
        sslvpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        updated_server_settings = sslvpnserver.edit_server_setting(**sslvpn_server)
        Assertion.assert_equal(updated_server_settings, True, "Err: failed to configure sslvpn server settings.")

    def test_02_enable_sslvpn_server_access(self):
        enable = {
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")
    
    def test_03_user_logout_log_setting(self):
        user_logout ={
            "log": {
                "event": [
                    {
                        "id": 263,
                        "name": "User Logout",
                        "category": "Users",
                        "group": "Authentication Access",
                        "priority_level": "debug",
                        "log_monitor": {
                            "redundancy_interval": 60
                        }
                    }
                ]
            }
        }
        resp = log_category.logging_level(level='debug')
        Assertion.assert_equal(resp, True, "ERR: Config log settings failed.")
        resp = log_settings.edit_event(event_id='263', **user_logout)
        resp = log_settings.show_event(event_id='263')
        Assertion.assert_regular(json.dumps(resp), '{"redundancy_interval": 60}', 'err: log event not changed')
    
    def test_04_add_ipv6_dmz_lan_rule(self):
        access_rule = {
            'option': 'modify',
            'name': 'ULA Rule1',
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'allow',
            'user_included': {"group": "Trusted Users"},
        }
        output = access_rules.config_ipv6_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_05_add_ipv6_cuz_lan_rule(self):
        access_rule = {
            'option': 'modify',
            'name': 'ULA Rule2',
            'from': 'cuz_zone',
            'to': 'LAN',
            'action': 'allow',
            'user_included': {"group": "Trusted Users"},
        }
        output = access_rules.config_ipv6_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")
    
    def test_06_user_login_log_setting(self):
        user_login ={
            "log": {
                "event": [
                    {
                        "id": 31,
                        "name": "Successful User Login",
                        "category": "Users",
                        "group": "Authentication Access",
                        "priority_level": "debug",
                        "log_monitor": {
                            "redundancy_interval": 60
                        }
                    }
                ]
            }
        }
        resp = log_category.logging_level(level='debug')
        Assertion.assert_equal(resp, True, "ERR: Config log settings failed.")
        resp = log_settings.edit_event(event_id='31', **user_login)
        resp = log_settings.show_event(event_id='31')
        Assertion.assert_regular(json.dumps(resp), '{"redundancy_interval": 60}', 'err: log event not changed')

    def test_07_edit_lan_wan_ipv6_rule(self):
        rule = access_rules_ipv6.get_accessrule_via_zones_ipv6(srczone='LAN', dstzone='WAN')
        del rule['access_rules'][0]['ipv6']['users']['included']
        rule['access_rules'][0]['ipv6']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv6']['uuid']
        res = fw_api.api_put(f'api/sonicos/access-rules/ipv6/uuid/{uuid}', data=rule)
        Assertion.assert_equal(res, True, "ERR: edit access rule failed.")

    def test_08_edit_lan_wan_ipv4_rule(self):
        rule = access_rules_ipv4.get_ipv4_access_rule_given_from_to(srczone='LAN', destzone='WAN')
        del rule['access_rules'][0]['ipv4']['users']['included']
        rule['access_rules'][0]['ipv4']['users']['included'] = {'group': 'Everyone'}
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        res = fw_api.api_put(f'api/sonicos/access-rules/ipv4/uuid/{uuid}', data=rule)
        Assertion.assert_equal(res, True, "ERR: edit access rule failed.")

    def test_09_disable_updates_prompt(self):
        ui_fw.disable_automatic_updates_prompt()

class TC_01_User_Has_Read_Only_privilege(Test):
    uuid = "SOSAIOT-TC-76068"
    description = show_testcase_info(Parameter.TESTPLAN, "1504090", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504090')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_local_user(self):
        user_json = { 
            'action': 'edit',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['SonicWALL Read-Only Admins']
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser1"', "ERR: failed to edit Local User")
    
    def test_03_verify_read_only_privilege(self):
        admin_api.set_non_config_mode()
        ui_ula.read_only_mode_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')

class TC_02_User_Has_Limited_Admin_Privilege(Test):
    uuid = "SOSAIOT-TC-76069"
    description = show_testcase_info(Parameter.TESTPLAN, "1504091", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504091')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_local_user(self):
        user_json = { 
            'action': 'edit',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['Limited Administrators']
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "testuser1"', "ERR: failed to edit Local User")
    
    def test_03_verify_limited_admin_privilege(self):
        admin_api.set_non_config_mode()
        ui_ula.limited_privilege_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')


class TC_03_User_Lockout_From_IPv6_Address(Test):
    uuid = "SOSAIOT-TC-76074"
    description = show_testcase_info(Parameter.TESTPLAN, "1504099", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504099')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_enable_user_lockout(self):
        admin_json = {
            "administration": {
            "local_user_lockout": True,
            "log_without_lockout": False,
            "user_lockout": {
                    "enable": True,
                    "failures_rate": 2,
                    "failures_duration": 2,
                    "lockout_duration": 2
                 },
            "admin":{
                'preempt_action': 'goto-non-config'
            }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")

    def test_03_user_lockout_from_IPv6_address(self):
        ui_ula.lockout_user_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'password', attempt=2)
        # waiting till lockout period
        time.sleep(130)
        ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')

    def test_04_edit_user_lockout(self):
        admin_json = {
            "administration": {
                "local_user_lockout": True,
                "log_without_lockout": False,
                "user_lockout": {
                    "enable": True,
                    "failures_rate": 3,
                    "failures_duration": 1,
                    "lockout_duration": 5
                },
                "admin": {
                    'preempt_action': 'goto-non-config'
                }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")


class TC_04_User_Logout_Using_Logout_Button(Test):
    uuid = "SOSAIOT-TC-76080"
    description = show_testcase_info(Parameter.TESTPLAN, "1504107", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504107')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_user_logout_using_logout_button(self):
        ui_ula.ula_user_fw_logout(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')
        ui_fw.verify_user_status_page(Parameter.PC1_ETH0_IPV6, 'testuser1', timeout=0, expected_failure=True)
       

class TC_05_User_Logout_Log(Test):
    uuid = "SOSAIOT-TC-76081"
    description = show_testcase_info(Parameter.TESTPLAN, "1504108", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504108')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_user_logout_log(self):
        log_monitor.clear_log()
        ui_ula.ula_user_fw_logout(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')
        log_text = "User logged out - web logout"
        verify_logs(log_text)
        verify_logs(Parameter.PC1_ETH0_IPV6)


class TC_06_User_Logout_By_Administrator(Test):
    uuid = "SOSAIOT-TC-76082"
    description = show_testcase_info(Parameter.TESTPLAN, "1504109", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504109')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_user_logout_by_administrator(self):
        run_io_tasks_in_parallel([
            lambda: ui_ula.verify_ula_user_logout_window(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1', timeout=80),
            lambda: ui_fw.user_logout_by_admin('testuser1', timeout=30)
        ])


class TC_07_User_Logout_By_Administrator_Log(Test):
    uuid = "SOSAIOT-TC-76083"
    description = show_testcase_info(Parameter.TESTPLAN, "1504110", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_user_logout_by_administrator_log(self):
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
            lambda: ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1'),
            lambda: ui_fw.user_logout_by_admin('testuser1', timeout=30)
        ])
        log_text = "User logged out - logged out by admin"
        verify_logs(log_text)
        verify_logs(Parameter.PC1_ETH0_IPV6)


class TC_08_User_Lockout_From_IPv6_Address_Then_Login_Via_IPv4_Address(Test):
    uuid = "SOSAIOT-TC-76075"
    description = show_testcase_info(Parameter.TESTPLAN, "1504100", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504100')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_edit_admin_settings(self):
        admin_json = {
            "administration": {
            "local_user_lockout": True,
            "log_without_lockout": False,
            "user_lockout": {
                    "enable": True,
                    "failures_rate": 2,
                    "failures_duration": 2,
                    "lockout_duration": 2
                 },
            "admin":{
                'preempt_action': 'goto-non-config'
            }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")
    
    def test_03_user_lockout_from_IPv6_address_then_login_via_IPv4_address(self):
        pc2.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ula_user_login.py ' + '-url ' + f'https://[{Parameter.X0_IPV6}]' + ' -user testuser1 -pwd password -attempt 2 -failure True'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        ui_ula.lockout_user_ui(f'https://{Parameter.FIREWALL}', 'testuser1', 'S0nic@uto1')

        # waiting till lockout period
        time.sleep(125)
        
        ui_ula.ula_login_ui(f'https://{Parameter.FIREWALL}', 'testuser1', 'S0nic@uto1')
        pc2.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ula_user_login.py ' + '-url ' + f'https://[{Parameter.X0_IPV6}]' + ' -user testuser1 -pwd S0nic@uto1 -attempt 0 -failure False'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)

    def test_04_edit_user_lockout(self):
        admin_json = {
            "administration": {
                "local_user_lockout": True,
                "log_without_lockout": False,
                "user_lockout": {
                    "enable": True,
                    "failures_rate": 3,
                    "failures_duration": 1,
                    "lockout_duration": 5
                },
                "admin": {
                    'preempt_action': 'goto-non-config'
                }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")

class TC_09_User_Lockout_From_IPv4_Address_Then_Login_Via_IPv6_Address(Test):
    uuid = "SOSAIOT-TC-76076"
    description = show_testcase_info(Parameter.TESTPLAN, "1504101", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_edit_admin_settings(self):
        # update common_lib to uncomment local_user_lockout:true
        admin_json = {
            "administration": {
            "local_user_lockout": True,
            "log_without_lockout": False,
            "user_lockout": {
                    "enable": True,
                    "failures_rate": 2,
                    "failures_duration": 2,
                    "lockout_duration": 2
                 },
            "admin":{
                'preempt_action': 'goto-non-config'
            }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")
    
    def test_03_user_lockout_from_IPv4_address_then_login_via_IPv6_address(self):
        ui_ula.lockout_user_ui(f'https://{Parameter.FIREWALL}', 'testuser1', 'password', attempt=2)
        pc2.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ula_user_login.py ' + '-url ' + f'https://[{Parameter.X0_IPV6}]' + ' -user testuser1 -pwd S0nic@uto1 -attempt 0 -failure True'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)
        
        # waiting till lockout period
        time.sleep(120)

        ui_ula.ula_login_ui(f'https://{Parameter.FIREWALL}', 'testuser1', 'S0nic@uto1')
        pc2.send_command('pkill firefox')
        time.sleep(10)
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ula_user_login.py ' + '-url ' + f'https://[{Parameter.X0_IPV6}]' + ' -user testuser1 -pwd S0nic@uto1 -attempt 0 -failure False'
        out = pc2.send_command(cmd)
        logger.info("response: \n" + out)

    def test_04_edit_user_lockout(self):
        admin_json = {
            "administration": {
                "local_user_lockout": True,
                "log_without_lockout": False,
                "user_lockout": {
                    "enable": True,
                    "failures_rate": 3,
                    "failures_duration": 1,
                    "lockout_duration": 5
                },
                "admin": {
                    'preempt_action': 'goto-non-config'
                }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")


class TC_10_Admin_Permission_With_IPv6_Address_Then_Try_Permission_Via_IPv4_Address(Test):
    uuid = "SOSAIOT-TC-76078"
    description = show_testcase_info(Parameter.TESTPLAN, "1504104", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_admin_permission_with_IPv6_address_then_try_permission_via_IPv4_address(self):
        run_io_tasks_in_parallel([
            lambda: verify_preemption_by_another_admin(f'https://[{Parameter.X0_IPV6}]'),
            lambda: ui_fw.fw_config(f'https://{Parameter.FIREWALL}', 'testuser4')
        ])


class TC_11_Admin_Permission_With_IPv4_Address_Then_Try_Permission_Via_IPv6_Address(Test):
    uuid = "SOSAIOT-TC-76079"
    description = show_testcase_info(Parameter.TESTPLAN, "1504105", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504105')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_admin_permission_with_IPv4_address_then_try_permission_via_IPv6_address(self):
        run_io_tasks_in_parallel([
            lambda: verify_preemption_by_another_admin(f'https://{Parameter.FIREWALL}'),
            lambda: ui_fw.fw_config(f'https://[{Parameter.X0_IPV6}]', 'testuser5')
        ])


class TC_12_Verify_User_Session_Logout_Limit_Expired_Log(Test):
    uuid = "SOSAIOT-TC-76066"
    description = show_testcase_info(Parameter.TESTPLAN, "1504088", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504088')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_local_user(self):
        user_json = {
            'action': 'edit',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['SonicWALL Administrators'],
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"minutes": 3', "ERR: failed to edit Local User")

    def test_03_ipv6_fw_local_user_login(self):
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
        lambda: ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1', timeout=180),
        lambda: verify_logs("User logged out - User Session Quota Exceeded", timeout=210)
        ])
    
    def test_04_edit_local_user(self):
        user_json = { 
            'action': 'edit',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['SonicWALL Administrators'],
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 0,
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_not_regular(json.dumps(added_user), '"minutes": 3', "ERR: failed to edit Local User")


class TC_13_Login_As_Built_Admin(Test):
    uuid = "SOSAIOT-TC-76071"
    description = show_testcase_info(Parameter.TESTPLAN, "1504093", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504093')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_login_as_built_admin(self):
        admin_api.set_non_config_mode()
        ui_ula.full_admin_mode_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')


class TC_14_User_Unlocked_By_Admin(Test):
    uuid = "SOSAIOT-TC-76077"
    description = show_testcase_info(Parameter.TESTPLAN, "1504102", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504102')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_edit_admin_settings(self):
        admin_json = {
            "administration": {
            "local_user_lockout": True,
            "log_without_lockout": False,
            "user_lockout": {
                    "enable": True,
                    "failures_rate": 2,
                    "failures_duration": 2,
                    "lockout_duration": 2
                 },
            "admin":{
                'preempt_action': 'goto-non-config'
            }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")

    def test_03_user_unlocked_by_admin(self):
        ui_ula.lockout_user_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'password', attempt=2)
        # unlock the user
        resp = user_status.unlock_user_name('testuser1')
        Assertion.assert_equal(resp, True, "ERR: Failed to unlock the user.")
        # login
        ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1')

    def test_04_edit_user_lockout(self):
        admin_json = {
            "administration": {
                "local_user_lockout": True,
                "log_without_lockout": False,
                "user_lockout": {
                    "enable": True,
                    "failures_rate": 3,
                    "failures_duration": 1,
                    "lockout_duration": 5
                },
                "admin": {
                    'preempt_action': 'goto-non-config'
                }
            }
        }
        resp = admin_api.edit_admin(**admin_json)
        Assertion.assert_equal(resp, True, "ERR: Enable user lockout failed.")


class TC_15_User_Logout_Login_Session_Limit_Expired(Test):
    uuid = "SOSAIOT-TC-76085"
    description = show_testcase_info(Parameter.TESTPLAN, "1504113", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504113')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_user_session_time_limit(self):
        user_setings["user"]["auth"]["web_login_session_limit"] = 2
        response = user_settings.user_settings_base(**user_setings)
        Assertion.assert_equal(response, True, "ERR: Unable to modify user session time limit.")

    def test_03_user_logout_login_session_limit_expired(self):
        run_io_tasks_in_parallel([
            lambda: ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1', timeout=125),
            lambda: ui_fw.verify_user_status_page(Parameter.PC1_ETH0_IPV6, 'testuser1', timeout=50),
            lambda: ui_fw.verify_user_status_page(Parameter.PC1_ETH0_IPV6, 'testuser1', timeout=180, expected_failure=True)
        ])

    def test_04_edit_user_session_time_limit(self):
        user_setings["user"]["auth"]["web_login_session_limit"] = 30
        response = user_settings.user_settings_base(**user_setings)
        Assertion.assert_equal(response, True, "ERR: Unable to modify user session time limit.")

def verify_logs_and_tsr_for_user(ip, username, timeout=10):
    log_monitor.clear_log()
    time.sleep(timeout)
    tsr_content = diag_api.get_tsr_part('Users', 'Status')
    Assertion.assert_regular(tsr_content, ip, "ERR: Failed to verify ipv6 address.")
    Assertion.assert_regular(tsr_content, username, "ERR: Failed to verify username.")

class TC_16_IPv6_User_Logged_In_Check_TSR(Test):
    uuid = "SOSAIOT-TC-76087"
    description = show_testcase_info(Parameter.TESTPLAN, "1418197", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1418197')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_IPv6_User_Logged_In_Check_TSR(self):
        run_io_tasks_in_parallel([
            lambda:ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1', timeout=70),
            lambda:verify_logs_and_tsr_for_user(Parameter.PC1_ETH0_IPV6_EXPANDED, 'testuser1', timeout=40),
        ])


def ula_login(pc, ip):
    static_pc = Params.testbed + pc
    pc = Host(static_pc)
    pc.send_command('pkill firefox')
    time.sleep(10)
    cmd = 'python3 ' + os.environ[
        "PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition/ui/ula_user_login.py ' + '-url ' + f'https://[{ip}]' + ' -user testuser1 -pwd S0nic@uto1 -attempt 0 -failure False'
    out = pc.send_command(cmd)
    logger.info("response: \n" + out)


class TC_17_User_Login_Status(Test):
    uuid = "SOSAIOT-TC-76065"
    description = show_testcase_info(Parameter.TESTPLAN, "1504087", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504087')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_edit_local_user(self):
        user_json = { 
            'action': 'edit',
            'username': 'testuser1',
            'userpassword': 'S0nic@uto1',
            'member_of': ['SonicWALL Administrators', 'SSLVPN Services']
        }
        resp = user_local.local_user(**user_json)
        added_user = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(added_user), '"name": "SSLVPN Services"', "ERR: failed to edit Local User")
    
    def test_03_ipv6_user_login_lan(self):
        run_io_tasks_in_parallel([
        lambda: ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1'),
        lambda: ui_fw.verify_user_status_page(Parameter.PC1_ETH0_IPV6, 'testuser1')
        ])

    def test_04_ipv6_user_login_sslvpn(self):
        user_status.user_logout_by_admin('testuser1')
        run_io_tasks_in_parallel([
        lambda: ui_ula.sslvpn_portal_login(f'https://[{Parameter.X0_IPV6}]:4433', 'testuser1', 'S0nic@uto1'),
        lambda: ui_fw.verify_user_status_page(Parameter.PC1_ETH0_IPV6, 'testuser1')
        ])

    def test_05_ipv6_user_login_dmz(self):
        run_io_tasks_in_parallel([
        lambda: ula_login('-PC3', Parameter.X2_IPV6),
        lambda: ui_fw.verify_user_status_page(Parameter.PC3_ETH0_IPV6, 'testuser1', timeout=20)
        ])

    def test_06_ipv6_user_login_cuz(self):
        run_io_tasks_in_parallel([
        lambda: ula_login('-PC4', Parameter.X3_IPV6),
        lambda: ui_fw.verify_user_status_page(Parameter.PC4_ETH0_IPV6, 'testuser1', timeout=20)
        ])


class TC_18_User_Login_Log(Test):
    uuid = "SOSAIOT-TC-76073"
    description = show_testcase_info(Parameter.TESTPLAN, "1504098", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1504098')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_ipv6_user_login_log_lan(self):
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
        lambda: ui_ula.ula_login_ui(f'https://[{Parameter.X0_IPV6}]', 'testuser1', 'S0nic@uto1'),
        lambda: verify_logs(Parameter.PC1_ETH0_IPV6, timeout=40)
        ])

    def test_03_ipv6_user_login_log_sslvpn(self):
        user_status.user_logout_by_admin('testuser1')
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
        lambda: ui_ula.sslvpn_portal_login(f'https://[{Parameter.X0_IPV6}]:4433', 'testuser1', 'S0nic@uto1'),
        lambda: verify_logs(Parameter.PC1_ETH0_IPV6, timeout=40)
        ])

    def test_04_ipv6_user_login_log_dmz(self):
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
        lambda: ula_login('-PC3', Parameter.X2_IPV6),
        lambda: verify_logs(Parameter.PC3_ETH0_IPV6, timeout=40)
        ])

    def test_05_ipv6_user_login_log_cuz(self):
        log_monitor.clear_log()
        run_io_tasks_in_parallel([
        lambda: ula_login('-PC4', Parameter.X3_IPV6),
        lambda: verify_logs(Parameter.PC4_ETH0_IPV6, timeout=40)
        ])