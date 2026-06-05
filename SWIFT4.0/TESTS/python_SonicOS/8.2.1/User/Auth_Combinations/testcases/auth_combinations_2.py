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


class TC29_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76982"
    description = show_testcase_info(TESTPLAN, '2477796', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477796')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_06_login_via_local_user(self):
        net_ex = netex(username="sslvpntest", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, "Err: Authentication with Local Auth and NetExtender Client Failed")

    def test_07_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')


class TC30_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76983"
    description = show_testcase_info(TESTPLAN, '2477797', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477796')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: sslvpntest not created')

    @repeat_method(3)
    def test_06_login_via_local_user(self):
        net_ex = netex(username="sslvpntest", password="wpassword", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False,
                               "Err: Authentication with Local Auth and NetExtender Client Passed with InValid local user")

    def test_07_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntest')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntest"', 'err: user not deleted')


class TC31_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76984"
    description = show_testcase_info(TESTPLAN, '2477798', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477798')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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

    @repeat_method(3)
    def test_08_login_via_local_user(self):
        net_ex = netex(username="ldap_auto_1", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, "Err: Authentication with ldap Auth and NetExtender Client Failed")


class TC32_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76985"
    description = show_testcase_info(TESTPLAN, '2477799', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477799')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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

    @repeat_method(3)
    def test_08_login_via_ldap_user(self):
        net_ex = netex(username="ldap_auto_1", password="wS0nic@uto,", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False,
                               'err: Authentication with ldap Auth and NetExtender Client successfull with invalid ldap user')


class TC33_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76986"
    description = show_testcase_info(TESTPLAN, '2477800', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477800')
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
    def test_08_login_via_radius_user(self):
        net_ex = netex(username="radius_auto_1", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn radius user login not successfull')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC34_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76987"
    description = show_testcase_info(TESTPLAN, '2477801', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477801')
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
        net_ex = netex(username="radius_auto_1", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn radius user login  successfull with invalid user')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC35_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76990"
    description = show_testcase_info(TESTPLAN, '2477804', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477804')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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
        net_ex = netex(username="ldap_auto_1", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn NX ldap local user login not successfull')


class TC36_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76991"
    description = show_testcase_info(TESTPLAN, '2477805', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477805')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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
        net_ex = netex(username="ldap_auto_1", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn ldap local user login  successfull with invalid user')


class TC37_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76992"
    description = show_testcase_info(TESTPLAN, '2477806', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477806')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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
        net_ex = netex(username="sslvpntestldaplocal", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn NX local user login not successfull in ldap-local auth')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')


class TC38_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76993"
    description = show_testcase_info(TESTPLAN, '2477807', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477807')
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
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
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
        net_ex = netex(username="sslvpntestldaplocal", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False, 'err: sslvpn nx local ldap user login  successfull with invalid local user')

    def test_10_delete_localUser(self):
        stage_description = 'Delete the user '
        logger.info(stage_description)
        resp = local_user.delete_local_user_no_domain('sslvpntestldaplocal')
        resp1 = local_user.show_local_users()
        time.sleep(5)
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "sslvpntestldaplocal"', 'err: user not deleted')


class TC39_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76994"
    description = show_testcase_info(TESTPLAN, '2477808', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477808')
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
        net_ex = netex(username="radius_auto_1", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn nx radius-local user login not successfull')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC40_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76995"
    description = show_testcase_info(TESTPLAN, '2477809', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477809')
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
        net_ex = netex(username="radius_auto_1", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False,
                               'err: sslvpn nx radius local user login  successfull with invalid radius user')

    def test_09_delete_radiususer(self):
        radius_user = user_radius.del_radius_server(radiusserver_name="192.168.168.85")
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: Radius user is not deleted successfully")


class TC41_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76996"
    description = show_testcase_info(TESTPLAN, '2477810', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477810')
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
        net_ex = netex(username="sslvpntestldaplocal", password="S0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, True, 'err: sslvpn nx radius -local user login not successfull')

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


class TC42_Auth_combinations(Test):
    uuid = "SOSAIOT-TC-76997"
    description = show_testcase_info(TESTPLAN, '2477811', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477811')
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
        net_ex = netex(username="sslvpntestldaplocal", password="wS0nic@uto", netexurl='192.168.168.168:4433',
                       domain='LocalDomain')
        res = net_ex.install_nxlinux()
        res &= net_ex.NX_disconnect()
        Assertion.assert_equal(res, False,
                               'err: sslvpn nx radius-local user login  successfull with invalid local user')

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
