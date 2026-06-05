import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Force_password_change_on_First_Login_2/')

from definition.settings import *
wan_url = "https://13.0.0.100"

class Admin_NonTC(Test):
    uuid = "NonTc"
    
    def test_01_credential_auditor_disable_api(self):
            json_obj = {
                "user": {
                    "auth": {
                        "credential_auditor": {
                            "enable": False,  
                            "block_user_login_with_external_auth": False
                        }
                    }
                }
            }
            resp = user_setting.user_settings_base(**json_obj)
            Assertion.assert_equal(resp, True, "ERR: testcase failed")
            res = user_setting.show_user_setting()
            Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,', "failed to disable toggle button")


class TC00_SSLVPN_config(Test):
    uuid = 'NonTC'

    def test_01_install_nx_Linux_remote(self):
        cpy_build = cp_nx.buildnx_linux_remote('-PC2')
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux_remote('-PC2')
        logger.info(inst)

    def test_02_create_sslvpn_address_object(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.10,192.168.168.20"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_range", "ipv4")
        Assertion.assert_regular(json.dumps(resp1),'"name": "sslvpn_range"', "Err: failed to create address object")

    def test_03_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
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
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

    def test_04_enable_server_access(self):
        enable = {
            'WAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_05_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(4)
    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('WAN', 'LAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Trusted Users"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Trusted Users"','err: access rules not updated.')

def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()

def install_nxlinux(username, password, netexurl, domain):
        netexsession = pexpect.spawn("netExtender", ["-u", username, "-p", password, "-d", domain, netexurl])
        logger.info("The netextender session".format(netexsession))
        index = netexsession.expect(["Do you want to proceed", pexpect.EOF, pexpect.TIMEOUT])
        time.sleep(5)
        if index == 0:
            logger.info("Received self-signed certificate override")
            netexsession.sendline("Y")
            logger.info("Successfully accepted the self-signed and trying to connect via NetExtender")
        else:
            logger.info("Error: Unable to connect via NetExtender as Authentication Failed")
            # continue
        time.sleep(15)
        index = netexsession.expect(["NetExtender connected successfully", pexpect.EOF, pexpect.TIMEOUT])
        time.sleep(50)
        if index == 0:
            logger.info("Successfully connected via NetExtender ")
        else:
            logger.info("SSLVPN not enabled in your zone. unable to connect ")

        return index

def change_pw_of_user_from_nx(user, pswd, new_pswd, netexurl, domain, openstack_PC):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        print(hostname)
        username = "root"
        password = "password"
        pc_login = s.login(hostname, username, password)
        print("Successfully login to:" + hostname)
        s.prompt()  # match the prompt
        print(s.before)  # print everything before the prompt.
        s.sendline('killall netExtender')
        s.prompt()
        print(s.before)
        s.sendline('netExtender')
        s.prompt()
        print(s.before)
        print("SSLVPN SERVER:" + netexurl)
        s.sendline(netexurl)
        s.prompt()
        print(s.before)
        print("User Authentication")
        print("User:" + user)
        s.sendline(user)
        s.prompt()
        print(s.before)
        print("Password:")
        s.sendline(pswd)
        s.prompt()
        print(s.before)
        print("Domain:" + domain)
        s.sendline("LocalDomain")
        s.sendline('Yes')
        time.sleep(5)
        s.prompt()
        time.sleep(30)
        print(s.before)
        s.sendline('Yes')
        s.prompt()
        print(s.before)
        print("Current password:" + pswd)
        s.sendline(pswd)
        s.prompt()
        s.sendline(new_pswd)
        print("new password:" + new_pswd)
        s.prompt()
        s.sendline(new_pswd)
        print("re enter new password:" + new_pswd)
        s.sendline('Yes')
        s.prompt()
        print(s.before)
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)

def connect_nxlinux_remote(user, pswd, netexurl, domain, openstack_PC):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        print(hostname)
        username = "root"
        password = "password"
        pc_login = s.login(hostname, username, password)
        print("Successfully login to:" + hostname)
        s.prompt()  # match the prompt
        print(s.before)  # print everything before the prompt.
        s.sendline('killall netExtender')
        s.prompt()
        print(s.before)
        s.sendline('netExtender')
        s.prompt()
        print(s.before)
        print("SSLVPN SERVER:" + netexurl)
        s.sendline(netexurl)
        s.prompt()
        print(s.before)
        print("User Authentication")
        print("User:" + user)
        s.sendline(user)
        s.prompt()
        print(s.before)
        print("Password:")
        s.sendline(pswd)
        s.prompt()
        print(s.before)
        print("Domain:" + domain)
        s.sendline("LocalDomain")
        s.sendline('Yes')
        time.sleep(5)
        s.prompt()
        print(s.before)
        time.sleep(50)

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)

