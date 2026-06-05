import sys
import os
import json
import re
import time

from definition.settings import *
from runner.settings import logger

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2')
headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])

# create SSLVPN service for user portal login
class sslvpn_config(Test):
    uuid = 'NonTC'

    def test_01_install_nx_Linux(self):
        cpy_build = cp_nx.cpbuildnx_linux_local()
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux()
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
            'LAN_enable': True,
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

    def test_06_add_sslvpn_user(self):
        add_localuser = {
            "action": "add",
            "username": "test",
            "userpassword": "P@ssw0rd",
            "lifetype": "days",
            "accountlifetime": 3,
            "prune_on_expiry": True

        }
        resp = local_user.local_user(**add_localuser)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test"', 'err: test not created')

    def test_07_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'P@ssw0rd',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','Guest Services']
        }
        resp = local_user.user_member_of(**member)
        resp1 = local_user.show_local_user_by_name('test')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')

    def test_08_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:LOCALs method is not selected successfully")

# Create Guest User
class create_guest_user(Test):
    uuid = "1529402"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_guestuser_account(self):
        add_guestuser_account = {
            'action': 'add',
            'accountname': 'guestuser_FW',
            'password': "password",
            'activate_on_login': True,
            'enable_guest_service_privilege': False,
        }
        response = guest_user.user_guest_account(**add_guestuser_account)
        logger.info(response)
        response_get = guest_user.show_user_guest_account_by_name("guestuser_FW")
        Assertion.assert_regular(json.dumps(response_get), '"name": "guestuser_FW"',
                                 'err: Failed to create guest users account')
        logger.info("Guest user created")

# edit the guest user
class Guest_UserEdit(Test):
    uuid = "1529399"
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_guestuser_account(self):
        add_guestuser_account = {
          'action': 'add',
          'accountname': 'guestuser',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': False,
          }
        response=guest_user.user_guest_account(**add_guestuser_account)
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name("guestuser")
        Assertion.assert_regular(json.dumps(response_get), '"name": "guestuser"', 'err: Failed to create guest users account')
        logger.info("Guest user created")

    def test_02_edit_guest_user(self):
        add_guestuser_account = {
            'action': 'edit',
            'accountname': 'guestuser',
            'password': "password",
            'activate_on_login': True,
            'enable_guest_service_privilege': True,

        }
        response = guest_user.user_guest_account(**add_guestuser_account)
        logger.info(response)
        response_get=guest_user.show_user_guest_account_by_name("guestuser")
        Assertion.assert_regular(json.dumps(response_get), '"name": "guestuser"', "err: Failed to edit guest user profile")
        logger.info("Guest user edited")

# Delete guest user
class delete_all_guest_user(Test):
    uuid = "1529390"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_add_guest_user(self):
        add_guestuser_account = {
            'action': 'add',
            'accountname': 'guestuser123',
            'password': "password",
            'activate_on_login': True,
            'enable_guest_service_privilege': False,
        }
        logger.info(" {} ".center(20, '-').format('add guest user'))
        rc = guest_user.user_guest_account(**add_guestuser_account)
        Assertion.assert_equal(rc, True, f"ERR: add guest user failed")
        logger.info("guest user added")

    def test_02_delete_guest_user(self):
        logger.info(" {} ".center(20, '-').format('delete guest user'))
        rc = guest_user.del_user_guest_account(accountname='guestuser123')
        Assertion.assert_equal(rc, True, f"ERR: delete guest user failed")
        logger.info("Guest user deleted")

    def test_03_check_guest_user_list(self):
        logger.info(" {} ".center(20, '-').format('check guest user list'))
        res = guest_user.show_user_guest_account()
        if "'name': 'guest123'" not in str(res):
            rc = True
        else:
            rc = False
            logger.info(res)
        Assertion.assert_equal(rc, True, f"ERR: check guest user list failed")
        logger.info("User not there, verified")

