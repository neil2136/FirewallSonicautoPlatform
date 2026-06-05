import sys
import os
import json
import re
import pexpect
import time
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Pwd_Check_In_DMZ/')
from definition.settings import *
from definition.conf_fw import *
from pexpect import pxssh
from definition import users

def verify_connection_remote(openstack_PC, ip, username, password):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        logger.info(hostname)

        # SSH into PC
        s.login(hostname, "root", "password")
        logger.info(f"Successfully login to: {hostname}")
        s.prompt()

        # SSH into Firewall
        s.sendline(f"ssh {username}@{ip}")

        # Wait for password prompt
        s.expect("Password:")
        s.sendline(password)

        # Capture output
        s.prompt(timeout=10)
        output = s.before.decode("utf-8", errors="ignore")
        logger.info(output)

        # Detect actual CLI shell prompt like test@xxxx>
        prompt_ok = re.search(rf"{username}@\S+", output) is not None
        warning_present = "you should change" in output.lower()
        access_denied = "access denied" in output.lower()

        # ---- Decision Logic ----
        if warning_present and prompt_ok:
            return {
                "status": "SUCCESS_WITH_WARNING",
                "output": output
            }
        elif warning_present and not prompt_ok:
            return {
                "status": "FAIL_NO_PROMPT",
                "output": output
            }
        elif access_denied:
            return {
                "status": "FAIL_ACCESS_DENIED",
                "output": output
            }
        else:
            return {
                "status": "UNKNOWN",
                "output": output
            }
    except Exception as e:
        return {
            "status": "SSH_FAILURE",
            "output": str(e)
        }

