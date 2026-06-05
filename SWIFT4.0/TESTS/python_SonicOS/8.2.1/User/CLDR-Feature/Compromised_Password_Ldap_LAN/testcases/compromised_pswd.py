import sys
import os
import json
import re
import pexpect
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/Compromised_Password_Ldap_LAN/')

from definition.settings import *
from definition.conf_fw import *
from pexpect import pxssh

def verify_connection_remote(openstack_PC, ip,username_fw, password_fw):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        logger.info(hostname)
        username = "root"
        password = "password"
        pc_login = s.login(hostname, username, password)
        logger.info("Successfully login to:" + hostname)
        s.prompt()
        logger.info(s.before)
        s.sendline('ssh ' + username_fw + '@' + ip + '')
        s.prompt()
        logger.info(s.before)
        s.sendline(password_fw)
        s.prompt()
        logger.info(s.before)
        output = s.before.decode('utf-8')
        return output
    except pxssh.ExceptionPxssh as e:
        logger.info("pxssh failed on login.")
        logger.info(e)

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
                'distinguished_name': 'test',
                'bind_password': 'password',
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
        logger.info("Radius Config")
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

    def test_05_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = Tacacs_user.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs user test got failed")

    def test_06_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")

    def test_07_Enable_Credential_Auditor(self):
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

    def test_08_LDAP_Users_AdminPrivelage(self):
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

    def test_09_disable_password_restrictions(self):
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



def credential_auditor_enable_cli(self):
    flag = False
    logger.info('Enable user login with external auth toggle button')
    commands = ['config', 'user authentication','credential-auditor', 'enable','block-user-login-with-external-auth','enable',
                'commit', 'exit']
    rc = fw_cli.do_cli_commands(commands, tag=1)
    if "Changes made" in rc[1] or "changes made" in rc[1]:
        flag = True
    Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button not enabled")

def credential_auditor_disable_cli(self):
    flag = False
    logger.info('Enable user login with external auth toggle button')
    commands = ['config', 'user authentication','credential-auditor', 'enable','no block-user-login-with-external-auth',
                'commit', 'exit']
    rc = fw_cli.do_cli_commands(commands, tag=1)
    if "Changes made" in rc[1] or "changes made" in rc[1]:
        flag = True
    Assertion.assert_equal(flag, True, "ERR: user login with external auth toggle button not enabled")

def credential_auditor_enable_api(self):
    json_obj = {
        "user": {
            "auth": {
                "credential_auditor": {
                    "enable": True,  
                    "block_user_login_with_external_auth": True
                }
            }
        }
    }
    resp = user_settings.user_settings_base(**json_obj)
    Assertion.assert_equal(resp, True, "ERR: testcase failed")
    res = user_settings.show_user_setting()
    Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": true,', "failed to enable toggle button")

def credential_auditor_disable_api(self):
    json_obj = {
        "user": {
            "auth": {
                "credential_auditor": {
                    "enable": True,  
                    "block_user_login_with_external_auth": False
                }
            }
        }
    }
    resp = user_settings.user_settings_base(**json_obj)
    Assertion.assert_equal(resp, True, "ERR: testcase failed")
    res = user_settings.show_user_setting()
    Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,', "failed to disable toggle button")

def enable_cli_login(self):
    output = verify_connection_remote(openstack_PC = "-PC1", ip= Parameter.FIREWALL, username_fw="test", password_fw= "password")
    Assertion.assert_regular(output, "The password that you have entered is one that is known to have possibly been compromised, it must be changed before you can log in",
                            "ERR: Expected Error is not displayed")

def disable_cli_login(self):
    output = verify_connection_remote(openstack_PC = "-PC1", ip= Parameter.FIREWALL, username_fw="test", password_fw= "password")
    Assertion.assert_regular(output, "The password that you have entered is one that is known to have possibly been compromised, you should change it",
                            "ERR: Expected Error is not displayed")
    
def enable_api_login(self):
    is_auth, bearer_token = Local_User.local_user_login()
    Assertion.assert_regular(str(is_auth), "false", "ERR: Compromised password message not found")
    
def disable_api_login(self):
    is_auth, bearer_token  = Local_User.local_user_login()
    Assertion.assert_regular(str(is_auth), r"True", "ERR: Login did not return True")
    


# -------------------------------------------------------------------CLI TESTCASES-----------------------------------------------------------------

