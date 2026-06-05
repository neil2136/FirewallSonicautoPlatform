import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293')
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

class TC003_ldap_user_settings(Test):
    uuid = "SOSAIOT-TC-77026"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
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

class TC011_ldap_protocol_version(Test):
    uuid = "SOSAIOT-TC-77026"
    description = show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_protocol_version(self):
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"protocol_version": 3,', "failed to get protocol version")

class TC038_ldap_use_ip(Test):
    uuid = "SOSAIOT-TC-77051"
    description = show_testcase_info(Parameter.TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '38')
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

class TC043_ldap_protocol_version3(Test):
    uuid = "SOSAIOT-TC-77054"
    description = show_testcase_info(Parameter.TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '43')
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

class TC056_ldap_microsoft_ad(Test):
    uuid = "SOSAIOT-TC-77041"
    description = show_testcase_info(Parameter.TESTPLAN, '56', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '56')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ldapuser(self):
        ldap_server = {
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

        ldap_user = ldap.edit_ldap_server(**ldap_server)
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        Assertion.assert_regular(json.dumps(resp), '"schema": "microsoft-active-directory"', "failed to get schema")

class TC061_ldap_default_user_group(Test):
    uuid = "SOSAIOT-TC-77064"
    description = show_testcase_info(Parameter.TESTPLAN, '61', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '61')
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

class TC064_ldap_default_user_group(Test):
    uuid = "SOSAIOT-TC-77066"
    description = show_testcase_info(Parameter.TESTPLAN, '64', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '64')
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

class TC065_ldap_default_user_group(Test):
    uuid = "SOSAIOT-TC-77067"
    description = show_testcase_info(Parameter.TESTPLAN, '65', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '65')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Limited Administrators',
            'mirror_user_groups': {
                "all": True,
                "have_members":True
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
        Assertion.assert_regular(json.dumps(resp), '"default_user_group": "Limited Administrators"',
                                 "default user group is defined.")

    def test_02_check_group(self):
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Trusted Users"', 'err: not a member of Trusted Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Everyone"', 'err: not a member of Everyone')
        Assertion.assert_regular(json.dumps(resp1), '"name": "Limited Administrators"',
                                 'err: not a member of Limited Administrators')

    # remove user from group
    def test_03_remove_user(self):
        member_json = {
            'groupname': 'Limited Administrators',
            'domain': 'any',
            'members': ['All LDAP Users']
        }
        resp = user.delete_members_from_group(**member_json)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "Limited Administrators"',
                                 'err: ldap users not removed from Limited Administrators')

class TC095_ldap_config_login(Test):

    uuid = "SOSAIOT-TC-77078"
    description = show_testcase_info(Parameter.TESTPLAN, '95', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '95')
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

class TC096_ldap_config_bind(Test):
    uuid = "SOSAIOT-TC-77079"
    description = show_testcase_info(Parameter.TESTPLAN, '96', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '96')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # configure ldap
    def test_02_config_ldapuser(self):
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
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        Assertion.assert_regular(json.dumps(resp), '"distinguished_name": "test"', "failed to config bind")

class TC133_ldap_user_login(Test):
    uuid = "SOSAIOT-TC-77081"
    jira = 'GEN8-7904'
    description = show_testcase_info(Parameter.TESTPLAN, '133', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '133')
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

    def test_07_import_ldap_users_without_cert(self):
        import_user = {
            "user": {
                "local": {
                    "user": [
                        {
                        "name": "test",
                        "domain": "os-autosnwl.com"
                        }
                    ]
		        }
	        }
        }
        user.import_local_usr_from_ldap(**import_user)
        resp = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "test"', "ERR: Importing LDAP User without certificate failed")
    @repeat_method(5)
    def test_08_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_TP293/lib/ui_ldap.py ' + \
              '-url ' + url + ' -user ldap_auto_1 -pwd S0nic@uto'
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2','eth1')
        logger.info(f"PC2 ETH1 IP (Expected): {PC2_ETH1_IP}")
        status = user_status.show_user_status_by_name('test')
        actual_ip = status['ip_address']  
        Assertion.assert_regular(actual_ip, PC2_ETH1_IP, "User IP should match PC2 ETH1 IP")

       

    # logout user
    def test_08_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class delete_ldap(Test):
    uuid = 'NonTC'

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

