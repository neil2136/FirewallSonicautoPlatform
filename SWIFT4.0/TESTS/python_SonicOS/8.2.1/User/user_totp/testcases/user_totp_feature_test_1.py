

from definition.settings_totp import *
from definition import constants

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp')

class sslvpn_config(Test):
    uuid = 'NonTC'

    def test_01_config_local(self):
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

class Totp_01(Test):
    uuid = "SOSAIOT-TC-77210"
    description= show_testcase_info(Parameter.TESTPLAN, '1514675', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514675')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user",
            "userpassword":"S0nic@uto" ,
            "one_time_password": "totp",
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_create_group(self):

        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            'one_time_password': 'otp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"otp": true', 'err: group1 not created')

class Totp_02(Test):
    uuid = "SOSAIOT-TC-77211"
    description= show_testcase_info(Parameter.TESTPLAN, '1514676', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514676')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:Failed to select Local authentication method.")

    def test_02_config_ldap_user(self):
        resp = ldap.show_ldap_server_by_name(ldap_server_ip)
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': "192.168.168.85",
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

            ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), f'"host": "{ldap_server_ip}"', "failed to config ldap server")

    def test_03_import_ldap_user(self):
        add = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = user_local.import_local_usr_from_ldap(**add)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")

    def test_04_enable_totp_with_privileges_to_ldap_user(self):
        logger.info('Enable TOTP also giving SonicWALL Administrators membership to LDAP user....')
        local_users_resp = user_local.show_local_users()
        logger.info(local_users_resp)
        edit_ldap_user = {
            "action": "edit",
            "oldusername": "test",
            "domain": "os-autosnwl.com",
            "username": "test",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
        }

        response = user_local.local_user(**edit_ldap_user)
        logger.info(response)
        Assertion.assert_equal(response, True, 'ERR:  Failed to enable TOTP with SonicWALL Administrators membership for LDAP user.')

