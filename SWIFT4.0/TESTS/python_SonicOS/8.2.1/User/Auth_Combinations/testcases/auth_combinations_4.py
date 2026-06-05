import json
from definition.settings import *

class netex:
    def __init__(self, username, password, netexurl, domain):
        self.username = username
        self.password = password
        self.netexurl = netexurl
        self.domain = domain

    def NX_disconnect(self):
        time.sleep(10)
        localhost = Host('localhost')
        logger.info(localhost)
        res = localhost.send_command("killall netExtender")
        logger.info("successfully disconnected netExtender ")
        return True

    def install_nxlinux(self):
        netexsession = pexpect.spawn("netExtender",
                                     ["-u", self.username, "-p", self.password, "-d", self.domain, self.netexurl,
                                      "--always-trust", "host"])
        logger.info(f"The netextender session {netexsession.__dict__}")
        index = netexsession.expect(["Do you want to proceed", pexpect.EOF, pexpect.TIMEOUT])
        time.sleep(5)
        if index == 0:
            logger.info("Received self-signed certificate override")
            netexsession.sendline("Y")
            logger.info("Successfully accepted the self-signed and trying to connect via NetExtender")
        else:
            logger.error("Error: Unable to connect via NetExtender as Authentication Failed")
        time.sleep(10)
        index = netexsession.expect(["NetExtender connected successfully", pexpect.EOF, pexpect.TIMEOUT])
        time.sleep(10)
        Flag = False
        if index == 0:
            logger.info("Successfully connected via NetExtender ")
            Flag = True
        else:
            logger.error(
                "Error: Unable to connect via NetExtender as Authentication failed due to Invalid Username/Password")
        return Flag