# local user guest service with WGS
class local_user_guest_service_WGS(Test):
    uuid = "1529400"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_zone_enable(self):
        enable_zone = {
            "zones": [
                {
                    "name": "Test",
                    "security_type": "wireless",
                    "interface_trust": True,
                    "auto_generate_access_rules":
                    {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": True,
                        "inter_guest": False,
                        "external_auth": {
                            "enable": False,
                            "client_redirect": "https",
                            "web_server_1": {},
                            "web_server_2": {},
                            "web_server": {
                                "timeout": 15
                            }
                        }
                        },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        rc = zone_obj.add_zone_object(**enable_zone)
        Assertion.assert_equal(rc, True, "ERR: enabling WLAN guest service failed")
        logger.info("enabling WLAN guest service")

    # @repeat_method(10)
    def test_02_portal_page_access(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2/definition/ui_user.py ' + '-url ' + url + ' -user test -pwd P@ssw0rd'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test"', "failed to get user status")
        logger.info("User status is visible")

# remove the guest service from local user and login should fail
class edit_local_user_guest_service(Test):
    uuid = "1529389"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')


    # @repeat_method(10)
    def test_01_portal_page_access(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2/definition/ui_user.py ' + '-url ' + url + ' -user test -pwd P@ssw0rd'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "test"', "failed to get user status")
        logger.info("User status is visible")
        user_status.user_logout_by_admin("test")
        static_client.send_command('pkill firefox')
        time.sleep(60)
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "test"', "failed to get user status")

    def test_02_edit_local_user(self):
        add_localuser = {
            "action": "edit",
            "username": "test",
            "userpassword": "P@ssw0rd",
            "member_of": [],
        }
        response = local_user.local_user(**add_localuser)
        logger.info(response)
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test"', 'err: Failed to create localuser')
        logger.info("Removing member of local user successeful")

    def test_03_portal_page_access(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Guest_Users_TP349_2/definition/ui_user.py ' + '-url ' + url + ' -user test -pwd P@ssw0rd'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "test"', "failed to get user status")
        logger.info("User status is Not visible")

# Performance file export import
class guest_user_in_prefs_file(Test):
    uuid = "1529391"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_guest_user(self):
        add_guestuser_profile = {
            'action': 'add',
            'profilename': 'guestuser_export',
            'generate': True,
            'generatename': True,
            'generatepassword': False,
            'activate_on_login': True,
            'enable_account': True,
            'login_uniqueness': False,
            'account_lifetime': False,
            'acco_lifetime': 2,
            'acco_lifetype': 'days'
        }
        response = guest_user.user_guest_profile(**add_guestuser_profile)
        logger.info(response)

    def test_02_export_exp(self):
        resp = setting.export_setting_exp(filepath='/tmp/testguestuser.exp')
        Assertion.assert_equal(resp, True, "failed to export the configuration")
        logger.info("Exported successfully")

    def test_03_import_performance_file(self):
        # FW boot in factory default mode
        boot_fw = setting.boot_fw(2)
        Assertion.assert_equal(boot_fw, True, "ERR: Boot current firmware with factory default settings fail.")
        # import preference file after factory default mode
        rc2 = setting.import_setting_exp(filepath='/tmp/testguestuser.exp')
        Assertion.assert_equal(rc2, True, "Error: Failed to import the settings...")
        response_get = guest_user.show_user_guest_profile_by_name("guestuser_export")
        Assertion.assert_regular(json.dumps(response_get), '"name": "guestuser_export"',
                                 'err: Failed to create guest users profile')
        logger.info("guestuser_export,  user successfully imported")

# verify remaining session time
class guest_user_session(Test):
    uuid = "1529393"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'Testp@ssw0rd',
            'member_of': ['Guest Administrators'],
            'account_lifetime': True,
            'accountlifetime': 50,
            'lifetype': 'minutes',
            'prune_on_expiry': True,
            'quota_cycle': 'minutes',
            'session_lifetime': True,
            'sessionlifetime': 3,
            'sessionlifetimetype': 'minutes',

        }
        post_resp = local_user.local_user(**user_json)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test1"', 'err: test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: test1 not created')

    def test_02_interface(self):
        dict1 = {
            'if': 'X0',
            'zone': 'LAN',
            'mgmt_https': True,
            'user_https': True,
            'ip': '192.168.168.168',
            "netmask": "255.255.255.0",
            "gateway": "0.0.0.0"
        }

        post_resp = configure_user.config_interface(**dict1)
        resp_get = configure_user.get_interface_status('X0')
        Assertion.assert_regular(json.dumps(resp_get), '"https": true', "err:failed")

    def test_02_guest_user_login_and_logout(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test1', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        logger.info(bearer_token)
        for remaining in range(60, 0, -1):
            sys.stdout.write(f"\rWaiting for {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)  # Sleep for 1 min
        sys.stdout.write("\rTime's up! \n")

    def test_03_session_details(self):
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test1"', 'err: Failed to create localuser')
        Assertion.assert_not_regular(json.dumps(response_get), '"minutes": 50', 'err: Failed to create localuser')
        logger.info("************************************")
        logger.info(response_get)
        logger.info("***********************************")

# reboot and verify the guest user session details
class guest_user_session_after_reboot(Test):
    uuid = "1529394"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_reboot_FW(self):
        res = restartapi.restart_now()
        # Assertion.assert_equal(res, True, "ERR: Restart DUT failed")
        time.sleep(10)

    def test_02_session_details(self):
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test1"', 'err: Failed to find localuser')
        Assertion.assert_not_regular(json.dumps(response_get), '"minutes": 50', 'err: Failed to find localuser')
        logger.info("************************************")
        logger.info(response_get)
        logger.info("***********************************")

# login when session time out remaining
class check_login_with_remaining_session_expiration_time(Test):
    uuid="1529395"
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_guest_user_login_and_logout(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test1', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        logger.info(bearer_token)
        for remaining in range(120, 0, -1):
            sys.stdout.write(f"\rWaiting for {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)  # Sleep for 1 second
        sys.stdout.write("\rTime's up! \n")

    def test_02_session_details(self):
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test1"', 'err: Failed to create localuser')
        Assertion.assert_not_regular(json.dumps(response_get), '"minutes": 30', 'err: Failed to create localuser')
        logger.info("************************************")
        logger.info(response_get)
        logger.info("***********************************")

    def test_03_guest_user_relogin(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test1', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, False, 'err:Login was sucessful')

# login with account time out remaining
class login_after_account_timeout_remaining(Test):
    uuid= "1529396"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_session_details(self):
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "test1"', 'err: Failed to create localuser')
        logger.info("Account remaining as account time out time still remaining")

    def test_02_guest_user_login(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test1', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, False, 'err:Login was sucessful')
        logger.info("Login failed")

# login once account timed out
class login_after_account_timeout(Test):
    uuid= "1529397"
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    @repeat_method(5)
    def test_01_session_details(self):
        time.sleep(60)
        response_get = local_user.show_local_users()
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "test1"', 'err: Failed to create localuser')
        logger.info("Account not present as account timed out")

    def test_02_guest_user_login(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test1', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, False, 'err:Login was sucessful')
        logger.info("Login failed")

# login with guest service and limited administrators privilege
class user_with_guest_service_limited_administrators(Test):
    uuid="1529403"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test2',
            'userpassword': 'Testp@ssw0rd',
            'member_of': ['Guest Services','Limited Administrators'],
        }
        post_resp = local_user.local_user(**user_json)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test2"', 'err: test1 not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "Limited Administrators"', 'err: test1 not created')

    def test_02_interface(self):
        dict1 = {
            'if': 'X0',
            'zone': 'LAN',
            'mgmt_https': True,
            'user_https': True,
            'ip': '192.168.168.168',
            "netmask": "255.255.255.0",
            "gateway": "0.0.0.0"
        }

        post_resp = configure_user.config_interface(**dict1)
        resp_get = configure_user.get_interface_status('X0')
        Assertion.assert_regular(json.dumps(resp_get), '"https": true', "err:failed")

    def test_03_guest_user_login(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test2', 'Testp@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, True, 'err:Login was not sucessful')
        logger.info("login with guest service and limited administrators privilege")

# login with guest service and read_only_administrators privilege
class user_with_guest_service_read_only_administrators(Test):
    uuid="1529405"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test3',
            'userpassword': 'P@ssw0rd',
            'member_of': ['Guest Services','SonicWALL Read-Only Admins'],

        }
        post_resp = local_user.local_user(**user_json)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test3"', 'err: test3  not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "SonicWALL Read-Only Admins"', 'err: test3 not created')

    def test_02_interface(self):
        dict1 = {
            'if': 'X0',
            'zone': 'LAN',
            'mgmt_https': True,
            'user_https': True,
            'ip': '192.168.168.168',
            "netmask": "255.255.255.0",
            "gateway": "0.0.0.0"
        }

        post_resp = configure_user.config_interface(**dict1)
        resp_get = configure_user.get_interface_status('X0')
        Assertion.assert_regular(json.dumps(resp_get), '"https": true', "err:failed")

    def test_03_guest_user_login(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test3', 'P@ssw0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, True, 'err:Login was not sucessful')
        logger.info("login with guest service and read_only_administrators privilege")

# login with guest service and Full_administrator privilege
class user_with_guest_service_administrators(Test):
    uuid="1529404"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'test4',
            'userpassword': 'P@ssW0rd',
            'member_of': ['Guest Services','SonicWALL Administrators'],

        }
        post_resp = local_user.local_user(**user_json)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "test4"', 'err: test4  not created')
        Assertion.assert_regular(json.dumps(get_resp), '"name": "SonicWALL Administrators"', 'err: test4 not created')

    def test_02_interface(self):
        dict1 = {
            'if': 'X0',
            'zone': 'LAN',
            'mgmt_https': True,
            'user_https': True,
            'ip': '192.168.168.168',
            "netmask": "255.255.255.0",
            "gateway": "0.0.0.0"
        }

        post_resp = configure_user.config_interface(**dict1)
        resp_get = configure_user.get_interface_status('X0')
        Assertion.assert_regular(json.dumps(resp_get), '"https": true', "err:failed")

    def test_03_guest_user_login(self):
        guest_user = users.UserLoginApi(headers, '192.168.168.168', 'test4', 'P@ssW0rd')
        is_authenticated, bearer_token = guest_user.local_user_login()
        Assertion.assert_equal(is_authenticated, True, 'err:Login was not sucessful')
        logger.info("login with guest service and Full_administrator privilege")

# export guest user account
class export_guest_account(Test):
    uuid = "2649995"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_autogenerate_guest_user(self):
        output = guest_user.guest_user_autogenerate()
        logger.info(output)
        Assertion.assert_equal(output,True,"err:Autogenarte guest user not sucessful")
        response_get = guest_user.show_user_guest_account()
        Assertion.assert_regular(json.dumps(response_get), '"comment": "Autogenerated guest user"',
                                 "err: Failed to edit guest user profile")
        logger.info("Guest user generated")

    def test_02_export_guest_account(self):
        output = guest_user. export_guest_account()
        logger.info(output)
        res_list = output.split("\n")
        for i in res_list:
            if "Autogenerated guest user" in i:
                guest_detail = i
        Assertion.assert_regular(str(guest_detail), 'Autogenerated guest user', 'err: Not exported all guest account ')
        logger.info("Guest account exported")

# export guest user account and verify user exported
class export_guest_account_validation(Test):
    uuid = "2649996"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_export_guest_account(self):
        output = guest_user. export_guest_account()
        logger.info(output)
        res_list = output.split("\n")
        for i in res_list:
            if "Autogenerated guest user" in i:
                guest_detail = i
        Assertion.assert_regular(str(guest_detail), 'Autogenerated guest user', 'err: Not exported all guest account ')
        logger.info("exported user verified")