def test_ppp_check(openstack_PC):
    ip_pc = Params.testbed + openstack_PC
    logger.info(ip_pc)
    PC_login = Host(ip_pc, user='root', password='P@ssw0rd')
    logger.info(PC_login)
    time.sleep(160)
    ppp = PC_login.send_command("ifconfig | grep ppp0")
    if (len(ppp) == 0):
        logger.info("NX is Connected")
        return False
    else:
        logger.info("NX disconected successfuly")
        return True
    time.sleep(10)
 

class TC01_Local_User(Test):  
    uuid = "SOSAIOT-TC-75385"
    description = show_testcase_info(Parameter.TESTPLAN, '1508768', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508768')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test9",
            "userpassword": "P@ssw0rd",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_user_by_name("test9")  
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 

        add_localuser = {
            "action": "add",
            "username": "test1",
            "userpassword": "P@ssw0rd",
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_user_by_name("test1") 
        Assertion.assert_regular(json.dumps(response_get), '"force_password_change": false,', 'err: Failed to enable ') 


        add_localuser = {
            "action": "add",
            "username": "test2",
            "userpassword": "P@ssw0rd",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_user_by_name("test2") 
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 


    def test_02_login_user1(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test9', 'P@ssw0rd')
        uiobj.login_ui_pwd_change('P@ssw0rd', G_PASSWORD_NEW)
        time.sleep(10)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test9"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")

        time.sleep(10)
    

    def test_03_login_user2(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test1', 'P@ssw0rd')
        time.sleep(10)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test1"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")

        time.sleep(10)



    def test_04_login_user3(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test2', 'P@ssw0rd')
        uiobj.login_ui_pwd_change('P@ssw0rd', G_PASSWORD_NEW)
        time.sleep(10)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test2"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")
 

    # logout user
    def test_05_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")


    def test_06_show_local_user(self):
        response = local_user.show_local_user_by_name("test9")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": false', 'err: Failed to enable ')

        res = local_user.show_local_user_by_name("test2")
        Assertion.assert_regular(json.dumps(res), '"force_password_change": false', 'err: Failed to enable ')


class TC02_Local_User(Test):
    uuid = "SOSAIOT-TC-75389"
    description = show_testcase_info(Parameter.TESTPLAN, '1508772', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508772')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test3",
            "userpassword": "P@ssw0rd",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test3") 
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 


    def test_02_login_user(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test3', 'P@ssw0rd')
        uiobj.login_ui_pwd_change('P@ssw0rd', G_PASSWORD_NEW)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test3"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_03_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_04_show_local_user(self):
        response = local_user.show_local_user_by_name("test3")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": false', 'err: Failed to enable ')  

    def test_05_login_user_again(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test3', G_PASSWORD_NEW)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test3"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")

    # logout user
    def test_06_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")
        

class TC03_Local_User(Test):
    jira = 'GEN8-10547'
    uuid = "SOSAIOT-TC-75387"
    description = show_testcase_info(Parameter.TESTPLAN, '1508770', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508770')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test5",
            "userpassword": "P@ssw0rd",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test5") 
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 


    def test_02_login_user(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test5', 'P@ssw0rd')
        uiobj.login_ui_pwd_change('P@ssw0rd', G_PASSWORD_NEW)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test5"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_03_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_04_show_local_user(self):
        response = local_user.show_local_user_by_name("test5")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": false', 'err: Failed to enable ')  
    
    @repeat_method(3)
    def test_05_login_user_again(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test5', G_PASSWORD_NEW)
        uiobj.change_pw_voluntarily(G_PASSWORD_NEW, 'P@ssw0rd')

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test5"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_06_logout_and_login_with_new_password(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

        # login_ui and check with changed password
        uiobj.login_ui(wan_url, 'test5', 'P@ssw0rd')

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test5"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_06_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")


class TC04_Local_User(Test):
    uuid = "SOSAIOT-TC-75386"
    description = show_testcase_info(Parameter.TESTPLAN, '1508769', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508769')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_acceptance_policy(self):
        ob_json = {
            'policy_banner_before_login': True,
            "pocontent": "Welcome to SONICWALL Firewall"
        }
        response = user_setting.customization(**ob_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"policy_banner_before_login": true,', 'err: edit user setting failed ') 

    def test_02_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test_user",
            "userpassword": "P@ssw0rd",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test_user") 
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 

    def test_03_login_user(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.accept_acceptable_policy(wan_url, 'test_user', 'P@ssw0rd')
        uiobj.login_ui_pwd_change('P@ssw0rd', G_PASSWORD_NEW)

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test_user"', 'failed to get user status') 
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_05_show_local_user(self):
        response = local_user.show_local_user_by_name("test_user")
        Assertion.assert_regular(json.dumps(response), '"force_password_change": false', 'err: Failed to enable ')  

    def test_06_disable_acceptance_policy(self):
        ob_json = {
            'policy_banner_before_login': False
        }
        response = user_setting.customization(**ob_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")


class TC05_Local_User(Test):
    uuid = "SOSAIOT-TC-75388"
    description = show_testcase_info(Parameter.TESTPLAN, '1508771', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508771')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_password_restrictions(self):
        obj_json = {
            "administration": {
                "password": {
                    "enforce_character_difference": True,
                    "minimum_length": 8,
                    "complexity": {
                        "type": "alpha-and-numeric",
                        "upper_case": 1,
                        "lower_case": 1,
                        "digital": 1
                    }
                },
                "constraints_apply_to": {
                    "builtin_admin": False,
                    "full_admins": False,
                    "limited_admins": False,
                    "local_users": True,
                    "guest_admins": False,
                }
            }
        }
        response = admin_setting.conf_admin_update(**obj_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = admin_setting.show_admin_setting()
        Assertion.assert_equal(resp['administration']['password']['complexity']['type'], 'alpha-and-numeric', 'err: edit admin setting failed ') 

    def test_02_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test4",
            "userpassword": "SoNic1234",
            "force_password_change": True,
            "member_of": ["Trusted Users"],
          }
         
        response = local_user.local_user(**add_localuser)
        logger.info(response) 
        response_get = local_user.show_local_user_by_name("test4") 
        # Assertion.assert_regular(json.dumps(response_get), '"force_password_change": true,', 'err: Failed to enable ') 

    def test_03_login_user(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui(wan_url, 'test4', 'SoNic1234')
        uiobj.login_ui_pwd_change('SoNic1234', 'password')
        out = uiobj.verify_warning_message()
        Assertion.assert_equal(out, True, "ERR: testcase failed")

        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "test4"', 'failed to get user status') 
        Assertion.assert_not_regular(json.dumps(status), '13.0.0.3', "failed to get user status")

    # logout user
    def test_04_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_05_show_local_user(self):
        response = local_user.show_local_user_by_name("test4")
        # Assertion.assert_regular(json.dumps(response), '"force_password_change": true', 'err: Failed to enable ')

    def test_06_disable_password_restrictions(self):
        obj_json = {
            "administration": {
                "password": {
                    "enforce_character_difference": True,
                    "minimum_length": 8,
                    "complexity": {}
                },
                "constraints_apply_to": {
                    "builtin_admin": True,
                    "full_admins": True,
                    "limited_admins": True,
                    "local_users": True,
                    "guest_admins": True,
                }
            }
        }
        response = admin_setting.conf_admin_update(**obj_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = admin_setting.show_admin_setting()
        Assertion.assert_equal(resp['administration']['password']['complexity'], {}, 'err: edit admin setting failed ') 


class TC06_Local_User(Test):
    uuid = "SOSAIOT-TC-77105"
    description = show_testcase_info(Parameter.TESTPLAN, '1508773', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508773')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_02_config_ldapuser(self):
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

    def test_03_import_ldap_user(self):
        add = {
            "user": {
                "local": {
                    "user": [{
                        "name": "changepassword1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**add)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "changepassword1"', 'err: Failed to create localuser')  

    @repeat_method(3)
    def test_04_login_user(self):
        flag = None
        ui_obj = None

        ui_obj = fw_ui_obj.user_login('13.0.0.100', 'changepassword1', 'password')
        if '"message": "Incorrect name/password. 2 more login attempts before lockout."'or '"message": "Incorrect name/password. 1 more login attempts before lockout."' or '"message": "Incorrect name/password' in ui_obj:
            flag = True      
        else:
            flag= False

        Assertion.assert_equal(flag, True, "ERR: error not displaying")

    # logout user
    def test_05_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_06_show_local_user(self):
        response = local_user.show_local_users_by_domain_name("changepassword1", "os-autosnwl.com")
        # Assertion.assert_regular(json.dumps(response), '"force_password_change": true', 'err: Failed to enable ')

    def test_07_delete_ldap_user(self):
        rc = local_user.delete_local_user_with_domain("changepassword1", "os-autosnwl.com")
        Assertion.assert_equal(rc, True, "ERR: delete ldap user failed")


class TC07_Local_User(Test):
    uuid = "SOSAIOT-TC-75390"
    description = show_testcase_info(Parameter.TESTPLAN, '1508774', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508774')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
        user_auth = {
                "auth_method": "radius",
                "sso_agent": False,
                "terminal_services_agent": False,
                "radius_accounting": False,
                "third_party_api": False,
                "capture_client": False
            }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"', "ERR:Failed to select Local authentication method.")

    def test_01_add_radius_server(self):
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
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to create radius server')

    def test_03_import_radius_user(self):
        import_radius = {
            "user": {
                "local": {
                    "user": [{
                        "name": "changepassword1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_radius)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "changepassword1"', 'err: Failed to create localuser')  

    @repeat_method(3)
    def test_04_login_user(self):
        flag = None
        ui_obj = None

        ui_obj = fw_ui_obj.user_login('13.0.0.100', 'changepassword1', 'password')
        if '"message": "Incorrect name/password. 2 more login attempts before lockout."'or '"message": "Incorrect name/password. 1 more login attempts before lockout."' or '"message": "Incorrect name/password' in ui_obj:
            flag = True      
        else:
            flag= False

        Assertion.assert_equal(flag, True, "ERR: error not displaying")

    # logout user
    def test_05_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_06_show_local_user(self):
        response = local_user.show_local_users_by_domain_name("changepassword1", "os-autosnwl.com")
        # Assertion.assert_regular(json.dumps(response), '"force_password_change": true', 'err: Failed to enable ')

    def test_07_delete_ldap_user(self):
        rc = local_user.delete_local_user_with_domain("changepassword1", "os-autosnwl.com")
        Assertion.assert_equal(rc, True, "ERR: delete ldap user failed")


class TC08_Local_User(Test):
    uuid = "SOSAIOT-TC-75383"
    description = show_testcase_info(Parameter.TESTPLAN, '1508766', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508766')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_02_config_ldapuser(self):
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
                'bind_password': 'P@ssw0rd',
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

    def test_03_import_ldap_user(self):
        add = {
            "user": {
                "local": {
                    "user": [{
                        "name": "changepassword1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**add)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "changepassword1"', 'err: Failed to create localuser')  
    
    def test_04_edit_ldap_user(self):
        add_localuser = {
            "action": "edit",
            "username": "changepassword1",
            "userpassword": "P@ssw0rd",
            "oldusername": "changepassword1",
            "force_password_change": True,
            "domain":"os-autosnwl.com",
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            'vpn_client_access': ['WAN Subnets']
          }
         
        response = local_user.local_user(**add_localuser) 
        Assertion.assert_equal(response, True, "ERR: edit ldap user failed") 

    # @repeat_method(3)
    # def test_05_change_password_for_ldap_user_from_while_login_to_nx(self):
    #     run_io_tasks_in_parallel([
    #         lambda: change_pw_of_user_from_nx(user='changepassword1', pswd='P@ssw0rd', new_pswd=G_PASSWORD_NEW, netexurl='13.0.0.100:4433',
    #                                        domain='LocalDomain', openstack_PC='-PC2'),
    #         lambda: test_ppp_check(openstack_PC='-PC2')])
        
    # @repeat_method(3)
    # def test_06_verify_nx_from_WAN(self):
    #     run_io_tasks_in_parallel([
    #         lambda: connect_nxlinux_remote(user='changepassword1', pswd=G_PASSWORD_NEW, netexurl='13.0.0.100:4433',
    #                                        domain='LocalDomain', openstack_PC='-PC2'),
    #         lambda: test_ppp_check(openstack_PC='-PC2')])
    #     # check user status
    #     status = user_status.show_user_status()
        # Assertion.assert_regular(json.dumps(status), '"name": "changepassword1"', "failed to get user status")

    # logout user
    def test_07_logout(self):
        rc = local_user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def test_08_show_local_user(self):
        response = local_user.show_local_users_by_domain_name("changepassword1", "os-autosnwl.com")
        # Assertion.assert_regular(json.dumps(response), '"force_password_change": true', 'err: Failed to enable ')

    def test_09_delete_ldap_user(self):
        rc = local_user.delete_local_user_with_domain("changepassword1", "os-autosnwl.com")
        Assertion.assert_equal(rc, True, "ERR: delete ldap user failed")