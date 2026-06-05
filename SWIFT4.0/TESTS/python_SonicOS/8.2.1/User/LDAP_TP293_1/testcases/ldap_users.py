import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293_1')

from definition.initial_parameter import *

class config_ldap(Test):
    uuid = 'NonTC'

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")

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

class TC01_GUI_LDAP_is_included_in_Authentication_Method_list(Test):
    uuid = "SOSAIOT-TC-77022"
    description = show_testcase_info(Parameter.TESTPLAN, '1503613', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503613')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_protocol_version(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")

class TC02_LDAP_Users_Import_user_groups(Test):
    uuid = "SOSAIOT-TC-77023"
    description = show_testcase_info(Parameter.TESTPLAN, '1503615', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503615')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': False,
            'group_name': '',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": ""', "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')


class TC03_Import_user_All_selected_users(Test):
    uuid = "SOSAIOT-TC-77029"
    description = show_testcase_info(Parameter.TESTPLAN, '1503623', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503623')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldapuser(self):
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

        ldap_user = ldap.edit_ldap_server(**add_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to use ip as host")

class TC04_Import_user_select_specific_user_at_under_from_the_LDAP_server_path(Test):
    uuid = "SOSAIOT-TC-77030"
    description = show_testcase_info(Parameter.TESTPLAN, '1503624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': False,
            'group_name': '',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"protocol_version": 3,', "failed to set protocol version")

class TC05_Functional_LDAP_Configuration_Test_LDAP_user_for_valid_name_password(Test):
    uuid = "SOSAIOT-TC-77049"
    description = show_testcase_info(Parameter.TESTPLAN, '1503645', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503645')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
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

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
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
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user ldap_auto_1 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_regular(json.dumps(status), '"name": "ldap_auto_1"', "failed to get user status")



class TC06_Functional_LDAP_Configuration_Test_LDAP_User_with_invalid_name_password(Test):
    uuid = "SOSAIOT-TC-77050"
    description = show_testcase_info(Parameter.TESTPLAN, '1503646', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503646')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
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

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
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
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user incorrect -pwd incorrect'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_not_regular(json.dumps(status), '13.0.0.1', "failed to get user status")



class TC07_Functional_LDAP_version_2_is_used(Test):
    uuid = "SOSAIOT-TC-77055"
    description = show_testcase_info(Parameter.TESTPLAN, '1503651', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503651')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Guest Services',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": "Guest Services"',
                                 "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Guest Services"', 'err: not a member of Guest Services')

class TC08_Functional_Login_password_is_using_incorrect_value(Test):
    uuid = "SOSAIOT-TC-77056"
    description = show_testcase_info(Parameter.TESTPLAN, '1503652', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503652')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
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

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
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
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user ldap_auto_1 -pwd incorrect'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_not_regular(json.dumps(status), '13.0.0.4', "failed to get user status")


    

class TC09_Functional_Connection_to_LDAP_server_TLS_is_not_used(Test):

    uuid = "SOSAIOT-TC-77057"
    description = show_testcase_info(Parameter.TESTPLAN, '1503653', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503653')
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

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")

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

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "ldap_auto_1"', "failed to config bind")

class TC10_Functional_Default_user_group_is_Everyone(Test):
    uuid = "SOSAIOT-TC-77065"
    description = show_testcase_info(Parameter.TESTPLAN, '1503669', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503669')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # configure ldap
    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Guest Services',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": "Guest Services"',
                                 "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        # Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')
        # Assertion.assert_regular(json.dumps(resp1), '"name": "Guest Services"', 'err: not a member of Guest Services')

class TC11_Functional_Default_user_group_is_a_custom_group(Test):
    uuid = "SOSAIOT-TC-77068"
    description = show_testcase_info(Parameter.TESTPLAN, '1503672', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503672')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Guest Services',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": "Guest Services"',
                                 "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        # Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')
class TC12_Functional_Allow_only_users_listed_locally(Test):
    uuid = "SOSAIOT-TC-77069"
    description = show_testcase_info(Parameter.TESTPLAN, '1503673', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503673')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
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

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
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
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user ldap_auto_1 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_regular(json.dumps(status), '"name": "ldap_auto_1"', "failed to get user status")

    # logout user
    def test_08_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")



class TC13_Functional_LDAP_Local_Users_authentication(Test):
    uuid = "SOSAIOT-TC-77071"
    description = show_testcase_info(Parameter.TESTPLAN, '1503675', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503675')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    # configure ldap

    def test_02_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")

    def test_03_config_ldapuser(self):
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

    def test_04_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_06_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
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
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_07_Import_ldap_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'password',
            'domain': 'os-autosnwl.com',

        }

        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293_1/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user ldap_auto_1 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('test')
        Assertion.assert_regular(json.dumps(status), '"name": "ldap_auto_1"', "failed to get user status")

    # logout user
    def test_08_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")


class TC14_Functional_Use_LDAP_Name(Test):
    uuid = "SOSAIOT-TC-77052"
    description = show_testcase_info(Parameter.TESTPLAN, '1503648', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503648')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Guest Services',
            'mirror_user_groups': {
                "all": True,
                "have_members": True
            },
            "refresh": {
                "period": 6
            },

            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
        }

        ldap_user = ldap.ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": "Guest Services"',
                                 "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Guest Services"', 'err: not a member of Guest Services')


class delete_ldap(Test):
    uuid = 'NonTC'

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