class Totp_03(Test):
    uuid = "SOSAIOT-TC-77212"
    description= show_testcase_info(Parameter.TESTPLAN, '1514677', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514677')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldap_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"', "ERR:Failed to select Local authentication method.")

    def test_02_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user2",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user2")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_03_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user2 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_04(Test):
    uuid = "SOSAIOT-TC-77214"
    description= show_testcase_info(Parameter.TESTPLAN, '1514679', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514679')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user3",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            'account_lifetime': True,
            'accountlifetime': 2,
            'lifetype': 'minutes',
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 2,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2,
             "one_time_password": "totp",
        }
        response = user_local.local_user(**add_localuser)
        resp = user_local.show_local_user_by_name("test_totp_local_user3")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
        Assertion.assert_regular(json.dumps(resp), '"minutes": 2', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_group_member_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user3 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user3', resp, re.M | re.I)
            match = find.group()
            logger.info("The user obtained is {}".format(find))
            Assertion.assert_equal(match, "test_totp_local_user3", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Sonicwall Administrator Group member faield enter totp in 2FA page")

    def test_03_test_user_status(self):
        time.sleep(150)
        status = user_local.show_local_user_by_name('test_totp_local_user3')
        Assertion.assert_not_regular(json.dumps(status), '"name": "test_totp_local_user3"', 'err: Failed to get localuser')

class Totp_05(Test):
    uuid = "SOSAIOT-TC-77216"
    description= show_testcase_info(Parameter.TESTPLAN, '1514681', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514681')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_group(self):
        add_local_group = {
                "user": {
                    "local": {
                    "group": [
                        {
                        "name": "test_group_1",
                        "domain": "os-autosnwl.com",
                        "one_time_password": {
                            "totp": True
                        }
                        }
                    ]
                    }
                }
                }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"domain": "os-autosnwl.com"', 'err: Failed to create local group')
        Assertion.assert_regular(json.dumps(response_get), '"name": "test_group_1"', 'err: Failed to create local group')

    def test_02_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            'one_time_password': 'totp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')


class Totp_06(Test):
    uuid = "SOSAIOT-TC-77217"
    description= show_testcase_info(Parameter.TESTPLAN, '1514682', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514682')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_group(self):
        group_json = {
            'action': 'edit',
            'grouptype': 'locally_only',
            'groupname': 'group2',
            'one_time_password': 'totp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group2"', 'err: group1 not created')

    def test_02_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'test_totp',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone', 'group2','SonicWALL Administrators'],
        }
        resp = user_local.local_user(**member)
        resp1 = user_local.show_local_user_by_name('test_totp')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: test_totp not added')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group2"',
                                 'err: test_totp not added')

    def test_04_local_group_member_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp', resp, re.M | re.I)
            match = find.group()
            logger.info("The user obtained is {}".format(find))
            Assertion.assert_equal(match, "test_totp", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Sonicwall Administrator Group member faield enter totp in 2FA page")


class Totp_07(Test):
    uuid = "SOSAIOT-TC-77228"
    description= show_testcase_info(Parameter.TESTPLAN, '1514693', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514693')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_invalid",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_invalid")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 4
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_invalid -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_invalid', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_not_equal(match, "test_totp_local_user_invalid", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_08(Test):
    uuid = "SOSAIOT-TC-77236"
    description= show_testcase_info(Parameter.TESTPLAN, '1514701', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514701')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_01_add_localuser_enable_totp(self):

        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_check",
            "userpassword": "P@ssw0rd",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_check")
        Assertion.assert_regular(json.dumps(resp), '"name": "test_totp_local_user_check"', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_login_to_fw(self):
        ui_obj = virtualoffice_page.VirtualPage(ip='192.168.168.168', user='test_totp_local_user_check', password='P@ssw0rd')
        logger.info(ui_obj)
        virtual_login = ui_obj.login_ui()
        logger.info(virtual_login)

        resp = userstatus1.show_users_status()
        logger.info(resp)
        find = re.search(r'test_totp_local_user_check', resp, re.M | re.I)
        logger.info("The user obtained is {}".format(find))
        match = find.group()
        Assertion.assert_equal(match, "test_totp_local_user_check", "ERR: :Invalid user logged in even though not password is wrong")

    def test_03_add_localuser_enable_totp(self):
        edit_user = {
            "action": "edit",
            "username": "test_totp_local_user_check",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**edit_user)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_check")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_04_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_check -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_check', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_check", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Admin failed to enter totp on scanner page")

class Totp_09(Test):
    uuid = "SOSAIOT-TC-77238"
    description= show_testcase_info(Parameter.TESTPLAN, '1514703', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514703')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user4",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user4")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user4 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_edit_user(self):
        edit_localuser = {
            "action": "edit",
            "username": "test_totp_local_user4",
            "userpassword": "S0nic@uto",
            "one_time_password": "",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**edit_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user4")
        Assertion.assert_regular(json.dumps(resp),'"name": "test_totp_local_user4"','ERR: Failed to create a user')

    def test_04_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 3
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user4 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Admin failed to enter totp on scanner page")

class Totp_10(Test):
    uuid = "SOSAIOT-TC-77247"
    description= show_testcase_info(Parameter.TESTPLAN, '1514716', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514716')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"', "ERR:Failed to select Local authentication method.")

    def test_02_config_ldap_user(self):
        resp = ldap.show_ldap_server_by_name(ldap_server_ip)
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': ldap_server_ip,
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

            ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), f'"host": "{ldap_server_ip}"', "failed to config ldap server")

    def test_03_enable_totp_with_admin_privileges_to_ldap_user(self):
        logger.info('Enable TOTP also giving SonicWALL Administrators membership to LDAP user....')
        local_users_resp = user_local.show_local_users()
        logger.info(local_users_resp)
        edit_ldap_user = {
            "action": "edit",
            "oldusername": "test",
            "domain": "os-autosnwl.com",
            "username": "test",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }

        response = user_local.local_user(**edit_ldap_user)
        logger.info(response)
        Assertion.assert_equal(response, True, 'ERR:  Failed to enable TOTP with SonicWALL Administrators membership for LDAP user.')

    def test_04_ldap_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test -pwd password -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: LDAP user failed enter totp in 2FA page")

class Totp_11(Test):
    uuid = "SOSAIOT-TC-77233"
    description= show_testcase_info(Parameter.TESTPLAN, '1514698', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514698')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local(self):
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

    def test_02_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_check_bind",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_check_bind")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_03_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_check_bind -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_check_bind', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_check_bind", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_04_unbind_totp(self):
        response = user_local.unbind_totp_key_with_name("test_totp_local_user_check_bind")
        logger.info(response)
        Assertion.assert_equal(response, True,'ERR: Failed to unbind totp')

    def test_05_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_check_bind -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_check_bind', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_check_bind", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_12(Test):
    uuid = "SOSAIOT-TC-77218"
    description= show_testcase_info(Parameter.TESTPLAN, '1514683', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514683')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_create_domain_group(self):
        add_local_group = {
                "user": {
                    "local": {
                    "group": [
                        {
                        "name": " Domain_group",
                        "domain": "Group21@local.com",
                        }
                    ]
                    }
                }
                }
        response = user_local.add_local_group(**add_local_group )
        logger.info(response)
        response_get = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(response_get), '"domain": "loocal.com"', 'err: Failed to create local group')

    def test_02_create_local_group(self):
        group_json = {
            'action': 'add',
            'groupname': 'group12',
            'one_time_password': 'totp',
            'member_of':['LOOCAL\\Domain_roup@Group21"']
        }
        resp = user_local.group_member_of(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"domain": "loocal.com"', 'err: Failed to create local group')
        
class Totp_13(Test):
    uuid = "SOSAIOT-TC-77219"
    description= show_testcase_info(Parameter.TESTPLAN, '1514684', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514684')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_local_user_1",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_local_user_1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_add_user_to_member(self):
        add_member_of_group = {
            'action': 'add',
            'groupname': 'Group12@local.com',
            'member_of': ['test_local_user_1']
        }
        ssl_services = user_local.group_member_of(**add_member_of_group)
        Assertion.assert_equal(ssl_services, True, "ERR: :Radius user with sslvpn services is not selected successfully")

class Totp_14(Test):
    uuid = "SOSAIOT-TC-77220"
    description= show_testcase_info(Parameter.TESTPLAN, '1514685', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514685')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user1",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
 
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user1 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_15(Test):
    uuid = "SOSAIOT-TC-77222"
    description= show_testcase_info(Parameter.TESTPLAN, '1514687', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514687')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_local_user3",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_local_user3")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_local_user3 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_local_user3', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_local_user3", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
            
class Totp_16(Test):
    uuid = "SOSAIOT-TC-77246"
    description= show_testcase_info(Parameter.TESTPLAN, '1514715', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514715')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_radiususer(self):
      add_radiususer = {
        'local_users_only': False,
        'default_user_group': "Everyone",
        'timeout': 6,
        'retries': 10,
        'user_group_mechanism': {
        'radius_attribute': 'vendor-specific'
      }
      }
      response = user_radius.user_radius_settings(**add_radiususer)
      response_get = user_radius.show_user_radius_settings() 
      Assertion.assert_regular(json.dumps(response_get), '"local_users_only": false', 'err: Failed to create Radius user')
    
class Totp_17(Test):
    uuid = "SOSAIOT-TC-77248"
    description= show_testcase_info(Parameter.TESTPLAN, '1514717', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514717')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_ldapuser(self):
        ldap_1 = {
            'local_users_only': True,
            
        }
        response = ldap.ldap_setting(**ldap_1)
        Assertion.assert_equal(response, True, 'err: Failed to create Radius user')

class Totp_18(Test):
    uuid = "SOSAIOT-TC-77251"
    description= show_testcase_info(Parameter.TESTPLAN, '1514723', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514723')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_tsr",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_tsr")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_Check_LocalUser_config_in_TSR(self):
        resp1 = user_local.show_local_user_by_name('test_tsr')
        Assertion.assert_regular(json.dumps(resp1), '"name": "test_tsr"', 'err: Failed to show user test_tsr')
        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            match1 = re.search(r'Old="", New="TOTP"', doc, re.I | re.S)
            if match1:
                output1 = match1.group(0)

            logger.info('The tsr user content is {}'.format(output1))
            Assertion.assert_equal(output1, 'Old="", New="TOTP"',
                                  'ERR: TOTP users are not present in tsr.')
            os.remove('/tmp/techSupport')
            flag = True if re.search('test_tsr', doc) else False
            Assertion.assert_equal(flag, True, "ERR: can't fine test123 config in tsr")
            
class Totp_19(Test):
    uuid = "SOSAIOT-TC-77259"
    description= show_testcase_info(Parameter.TESTPLAN, '1514738', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514738')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_check_bind",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_check_bind")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_check_bind -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_check_bind', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_check_bind", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_20(Test):
    uuid = "SOSAIOT-TC-77267" 
    description= show_testcase_info(Parameter.TESTPLAN, '2622907', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2622907')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpntest_portal",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            "vpn_client_access": ['LAN Subnets','WAN Subnets','DMZ Subnets']
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpntest_portal")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_genearate_text(self):
        try:
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = "https://192.168.168.168:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_enter_otp.py ' + \
                    '-url ' + url + ' -user sslvpntest_portal -pwd S0nic@uto'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest_portal', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest_portal", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_21(Test):
    uuid = "SOSAIOT-TC-77213"
    
    def test_01_add_user_with_password_change(self):
        add_user = {
            "action": "add",
            "username": "test_user1",
            "userpassword": "S0nic@uto",
            "member_of": ["Trusted Users", "SonicWALL Administrators"],
            "one_time_password": "totp",
            "force_password_change": True
        }
        response = user_local.local_user(**add_user)
        response1 = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(response1), '"name": "test_user1"', 'ERR: Unable to create local user with password change config')

    def test_02_genearate_text(self):
        try:
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = "https://192.168.168.168"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/lib/ui_user_otp.py ' + \
                    '-url ' + url + ' -user test_user1 -pwd S0nic@uto'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_user1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_user1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