class NonTC_installnx(Test):
    uuid = "NonTC"
    
    def test_00_enable_ldapuser(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_01_sslvpn_local(self):
        cpy_build = cp_nx.cpbuildnx_linux_local()
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux()
        logger.info(inst)

class TC057_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76948"
    description = show_testcase_info(TESTPLAN, '2477762', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477762')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")
        tacacs_user_info =user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)
    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_AdminPrevilage(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ["All TACACS+ Users"]
        }
        resp = local_user.group_member_of(**member)
        resp1 = local_user.show_local_group_by_name("SonicWALL Administrators")
        if isinstance(resp1, str):
            data = json.loads(resp1)
        else:
            data = resp1
        groups = data.get('user', {}).get('local', {}).get('group', [])
        assert any(
            g.get('name') == 'SonicWALL Administrators' and
            any(m.get('name') == 'All TACACS+ Users' for m in (g.get('member') or []))
            for g in groups
        ), 'err: tacacs users not added to sonicwall administrators'

    def test_05_tacac_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with tacacs user")

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC058_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76949"
    description = show_testcase_info(TESTPLAN, '2477763', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477763')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")
        tacacs_user_info =user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)
    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")
    def test_04_tacac_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'wpassword')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with wrong tacacs user")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC059_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76958"
    description = show_testcase_info(TESTPLAN, '2477772', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477772')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")
        tacacs_user_info =user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_AdminPrevilage(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ["All TACACS+ Users"]
        }
        resp = local_user.group_member_of(**member)
        resp1 = local_user.show_local_group_by_name("SonicWALL Administrators")
        if isinstance(resp1, str):
            data = json.loads(resp1)
        else:
            data = resp1
        groups = data.get('user', {}).get('local', {}).get('group', [])
        assert any(
            g.get('name') == 'SonicWALL Administrators' and
            any(m.get('name') == 'All TACACS+ Users' for m in (g.get('member') or []))
            for g in groups
        ), 'err: tacacs users not added to sonicwall administrators'

    def test_05_tacac_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'password')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, True, "Error: can't able to generate token with tacacs user")

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC060_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76959"
    description = show_testcase_info(TESTPLAN, '2477773', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477773')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")
        tacacs_user_info =user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)
    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")
    def test_04_tacac_user(self):
        headers = OrderedDict([('Accept', 'application/json'),
                               ('Content-Type', 'application/json'),
                               ('Accept-Encoding', 'application/json'),
                               ('charset', 'UTF-8')])
        Local_User = users.UserLoginApi(headers, ip, 'user1', 'wpassword')
        time.sleep(60)
        is_auth, bearer_token = Local_User.guest_user_login()
        Assertion.assert_equal(is_auth, False, "Error: can able to generate token with tacacs user")

    def test_05_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC061_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76960"
    description = show_testcase_info(TESTPLAN, '2477774', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477774')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
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

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC062_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76961"
    description = show_testcase_info(TESTPLAN, '2477775', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477775')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")
        tacacs_user_info =user_tacacs.show_tacacs_server()
        logger.info(tacacs_user_info)
    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
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

    def test_06_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC063_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76968"
    description = show_testcase_info(TESTPLAN, '2477782', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477782')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="user1", pwd="password")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_09_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC064_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76969"
    description = show_testcase_info(TESTPLAN, '2477783', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477783')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="user1", pwd="wpassword")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        time.sleep(3)
        if not res_url.startswith(expected_url):
            logger.info("Retrying login since URL did not match expected pattern...")
            time.sleep(2)
            res, res_url = firewallUI.login_ui()
            time.sleep(3)
        if res and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn local user login successfull with invalid user')

    def test_09_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC065_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76978"
    description = show_testcase_info(TESTPLAN, '2477792', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477792')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="user1", pwd="password")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        time.sleep(3)
        if not res_url.startswith(expected_url):
            logger.info("Retrying login since URL did not match expected pattern...")
            time.sleep(2)
            res, res_url = firewallUI.login_ui()
            time.sleep(3)
        if res and res_url.startswith(expected_url):
            flag = True
        Assertion.assert_equal(flag, True, 'err: sslvpn local user login not successfull')

    def test_09_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC066_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76979"
    description = show_testcase_info(TESTPLAN, '2477793', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477793')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_local_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168:4433"
        firewallUI = FWPage(url=url, user="user1", pwd="wpassword")
        flag = False
        expected_url = "https://192.168.168.168:4433"
        res, res_url = firewallUI.login_ui()
        if not res_url.startswith(expected_url):
            res, res_url = firewallUI.login_ui()
        if res == True and res_url.startswith(expected_url):
            flag = False
        Assertion.assert_equal(flag, False, 'err: sslvpn local user login not successfull')


    def test_09_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC067_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76980"
    description = show_testcase_info(TESTPLAN, '2477794', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477794')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_11_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC068_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76981"
    description = show_testcase_info(TESTPLAN, '2477795', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477795')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_radius_user_auth_method(self):
        logger.info('Select radius authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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
        Assertion.assert_equal(flag, False, 'err: sslvpn local user login successfull with invalid details')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

    def test_11_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC069_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76988"
    description = show_testcase_info(TESTPLAN, '2477802', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477802')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_radius_user(self):
        net_ex = netex(username="user1", password="password", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn radius user login not successfull')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC070_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76989"
    description = show_testcase_info(TESTPLAN, '2477803', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477803')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs authentication method....')
        user_auth = {
            "auth_method": "tacacs",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_radius_user(self):
        net_ex = netex(username="user1", password="wpassword", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn radius user login successfull with invalid user')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC071_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76998"
    description = show_testcase_info(TESTPLAN, '2477812', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477812')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs-local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_radius_user(self):
        net_ex = netex(username="user1", password="password", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn radius user login not successfull')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC072_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76999"
    description = show_testcase_info(TESTPLAN, '2477813', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477813')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs-local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_08_login_via_radius_user(self):
        net_ex = netex(username="user1", password="wpassword", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn tacacs user login successfull with invalid user')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

class TC073_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-77000"
    description = show_testcase_info(TESTPLAN, '2477814', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477814')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs-local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_09_login_via_tacacs_local_user(self):
        net_ex = netex(username="sslvpntestldaplocal", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn radius user login not successfull')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

    def test_11_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')

class TC074_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-77001"
    description = show_testcase_info(TESTPLAN, '2477815', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477815')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_tacacsuser(self):
        # Create tacacs user
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = user_tacacs.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user is not created successfully")

    def test_02_tacacs_server_test(self):
        time.sleep(10)
        tacacs_user = user_tacacs.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERR: Radius user test got failed")

    def test_03_enable_tacacs_user_auth_method(self):
        logger.info('Select tacacs-local authentication method....')
        user_auth = {
            "auth_method": "tacacs-local",
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
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "tacacs-local"',
                                 "ERR:Failed to select Local authentication method.")

    def test_04_enable_tacacs_group(self):
        logger.info('Enable tacacs for admin group - SSLVPN Services....')
        edit_local_group = {
            "action": "edit",
            "grouptype": "domaingroup",
            "name": 'SSLVPN Services',
            "groupname": "SSLVPN Services",
            "domainname": "any",
            "member": [{"name": "All TACACS+ Users"}]

        }

        response = local_user.local_group(**edit_local_group)
        logger.info(response)
        resp = local_user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp), 'TACACS', 'err: Failed to edit All TACACS Users')

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

    def test_09_login_via_tacacs_local_user(self):
        net_ex = netex(username="sslvpntestldaplocal", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn tacacs user login successfull with invalid user')

    def test_10_delete_tacacsuser(self):
        tacacs_user = user_tacacs.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: tacacs_user is not deleted successfully")

    def test_11_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')