class config_ldap_radius_tacacs(Test):
    uuid = 'NonTC'

    def test_01_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }
            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

    def test_02_add_radius_user_method(self):
        logger.info("-------Radius Config---------")
        add_radius_user = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False
        }
        response = Radius_user.add_radius_server(**add_radius_user)
        logger.info(response)
        response_get = Radius_user.show_radius_server()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"', 'err: Failed to create radius server')

    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user_test = Radius_user.test_radius_server()
        Assertion.assert_equal(radius_user_test, True, "ERR: Radius user test got failed")

    def test_04_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,
        }
        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs user is not created successfully")
        tacacs_user_info = Tacacs_user.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_04_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = Tacacs_user.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs user test got failed")

    def test_05_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")

    def test_06_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,', "failed to enable toggle button")

    def test_07_LDAP_Users_AdminPrivelage(self):
        json_obj = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "SonicWALL Administrators",
                            "domain": "any",
                            "member": [
                                {"name": "All LDAP Users"}
                            ]
                        }
                    ]
                }
            }
        }
        resp = user.config_local_group_by_name("SonicWALL Administrators","any",**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user.show_local_group_by_name("SonicWALL Administrators")
        # print(json.dumps(res))
        Assertion.assert_regular(
            json.dumps(res),
            r'"member": \[\{"name": "All LDAP Users"\}\]',
            "ERR: Failed to add LDAP Users under SonicWALL Administrators group"
        )

    def test_08_disable_password_restrictions(self):
        obj_json = {
            "administration": {
                "password": {
                    "aging": {},
                    "last_changed": {},
                    "uniqueness": {},
                    "enforce_character_difference": False,
                    "minimum_length": 8,
                    "complexity": {},
                }
            }
        }
        response = admin_setting.conf_admin_update(**obj_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = admin_setting.show_admin_setting()
        Assertion.assert_regular(json.dumps(resp), '"complexity": {},', "ERR: Failed to edit password constraints")

# FOR LDAP USER
class TC01_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77829"
    description = show_testcase_info(Parameter.TESTPLAN, '4405975', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405975')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": True
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": true,', "failed to enable toggle button")

    def test_02_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'test', 'password')
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_regular(is_auth,
            r"(?i)the password is one that is known to have possibly been compromised, it must be changed before you can log in",
            "ERR: Compromised password message not found")


class TC02_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77828"
    description = show_testcase_info(Parameter.TESTPLAN, '4405974', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405974')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,',
                                 "failed to disable toggle button")

    def test_02_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'test', 'password')
        time.sleep(10)
        is_auth = Local_User.local_user_login()
        # Assertion.assert_equal(is_auth, "True", "Error: Login unsuccessful ")
        Assertion.assert_regular(str(is_auth), r"True", "ERR: Login did not return True")

class TC03_compromised_pwd_check_in_dmz(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77827"
    description = show_testcase_info(Parameter.TESTPLAN, '4405973', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405973')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-user-login-with-external-auth','enable',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button not enabled")

    def test_02_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "test", "password")
        Assertion.assert_equal(
            result["status"],
            "FAIL_ACCESS_DENIED",
            "ERR: Login should be blocked when compromised password check is enabled.")


class TC04_compromised_pwd_check_in_dmz(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77826"
    description = show_testcase_info(Parameter.TESTPLAN, '4405972', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405972')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','no block-user-login-with-external-auth',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button failed to disable")

    def test_02_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "test", "password")

        Assertion.assert_equal(result["status"],"SUCCESS_WITH_WARNING",
            "ERR: Login should succeed with warning when block-user-login-with-external-auth is disabled.")

# FOR RADIUS USER
class TC05_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77833"
    description = show_testcase_info(Parameter.TESTPLAN, '4405979', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405979')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("-------Radius Auth---------")
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"', "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": True
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": true,', "failed to enable toggle button")

    def test_03_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'test', 'password')
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_regular(is_auth,
                                 r"(?i)the password is one that is known to have possibly been compromised, it must be changed before you can log in",
                                 "ERR: Compromised password message not found")

class TC06_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77832"
    description = show_testcase_info(Parameter.TESTPLAN, '4405978', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405978')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("-------Radius Auth---------")
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,',
                                 "failed to disable toggle button")

    def test_03_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'test', 'password')
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_regular(str(is_auth), r"True", "ERR: Login did not return True")

class TC07_compromised_pwd_check_in_dmz(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77831"
    description = show_testcase_info(Parameter.TESTPLAN, '4405977', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405977')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("-------Radius Auth---------")
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-user-login-with-external-auth','enable',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button not enabled")

    def test_03_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "test", "password")
        Assertion.assert_equal(
            result["status"],
            "FAIL_ACCESS_DENIED",
            "ERR: Login should be blocked when compromised password check is enabled.")

class TC08_compromised_pwd_check_in_dmz(Test):
    # CLI Case
    uuid = "SOSAIOT-TC-77830"
    description = show_testcase_info(Parameter.TESTPLAN, '4405976', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405976')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("-------Radius Auth---------")
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','no block-user-login-with-external-auth',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button failed to disable")

    def test_03_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "test", "password")

        Assertion.assert_equal(result["status"],"SUCCESS_WITH_WARNING",
            "ERR: Login should succeed with warning when block-user-login-with-external-auth is disabled.")

# FOR TACACS USER
class TC09_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77837"
    description = show_testcase_info(Parameter.TESTPLAN, '4405985', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405985')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Select Tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_settings.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": True
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": true,', "failed to enable toggle button")

    def test_03_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'user1', 'password')
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_regular(is_auth,
                                 r"(?i)the password is one that is known to have possibly been compromised, it must be changed before you can log in",
                                 "ERR: Compromised password message not found")


class TC10_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77836"
    description = show_testcase_info(Parameter.TESTPLAN, '4405984', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405984')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Select Tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_settings.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,  # usually this must be True to apply sub-options
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,',
                                 "failed to disable toggle button")

    def test_03_user_login(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.X2_IP, 'user1', 'password')
        time.sleep(10)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_regular(str(is_auth), r"True", "ERR: Login did not return True")

class TC11_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77835"
    description = show_testcase_info(Parameter.TESTPLAN, '4405981', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405981')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Select Tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_settings.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','block-user-login-with-external-auth','enable',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button not enabled")

    def test_03_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "user1", "password")
        Assertion.assert_equal(
            result["status"],
            "FAIL_ACCESS_DENIED",
            "ERR: Login should be blocked when compromised password check is enabled.")

class TC12_compromised_pwd_check_in_dmz(Test):
    uuid = "SOSAIOT-TC-77834"
    description = show_testcase_info(Parameter.TESTPLAN, '4405980', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4405980')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Select Tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_settings.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
            flag = False
            logger.info('Enable user login with external auth toggle button')
            commands = ['con', 'user authentication','credential-auditor', 'enable','no block-user-login-with-external-auth',
                        'commit', 'exit']
            rc = fw_cli_dmz.do_cli_commands(commands, tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flag = True
            Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button failed to disable")

# While configuring TACACS Server under TACACS Users => Use LDAP to retrieve user group information is selected by default hence we are using LDAP User "test"
    def test_03_user_login_via_Cli(self):
        result = verify_connection_remote("-PC1", Parameter.X2_IP, "test", "password")

        Assertion.assert_equal(result["status"],"SUCCESS_WITH_WARNING",
            "ERR: Login should succeed with warning when block-user-login-with-external-auth is disabled.")






































