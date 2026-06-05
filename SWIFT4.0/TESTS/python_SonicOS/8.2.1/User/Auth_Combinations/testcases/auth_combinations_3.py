import json
import subprocess
from definition.settings import *


class TC001_Ula_Auth_combinations(Test):
    uuid = "NonTC"

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


class TC043_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76922"
    description = show_testcase_info(TESTPLAN, '2477736', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477736')
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
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'S0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_03_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC044_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76923"
    description = show_testcase_info(TESTPLAN, '2477737', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477737')
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
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'wS0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_03_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC045_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76924"
    description = show_testcase_info(TESTPLAN, '2477738', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477738')
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

    def test_02_enable_ldap_user_auth_method(self):
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

    def test_04_local_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_with_domain(username="ldap_auto_1", domainname="os-autosnwl.com")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC046_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76925"
    description = show_testcase_info(TESTPLAN, '2477739', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477739')
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

    def test_02_enable_ldap_user_auth_method(self):
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

    def test_04_local_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_with_domain(username="ldap_auto_1", domainname="os-autosnwl.com")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC047_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76926"
    description = show_testcase_info(TESTPLAN, '2477740', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477740')
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

    def test_05_radius_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'radius_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC048_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76927"
    description = show_testcase_info(TESTPLAN, '2477741', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477741')
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

    def test_05_radius_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'radius_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with radius user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC049_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76930"
    description = show_testcase_info(TESTPLAN, '2477744', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477744')
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

    def test_04_local_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_with_domain(username="ldap_auto_1", domainname="os-autosnwl.com")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC050_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76931"
    description = show_testcase_info(TESTPLAN, '2477745', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477745')
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

    def test_04_local_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'ldap_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_with_domain(username="ldap_auto_1", domainname="os-autosnwl.com")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC051_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76932"
    description = show_testcase_info(TESTPLAN, '2477746', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477746')
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
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC052_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76933"
    description = show_testcase_info(TESTPLAN, '2477747', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477747')
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
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth', 'wS0nic@uto,')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with invalid local user ")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_05_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")


class TC053_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76934"
    description = show_testcase_info(TESTPLAN, '2477748', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477748')
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

    def test_05_radius_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'radius_auto_1', 'S0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC054_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76935"
    description = show_testcase_info(TESTPLAN, '2477749', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477749')
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

    def test_05_radius_user(self):
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'radius_auto_1', 'wS0nic@uto')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with radius user")

        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC055_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76936"
    description = show_testcase_info(TESTPLAN, '2477748', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477748')
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

    def test_05_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'S0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_not_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC056_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76937"
    description = show_testcase_info(TESTPLAN, '2477751', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477751')
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

    def test_05_local_user_quota(self):
        add_localuser = {
            "action": "add",
            "username": "test_auth_1",
            "userpassword": "S0nic@uto",
            "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"]
        }

        response = local_user.local_user(**add_localuser)
        Assertion.assert_equal(response, True, "Error: Can't able to create local user")
        web_url = "baidu.com"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'test_auth_1', 'wS0nic@uto')
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can't able to generate token with local user ")
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{ip}", "ERR: export log and check info failed")

    def test_06_delete_user(self):
        response = local_user.delete_local_user_no_domain(username="test_auth_1")
        Assertion.assert_equal(response, True, "ERR: can't able to delete local user")

    def test_07_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")