# LDAP        
class TC01_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77779"
    description = show_testcase_info(Parameter.TESTPLAN, '4113567', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113567')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:LDAP method is not selected successfully")
        
    def test_02_Block_User_Login_With_External_Auth(self):
        turn_on = credential_auditor_enable_cli(self)
        return turn_on

    def test_03_user_login_via_Cli(self):
        rc = enable_cli_login(self)
        return rc

class TC02_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77778"
    description = show_testcase_info(Parameter.TESTPLAN, '4113566', description=True)['title']
        
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113566')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
            user_auth = {
                "auth_method": "ldap",
            }
            ldap_auth = user_settings.user_method_authentication(**user_auth)
            resp = user_settings.show_user_auth()
            Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:LDAP method is not selected successfully")

    def test_02_Block_User_Login_With_External_Auth(self):
        turn_off = credential_auditor_disable_cli(self)
        return turn_off

    def test_03_user_login_via_Cli(self):
        rc = disable_cli_login(self)
        return rc


#RADIUS 
class TC03_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77781"
    description = show_testcase_info(Parameter.TESTPLAN, '4113569', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113569')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_radius(self):
        user_auth = {
            "auth_method": "radius",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"', "ERR:LDAP method is not selected successfully")
        
    def test_02_Block_User_Login_With_External_Auth(self):
        turn_on = credential_auditor_enable_cli(self)
        return turn_on
    
    def test_03_user_login_via_Cli(self):
        rc = enable_cli_login(self)
        return rc
        

class TC04_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77780"
    description = show_testcase_info(Parameter.TESTPLAN, '4113568', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113568')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_radius(self):
        user_auth = {
            "auth_method": "radius",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"', "ERR:LDAP method is not selected successfully")
        
    def test_02_Block_User_Login_With_External_Auth(self):
        turn_off = credential_auditor_disable_cli(self)
        return turn_off
    
    @repeat_method(9)
    def test_03_user_login_via_Cli(self):
        rc = disable_cli_login(self)
        return rc

# TACACS
class TC05_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77783"
    description = show_testcase_info(Parameter.TESTPLAN, '4113571', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113571')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_tacacs(self):
        user_auth = {
            "auth_method": "tacacs",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"', "ERR:LDAP method is not selected successfully")
        
    def test_02_Block_User_Login_With_External_Auth(self):
        turn_on = credential_auditor_enable_cli(self)
        return turn_on

    def test_03_user_login_via_Cli(self):
        rc = enable_cli_login(self)
        return rc

class TC06_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77782"
    description = show_testcase_info(Parameter.TESTPLAN, '4113570', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113570')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_tacacs(self):
        user_auth = {
            "auth_method": "tacacs",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"', "ERR:LDAP method is not selected successfully")
        
    def test_02_Block_User_Login_With_External_Auth(self):
        turn_off = credential_auditor_disable_cli(self)
        return turn_off

    def test_03_user_login_via_Cli(self):
        rc = disable_cli_login(self)
        return rc
        

# -----------------------------------------------------------API -TESTCASES-------------------------------------------------------------------

#LDAP 
class TC07_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77785"
    description = show_testcase_info(Parameter.TESTPLAN, '4113575', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113575')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:LDAP method is not selected successfully")

    def test_02_Block_User_Login_With_External_Auth(self):
        turn_on = credential_auditor_enable_api(self)
        return turn_on

    def test_03_user_login(self):
        rc = enable_api_login(self)
        return rc
        
class TC08_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77784"
    description = show_testcase_info(Parameter.TESTPLAN, '4113574', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113574')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
        }
        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:LDAP method is not selected successfully")

    def test_02_Block_User_Login_With_External_Auth(self):
        turn_off = credential_auditor_disable_api(self)
        return turn_off
    
    def test_03_user_login(self):
        rc = disable_api_login(self)
        return rc


#RADIUS
class TC09_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77787"
    description = show_testcase_info(Parameter.TESTPLAN, '4113577', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113577')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("Radius Auth")
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
        turn_on = credential_auditor_enable_api(self)
        return turn_on

    def test_03_user_login(self):
        rc = enable_api_login(self)
        return rc

class TC10_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77786"
    description = show_testcase_info(Parameter.TESTPLAN, '4113576', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113576')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        logger.info("Radius Auth")
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
        turn_off = credential_auditor_disable_api(self)
        return turn_off

    def test_03_user_login(self):
        rc = disable_api_login(self)
        return rc


#TACACS
class TC11_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77789"
    description = show_testcase_info(Parameter.TESTPLAN, '4113579', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113579')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Tacacs auth')
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
        turn_on = credential_auditor_enable_api(self)
        return turn_on

    def test_03_user_login(self):
        rc = enable_api_login(self)
        return rc


class TC12_compromised_pswd_lan(Test):
    uuid = "SOSAIOT-TC-77788"
    description = show_testcase_info(Parameter.TESTPLAN, '4113578', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4113578')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_tacacs_user_auth_method(self):
        logger.info('Tacacs auth')
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"', "ERR:Failed to select Local authentication method.")

    def test_02_Block_User_Login_With_External_Auth(self):
        turn_off = credential_auditor_disable_api(self)
        return turn_off

    def test_03_user_login(self):
        rc = disable_api_login(self)
        return rc




