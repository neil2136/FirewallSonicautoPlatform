from definition.settings import *

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/RADIUS-TP89')

class Radius_configs(Test):
    uuid = "NonTC"

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
    
    
    def test_02_edit_radius_user_mechanism(self):
        edit_radius_server_json = {
            "user": {
                "radius": {
                "timeout": 5,
                "retries": 3,
                "periodic_check_server": True,
                "mschapv2_mode": False,
                "local_users_only": False,
                "user_group_mechanism": {
                    "ldap": True
                }
                }
            }
            }
        radius_user = user_radius.edit_user_radius_settings(**edit_radius_server_json)
        logger.info("Radius user edited is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user edit failed")


    
    def test_02_default_radius_user_to_group_sonicwall_limited_administrators(self):
        user_radius_set = {
            "user":
                {
                    "radius":
                        {                     
                         "timeout":8,
                         "retries":4,
                         "default_user_group":"Limited Administrators",
                          "local_users_only":False,
                          "periodic_check_server": True,
                          "mschapv2_mode": False,
                         "user_group_mechanism":{"radius_attribute":"filter-id"}
                        }
                     }
                }
        rc = Radius_user.add_radius_server_new(**user_radius_set)
        Assertion.assert_equal(rc, True, "ERR: Editing the user group object failed")

    def test_03_edit_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **accessrule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to modify access rule')

    def test_04_add_access_rule(self):
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


class TC01_Radius(Test):
    uuid = "SOSAIOT-TC-77180"
    
    def test_01_add_radius_user_method(self):
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
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to create radius server')

    def test_02_radius_user_with_sslvpn_services(self):
        add_member_of_group = {
            'action': 'add',
            'groupname': 'Limited Administrators',
            'member_of': ['All RADIUS Users']
        }
        ssl_services = userLocalapi.group_member_of(**add_member_of_group)
        Assertion.assert_equal(ssl_services, True, "ERR: :Radius user with sslvpn services is not selected successfully")
    
    def test_03_portal_login_using_LDAP_user_group(self):
        assert_msg = True
        try:
            localhost.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/RADIUS-TP89/definition/ui_group.py -url {url} -user test -pwd password'
            out = localhost.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class TC02_Radius(Test):
    uuid = "SOSAIOT-TC-77182"
    description = show_testcase_info(TESTPLAN, '1509023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509023')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_radius_user_auth_method(self):
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
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_enable_radius_group(self):
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

    def test_03_radius_user(self):
        web_url = "12.12.1.40"
        cmd = [f'curl https://{web_url} -k']
        output = static_client.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")


