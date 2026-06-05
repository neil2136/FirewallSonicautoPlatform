import  json
from definition.settings import *

class TC01_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76942"
    description = show_testcase_info(TESTPLAN, '2477756', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477756')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_02_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
    def test_03_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

class TC02_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76943"
    description = show_testcase_info(TESTPLAN, '2477757', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477757')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_02_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")
    def test_03_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

class TC03_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76944"
    description = show_testcase_info(TESTPLAN, '2477758', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477758')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'ldap_auto_1',
                'domain': 'os-autosnwl.com',
                'username': 'ldap_auto_1',
                'userpassword': 'S0nic@uto',
                 "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_local_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

class TC04_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76945"
    description = show_testcase_info(TESTPLAN, '2477759', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477759')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'ldap_auto_1',
                'domain': 'os-autosnwl.com',
                'username': 'ldap_auto_1',
                'userpassword': 'S0nic@uto',
                 "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_local_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")

class TC05_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76950"
    description = show_testcase_info(TESTPLAN, '2477764', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477764')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'ldap_auto_1',
                'domain': 'os-autosnwl.com',
                'username': 'ldap_auto_1',
                'userpassword': 'S0nic@uto',
                 "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_local_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

class TC06_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76951"
    description = show_testcase_info(TESTPLAN, '2477765', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477765')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
                'action': 'edit',
                'oldusername': 'ldap_auto_1',
                'domain': 'os-autosnwl.com',
                'username': 'ldap_auto_1',
                'userpassword': 'S0nic@uto',
                 "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_local_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")

class TC07_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76952"
    description = show_testcase_info(TESTPLAN, '2477766', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477766')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")


    def test_03_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

class TC08_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76953"
    description = show_testcase_info(TESTPLAN, '2477767', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477767')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")


    def test_03_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

class TC09_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76946"
    description = show_testcase_info(TESTPLAN, '2477760', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477760')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_radius_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC10_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76947"
    description = show_testcase_info(TESTPLAN, '2477761', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477761')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_radius_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with invalid radius user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC11_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76954"
    description = show_testcase_info(TESTPLAN, '2477768', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477768')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_radius_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC12_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76955"
    description = show_testcase_info(TESTPLAN, '2477769', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477769')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_radius_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with invalid radius user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC13_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76956"
    description = show_testcase_info(TESTPLAN, '2477770', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477770')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

    def test_07_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_08_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC14_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76957"
    description = show_testcase_info(TESTPLAN, '2477771', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477771')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_02_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")
    def test_03_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_04_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_05_enable_radius_group(self):
        logger.info('Enable radius for admin group - SonicWALL Administrators....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": "SonicWALL Administrators",
            "groupname": "SonicWALL Administrators",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_06_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
            "quota_cycle": "day",
            "session_lifetime": True,
            "sessionlifetimetype": "minutes",
            "sessionlifetime": 3,
            "prune_on_expiry": True,
            "userquotalimit": True,
            "receivelimit": 1,
            "transmit": 2

        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with local user ")

    def test_07_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_08_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC15_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76962"
    description = show_testcase_info(TESTPLAN, '2477776', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477776')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_03_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_04_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_05_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_06_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntest", pwd="S0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_07_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')

class TC16_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76963"
    description = show_testcase_info(TESTPLAN, '2477777', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477777')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_02_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_03_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_04_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_05_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_06_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntest", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn local user login successfull with invalid details')

    def test_07_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')

class TC17_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76964"
    description = show_testcase_info(TESTPLAN, '2477778', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477778')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        # firewallUI = FWPage(url=url, user="test", pwd="password")
        firewallUI = FWPage(url=url, user="test", pwd="S0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')

class TC18_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76965"
    description = show_testcase_info(TESTPLAN, '2477779', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477779')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_user_auth_method(self):
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:Failed to select Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn local user login successfull with invalid ldap user')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')

class TC19_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76966"
    description = show_testcase_info(TESTPLAN, '2477780', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477780')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,
        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="password")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC20_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76967"
    description = show_testcase_info(TESTPLAN, '2477781', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477781')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn radius user login  successfull with invalid user')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC21_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76970"
    description = show_testcase_info(TESTPLAN, '2477784', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477784')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_local_user_auth_method(self):
        logger.info('Select LDAP-LOCAL authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select LDAP Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="S0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successful')


class TC22_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76971"
    description = show_testcase_info(TESTPLAN, '2477785', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477785')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_local_user_auth_method(self):
        logger.info('Select LDAP-LOCAL authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select LDAP Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn ldap local user login  successfull with invalid use')


class TC23_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76972"
    description = show_testcase_info(TESTPLAN, '2477786', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477786')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_local_user_auth_method(self):
        logger.info('Select LDAP-LOCAL authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select LDAP Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestldaplocal',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntestldaplocal", pwd="S0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

class TC24_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76973"
    description = show_testcase_info(TESTPLAN, '2477787', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477787')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "ldap_auto_1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "ldap_auto_1", "ERR: Failed to import LDAP user.")

    def test_03_edit_user(self):
        edit_local_user_domain = {
            'action': 'edit',
            'oldusername': 'ldap_auto_1',
            'domain': 'os-autosnwl.com',
            'username': 'ldap_auto_1',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services',"SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']

        }

        rc = local_user.local_user(**edit_local_user_domain)
        get_resp = local_user.show_local_users()
        logger.info(get_resp)
        Assertion.assert_equal(rc, True, "ERR: edit_user failed")

    def test_04_enable_ldap_local_user_auth_method(self):
        logger.info('Select LDAP-LOCAL authentication method....')
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:Failed to select LDAP Local authentication method.")

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestldaplocal',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntestldaplocal", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn local ldap user login  successfull with invalid local user')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

class TC25_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76974"
    description = show_testcase_info(TESTPLAN, '2477788', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477788')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="password")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC26_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76975"
    description = show_testcase_info(TESTPLAN, '2477789', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477789')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]
        }
        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")

    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="test", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn radius local user login  successfull with invalid radius user')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC27_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76976"
    description = show_testcase_info(TESTPLAN, '2477790', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477790')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestldaplocal',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntestldaplocal", pwd="S0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

    def test_11_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

class TC28_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76977"
    description = show_testcase_info(TESTPLAN, '2477791', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477791')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_show_testcase_info(self):
        pass

    def test_01_create_radiususer(self):
        # Create radius user
        add_radius_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not created successfully")

    def test_02_radius_server_test(self):
        time.sleep(10)
        radius_user = user_radius.test_radius_server()
        Assertion.assert_equal(radius_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "radius-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        time.sleep(10)
        user_setting.user_method_authentication(**user_auth)
        time.sleep(10)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_radius_group(self):
        logger.info('Enable radius for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All RADIUS Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'All RADIUS Users', 'err: Failed to edit All RADIUS Users')

    def test_05_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_LAN"', "Err: failed to create address object")
    def test_06_enable_server_access(self):
        enable = {
            'LAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_07_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_08_add_sslvpn_user(self):
        user_json = {

            'action': 'add',
            'username': 'sslvpntestldaplocal',
            'userpassword': 'S0nic@uto',
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_09_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="sslvpntestldaplocal", pwd="wS0nic@uto")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn radius-local user login  successfull with invalid local user')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

    def test_11_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")