class TC03_Radius(Test):
    uuid = "SOSAIOT-TC-77183"
    description = show_testcase_info(TESTPLAN, '1509024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radiususer(self):
        add_radiususer = {
            'local_users_only': False,
            'default_user_group': "",
            'timeout': 6,
            'retries': 10,
            'radius_attribute': 'filter-id'

        }
        response = Radius_user.user_radius_settings(**add_radiususer)
        response_get = Radius_user.show_user_radius_settings() 
        Assertion.assert_regular(json.dumps(response_get), '"local_users_only": false', 'err: Failed to create Radius user')

    def test_02_check_filter_id(self):
        Radius_server1 = {
            "user": {
                "radius": {
                "test": {
                    "name": "192.168.168.85",
                    "user": {
                    "userName": "test_radius1",
                    "userPwd": "password"
                    }
                }
                }
            }
            }
        radius_test = Radius_user.test_radius_server(**Radius_server1)
        logger.info(radius_test)
        Assertion.assert_equal(radius_test,True, 'err: Failed to create Radius user')
        
class TC04_Radius(Test):
    uuid = "SOSAIOT-TC-77184"
    description = show_testcase_info(TESTPLAN, '1509025', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509025')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_groups(self):
        add_groups = {
        "user": {
            "local": {
            "group": [
                {
                "name": "test_radius_group1",
                "domain": "os-autosnwl.com",
                "quota_cycle": {
                    "non_cyclic": True
                },
                "session_lifetime": {},
                "limit": {
                    "receive": 0,
                    "transmit": 0
                }
                },
                {
                "name": "test_radius_group2",
                "domain": "os-autosnwl.com",
                "quota_cycle": {
                    "non_cyclic": True
                },
                "session_lifetime": {},
                "limit": {
                    "receive": 0,
                    "transmit": 0
                }
                }
            ]
            }
        }
        }
        local_groups = local_user.add_local_group(**add_groups)
        logger.info(local_groups)
        Assertion.assert_equal(local_groups,True,"Err:Unable to retrieve groups")
        
    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule12',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "OS-AUTOSNWL\\test_radius_group1"},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule34',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_04_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")
        
    def test_05_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius2', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_not_equal(is_auth, True, "Error: can't able to generate token with radius user")

class TC05_Radius(Test):
    uuid = "SOSAIOT-TC-77185"
    description = show_testcase_info(TESTPLAN, '1509026', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509026')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "OS-AUTOSNWL\\test_radius_group1"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **accessrule)
        Assertion.assert_equal(resp, True ,'ERR: Failed to modify access rule')


    def test_02_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")
    
    def test_03_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius2', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_not_equal(is_auth, True, "Error: can't able to generate token with radius user")

class TC06_Radius(Test):
    uuid = "SOSAIOT-TC-77186"
    description = show_testcase_info(TESTPLAN, '1509028', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509028')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_user_method(self):
        logger.info("-------Radius Config---------")
        add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 1812,
                'secret': 'password',
                'send_through_vpn_tunnel': False,
                "user_name_format": "user_name"

            }
        response = Radius_user.edit_radius_server(**add_radius_user)
        logger.info(response)
        response_get = Radius_user.show_radius_server()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to create radius server')

class TC07_Radius(Test):
    uuid = "SOSAIOT-TC-77191"
    description = show_testcase_info(TESTPLAN, '2956924', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2956924')
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
    
    def test_02_enable_radius_user_auth_method(self):

        logger.info("-------Local Auth---------")
        user_auth = {
                "auth_method": "local",
                "sso_agent": False,
                "terminal_services_agent": False,
                "radius_accounting": False,
                "third_party_api": False,
                "capture_client": False
            }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"', "ERR:Failed to select Local authentication method.")
    
class TC08_Radius(Test):
    uuid = "SOSAIOT-TC-77187"
    description = show_testcase_info(TESTPLAN, '1509029', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509029')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test_radius1",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "test_radius1", "ERR: Failed to import LDAP user.")

    def test_02_import_ldap_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test_radius2",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "test_radius2", "ERR: Failed to import LDAP user.")

    
    def test_03_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")
    
    def test_04_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius2', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_not_equal(is_auth, True, "Error: can't able to generate token with radius user")

    
class TC09_Radius(Test):
    uuid = "SOSAIOT-TC-77190"
    description = show_testcase_info(TESTPLAN, '2345590', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2345590')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_03_enable_ldap_user_auth_method(self):
        logger.info('Select LDAP authentication method....')
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

    def test_02_edit_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **accessrule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to modify access rule')

    def test_03_local_user(self):
        web_url = "http://12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")

        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with local user ")
        


class TC10_Radius(Test):
    uuid = "SOSAIOT-TC-77188"
    description = show_testcase_info(TESTPLAN, '1509030', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1509030')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule = {
            'name': name,
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "OS-AUTOSNWL\\test_radius_group1"}
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **accessrule)
        Assertion.assert_equal(False, True, 'ERR: Failed to modify access rule')

        
    def test_02_add_localuser_enable_totp(self):
        
        add_localuser = {
        "action": "add",
        "username": "Radius_local_user",
        "userpassword": "password",
        "member_of": ["SonicWALL Administrators"]
        }
        response = local_user.local_user(**add_localuser)
        logger.info(response)
        resp = local_user.show_local_user_by_name("Radius_local_user")
        Assertion.assert_regular(json.dumps(resp), '"name": "Radius_local_user"', 'ERR:  Failed to enable TOTP for new localuser')
       
    def test_03_enable_radius_user_auth_method(self):

        logger.info("-------Radius Auth---------")
        user_auth = {
                "auth_method": "radius-local",
                "sso_agent": False,
                "terminal_services_agent": False,
                "radius_accounting": False,
                "third_party_api": False,
                "capture_client": False
            }
        user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"', "ERR:Failed to select Local authentication method.")

    def test_03_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")

    def test_04_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'Radius_local_user', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")


class TC11_Radius(Test):
    uuid = "SOSAIOT-TC-77189"
    description = show_testcase_info(TESTPLAN, '2345588', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2345588')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_radius_user(self):
        web_url = "12.12.1.40"
        cmd = [f'curl https://{web_url} -k']
        output = static_client.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")

    
    def test_02_radius_user(self):
        web_url = "12.12.1.40"
        res = fw.api_logout()
        time.sleep(10)
        result = subprocess.Popen(["wget", f"{web_url}", "--timeout=5", "--tries=1"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  text=True).communicate()
        logger.info(result)
        Assertion.assert_regular(str(result), f"{Parameter.ip}", "ERR: export log and check info failed")
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, Parameter.ip, 'test_radius1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.local_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with radius user")


    
    