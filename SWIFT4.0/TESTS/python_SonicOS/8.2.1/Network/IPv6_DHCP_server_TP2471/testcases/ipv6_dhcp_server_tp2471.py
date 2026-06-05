from definition.settings import *
from definition.config_page_via_ui import *
from definition.utils import *


# Excepted:DHCPv6 Server can be disabled and enabled
class TestTC01_Verify_DHCPv6_Server_can_be_disabled_and_enabled(Test):
    uuid = "SOSAIOT-TC-56496"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_disable_dhcpv6_server(self):
        dhcp_server_setting_v6 = {
            "dhcp_server": {
                "ipv6": {
                    "enable": False,
                }
            }
        }
        rc = dhcpserverapi.config_dhcp_server_settings(**dhcp_server_setting_v6)
        Assertion.assert_equal(rc, True, "ERR: disable dhcpv6 server failed")

    def test_03_enable_dhcpv6_server(self):
        dhcp_server_setting_v6 = {
            "dhcp_server": {
                "ipv6": {
                    "enable": True,
                }
            }
        }
        rc = dhcpserverapi.config_dhcp_server_settings(**dhcp_server_setting_v6)
        Assertion.assert_equal(rc, True, "ERR: enable dhcpv6 server failed")


# Excepted:dhcpv6 server single dynamic entry can be deleted
class TestTC17_Verify_DHCPv6_server_single_dynamic_entry_can_be_deleted(Test):
    uuid = "SOSAIOT-TC-56504"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcpv6_server_dynamic_scope(self):
        dict_update = {
            "name": "TC17_scope",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_delete_dhcpv6_server_dynamic_scope(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('TC17_scope', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:dhcpv6 server multiple dynamic entries can be deleted
class TestTC18_Verify_DHCPv6_server_multiple_dynamic_entries_can_be_deleted(Test):
    uuid = "SOSAIOT-TC-56505"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcpv6_server_multiple_dynamic_scope(self):
        tag = []
        dict_update_1 = {
            "name": "scope_1",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
        }
        dict_update_2 = {
            "name": "scope_2",
            "range": {
                "from": "1101:1::130",
                "to": "1101:1::140"
            },
            "prefix": "1101:1::0",
        }
        dict_update_3 = {
            "name": "scope_3",
            "range": {
                "from": "1201:1::150",
                "to": "1201:1::160"
            },
            "prefix": "1201:1::0",
        }
        dynamic_scopes_list = [dict_update_1, dict_update_2, dict_update_3]
        for scope in dynamic_scopes_list:
            dhcpv6_server_dynamic_base_dict.update(scope)
            rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
            if rc is False:
                logger.info(f'add dhcpv6 server dynamic scope {scope["name"]} failed')
            tag.append(rc)
        Assertion.assert_equal(all(tag), True, "ERR: add dhcpv6 server multiple dynamic scopes failed")

    def test_03_delete_dhcpv6_server_multiple_dynamic_scopes(self):
        tag = []
        scope_name_list = ['scope_1', 'scope_2', 'scope_3']
        for scope_name in scope_name_list:
            rc = dhcpserverapi.del_dhcp_server_scope_dynamic(scope_name, version=6)
            if rc is False:
                logger.info(f'delete dhcpv6 dynamic scope {scope_name} failed')
            tag.append(rc)
        Assertion.assert_equal(all(tag), True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:valid name can be allowed
class TestTC02_Verify_valid_name_can_be_allowed(Test):
    uuid = "SOSAIOT-TC-56507"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcpv6_dynamic_scope_with_valid_name(self):
        dict_update = {
            "name": "scope_1234567890",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_valid_name(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_1234567890', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:valid dynamic addresses can be allowed
class TestTC05_Verify_valid_dynamic_addresses_can_be_allowed(Test):
    uuid = "SOSAIOT-TC-56516"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_valid_addresses(self):
        dict_update1 = {
            "name": "scope_1",
            "range": {
                "from": Parameter.STATIC_PRIMARY_DNS,
                "to": "2001:25de::caee"
            },
            "prefix": "2001:25de::0",
        }

        dict_update2 = {
            "name": "scope_2",
            "range": {
                "from": "2001::1",
                "to": "2001::4"
            },
            "prefix": "2001::0",
        }

        dict_update3 = {
            "name": "scope_3",
            "range": {
                "from": Parameter.STATIC_SECONDARY_DNS,
                "to": "2001:0db8:85a3:08d3:1319:8a2e:0400:7344"
            },
            "prefix": "2001:0db8:85a3:08d3:1319:8a2e:0370:0",
        }
        dict_list = [dict_update1, dict_update2, dict_update3]
        tag = []
        for list in dict_list:
            dhcpv6_server_dynamic_base_dict.update(list)
            res = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
            tag.append(res)
        logger.info(tag)
        Assertion.assert_equal(all(tag), True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_delete_dhcpv6_dynamic_scope(self):
        scope_name = ['scope_1', 'scope_2', 'scope_3']
        tag = []
        for s_name in scope_name:
            res = dhcpserverapi.del_dhcp_server_scope_dynamic(s_name, version=6)
            tag.append(res)
        logger.info(tag)
        Assertion.assert_equal(all(tag), True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted: valid prefix is allowed
class TestTC07_Verify_valid_prefix_is_allowed(Test):
    uuid = "SOSAIOT-TC-56521"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_valid_prefix(self):
        dict_update = {
            "name": "scope_1234567890",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
            "lifetime": {
                "valid": 71582789,
                "preferred": 564522
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope with valid prefix failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_valid_prefix(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_1234567890', version=6)
        dict_update_lifetime = {
            "range": {
                "from": "",
                "to": ""
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update_lifetime)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope with valid prefix failed")


# Excepted: Valid Lifetime Value is allowed
class TestTC09_Verify_valid_lifetime_value_is_allowed(Test):
    uuid = "SOSAIOT-TC-56523"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_valid_lifetime(self):
        dict_update = {
            "name": "scope_1234567890",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
            "lifetime": {
                "valid": 71582789,
                "preferred": 564522
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope with valid lifetime failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_valid_name(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_1234567890', version=6)
        dict_update_lifetime = {
            "lifetime": {
                "valid": 2160,
                "preferred": 1440
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update_lifetime)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:c Valid Preferred Lifetime Value is allowed
class TestTC11_Verify_valid_preferred_lifetime_value_is_allowed(Test):
    uuid = "SOSAIOT-TC-56498"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_valid_preferred_lifetime(self):
        dict_update = {
            "name": "scope_1234567890",
            "range": {
                "from": "1001:1::100",
                "to": "1001:1::120"
            },
            "prefix": "1001:1::0",
            "lifetime": {
                "valid": 71582789,
                "preferred": 71582789
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope with valid preferred lifetime failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_valid_name(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_1234567890', version=6)
        dict_update_lifetime = {
            "lifetime": {
                "valid": 2160,
                "preferred": 1440
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update_lifetime)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope with valid name failed")


# Excepted:comment can be configured successfully
class TestTC12_Verify_comment_can_be_configured_successfully(Test):
    uuid = "SOSAIOT-TC-56499"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_comment(self):
        dict_update = {
            "name": "scope_tc12",
            "range": {
                "from": "3001:2::100",
                "to": "3001:2::120"
            },
            "prefix": "3001:2::0",
            "comment": 'test',
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_comment(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_tc12', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepte:valid DNS value can be configured successfully
class TestTC14_Verify_valid_dns_value_can_be_configured_successfully(Test):
    uuid = "SOSAIOT-TC-56501"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_valid_dns(self):
        dict_update = {
            "name": "scope_112",
            "range": {
                "from": "3001:2::100",
                "to": "3001:2::120"
            },
            "prefix": "3001:2::0",
            "comment": 'test',
            "dns": {
                "server": {
                    "static": {
                        "primary": Parameter.STATIC_PRIMARY_DNS,
                        "secondary": Parameter.STATIC_SECONDARY_DNS,
                        "tertiary": "::"
                    }
                }
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_delete_dhcpv6_dynamic_scope_with_comment(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_112', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:invalid name is not be allowed
class TestTC03_Verify_invalid_name_is_not_be_allowed(Test):
    uuid = "SOSAIOT-TC-56510"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_invalid_name(self):
        general_dict = {
            'name_invalid': [{'empty': ''},
                             {'long more than 50': '012345678901234567890123456789012345678901234567890123456789'}],
            'prefix': '2002:1:1:0',
            'range start': '2002:1:1:20',
            'range end': '2002:1:1:20'}
        res = fwpage.configure_dhcpv6_dynamic_scope_with_invalid_name(**general_dict)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid name successfully")


# Excepted: Invalid dynamic range is not allowed
class TestTC04_Verify_invalid_dynamic_range_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56514"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_invalid_prefix(self):
        dict_1 = {
            'name': 'scope_dynamic',
            'range start': '2001::25de::cade',
            'range end': '2001::25de::cade',
            'prefix': '2001::0'
        }
        dict_2 = {
            'name': 'scope_dynamic',
            'range start': '2001:100g::1',
            'range end': '2001:100g::1',
            'prefix': '2001::0'
        }
        dict_3 = {
            'name': 'scope_dynamic',
            'range start': '2001:250:abcg::1',
            'range end': '2001:250:abcg::1',
            'prefix': '2001:250::0'
        }
        dict_4 = {
            'name': 'scope_dynamic',
            'range start': '2001:250:6003:123:1230:111g::1',
            'range end': '2001:250:6003:123:1230:111g::1',
            'prefix': '2001:250::0'
        }

        dict_list = [dict_1, dict_2, dict_3, dict_4]
        res = fwpage.configure_dhcpv6_dynamic_scope_with_invalid_range(dict_list)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid prefix successfully")

    def test_03_get_dhcpv6_dynamic_scope(self):
        scoperes = dhcpserverapi.get_dhcp_server_scope_dynamic(version=6)
        logger.info(f'get dhcp server scopes:{scoperes}')
        flag = True if 'scope_dynamic' not in scoperes else False
        Assertion.assert_equal(flag, True, "ERR: check dhcpv6 dynamic scope failed")


# Excepted: Invalid prefix Value is not allowed
class TestTC06_Verify_invalid_prefix_value_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56520"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_invalid_prefix(self):
        general_dict = {
            'name': 'scope_dynamic',
            'range start': '4002:1:1::20',
            'range end': '4002:1:1::30',
            'prefix_invalid': [{'invalid_value': '4002:1:1:1'}, {'invalid_format': '2g:1'}]
        }
        res = fwpage.configure_dhcpv6_dynamic_scope_with_invalid_prefix(**general_dict)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid prefix successfully")

    def test_03_get_dhcpv6_dynamic_scope(self):
        scoperes = dhcpserverapi.get_dhcp_server_scope_dynamic(version=6)
        logger.info(f'get dhcp server scopes:{scoperes}')
        flag = True if 'scope_dynamic' not in scoperes else False
        Assertion.assert_equal(flag, True, "ERR: check dhcpv6 dynamic scope with invalid prefix successfully")


# Excepted: Invalid Valid Lifetime Value is not allowed
class TestTC08_Verify_invalid_valid_lifetime_value_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56522"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_invalid_lifetime(self):
        general_dict = {
            'name': 'scope_dynamic',
            'prefix': '4002:1:1::0',
            'range start': '4002:1:1::20',
            'range end': '4002:1:1::30',
            'valid_lifetime_invalid': [{'empty': ' '}, {'negative': '-5'}, {'decimal': '0.5'}]
        }
        res = fwpage.configure_dhcpv6_dynamic_scope_with_valid_lifetime_invalid(**general_dict)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid lifetime successfully")

    def test_03_get_dhcpv6_dynamic_scope(self):
        scoperes = dhcpserverapi.get_dhcp_server_scope_dynamic(version=6)
        logger.info(f'get dhcp server scopes:{scoperes}')
        flag = True if 'scope_dynamic' not in scoperes else False
        Assertion.assert_equal(flag, True, "ERR: check dhcpv6 dynamic scope with invalid lifetime failed")


# Excepted: Invalid Preferred Lifetime Value is not allowed
class TestTC10_Verify_invalid_preferred_lifetime_value_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56497"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_dhcpv6_dynamic_scope_with_invalid_preferred_lifetime(self):
        general_dict = {
            'name': 'scope_dynamic',
            'prefix': '4002:1:1::0',
            'range start': '4002:1:1::20',
            'range end': '4002:1:1::30',
            'preferred_lifetime_invalid': [{'pref more than valid': '3440'}, {'pref negative': '-5'}]
        }
        res = fwpage.configure_dhcpv6_dynamic_scope_with_preferred_lifetime_invalid(**general_dict)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid preferred lifetime value successfully")

    def test_03_get_dhcpv6_dynamic_scope(self):
        scoperes = dhcpserverapi.get_dhcp_server_scope_dynamic(version=6)
        logger.info(f'get dhcp server scopes:{scoperes}')
        flag = True if 'scope_dynamic' not in scoperes else False
        Assertion.assert_equal(flag, True, "ERR: check dhcpv6 dynamic scope with invalid preferred lifetime failed")


# Excepte:invalid DNS value is not allowed
class TestTC13_Verify_invalid_dns_value_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56500"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcpv6_server_lease_scope_on_x2(self):
        dict_update = {
            "name": "scope_test",
            "range": {
                "from": "4001:1::100",
                "to": "4001:1::120"
            },
            "prefix": "4001:1::0",
            "dns": {
                "server": {
                    'static': {
                        "primary": "::",
                        "secondary": "::",
                        "tertiary": "::"
                    }
                }
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_03_configure_dhcpv6_dynamic_scope_with_invalid_dns(self):
        dnsserverlist = ['4001::25de::cade', '100g::1', '4001:100g::1', '4001:250:abcg::1', '4001:250:6002:100g::1',
                         '4001:250:6003:123:123g::1', '4001:']
        res = fwpage.configure_dhcpv6_dynamic_scope_with_invalid_dns_server('4001:1:: / 64', dnsserverlist)
        logger.info(f'res is {res}')
        Assertion.assert_equal(res, True, "ERR: input invalid dns successfully")


# Excepted: Invalid Domain is not allowed
class TestTC16_Verify_invalid_domain_is_not_allowed(Test):
    uuid = "SOSAIOT-TC-56503"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_invalid_domanin_name(self):
        d_name_list = ["@^&*ty", "@()"]
        res = fwpage.configure_dhcpv6_dynamic_scope_with_invalid_domain_name('4001:1:: / 64', d_name_list)
        Assertion.assert_equal(res, True, "ERR: configure invalid domain name successfully")

    def test_03_delete_dhcpv6_dynamic_scope_with_valid_name(self):
        rc = dhcpserverapi.del_dhcp_server_scope_dynamic('scope_test', version=6)
        Assertion.assert_equal(rc, True, "ERR: delete dhcpv6 dynamic scope failed")


# Excepted:DHCP clients DNS settings match SonicWALL DNS settings when using dynamic IPs .
class TestTC15_Verify_DHCPv6_scope_with_inherit_dns(Test):
    uuid = "SOSAIOT-TC-56502"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_specify_ipv6_dns_servers(self):
        ipv6_dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": "0.0.0.0",
                        "secondary": "0.0.0.0",
                        "tertiary": "0.0.0.0"
                    },
                    "ipv6": {
                        "inherit": False,
                        "static": {
                            "primary": Parameter.PRIMARY_DNS,
                            "secondary": Parameter.SECONDARY_DNS,
                            "tertiary": Parameter.TERTIARY_DNS
                        },
                        "preferred": False
                    }
                }
            }
        }

        res = dnssettingsapi.set_dns(**ipv6_dns_dict)
        Assertion.assert_equal(res, True, "ERR: specify ipv6 dns failed")

    def test_03_add_dhcpv6_server_lease_scope_on_x2(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "dns": {
                "server": {
                    'inherit': True,
                }
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_04_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x2',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_05_get_ipv6_address_and_dns_server_from_dhcpv6_server(self):
        flag = False
        start_capture_and_clear_packets(packetmonitorapi)
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        if ipv6addr:
            output = PC2_Login.send_command('cat /var/lib/dhclient/dhclient6.leases')
            logger.info(output)
            checklist = [Parameter.PRIMARY_DNS, Parameter.SECONDARY_DNS, Parameter.TERTIARY_DNS]
            flag = True if all(i in output for i in checklist) else False
        Assertion.assert_equal(flag, True, "ERR: get IPv6 address and dns failed")


# Expected:Verify the IAID for each DHCP lease entry
class TestTC19_Check_IAID_in_each_DHCPv6_lease(Test):
    uuid = "SOSAIOT-TC-56506"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_verify_iaid_in_dhcpv6_lease(self):
        flag = False
        leaselist = dhcpserverapi.get_dhcp_server_leases(version=6)
        if leaselist:
            iaidreslist = re.findall("(?<='iaid': )\d+", str(leaselist), re.I)
            logger.info(f'iaidlist is:{iaidreslist}')
            if iaidreslist:
                flag = True if len(leaselist) == len(iaidreslist) else False
        else:
            logger.error('there is no dhcpv6 leases displayed')
        Assertion.assert_equal(flag, True, "ERR: verify iaid in dhcpv6 lease table failed")


# Expected:Verify the DUID for each DHCP lease entry
class TestTC20_Check_DUID_in_each_DHCPv6_lease(Test):
    uuid = "SOSAIOT-TC-56508"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_verify_duid_in_dhcpv6_lease_table(self):
        flag = False
        leaselist = dhcpserverapi.get_dhcp_server_leases(version=6)
        if leaselist:
            duidreslist = re.findall("(?<='duid': ')([A-Za-z0-9]+:){13}[A-Za-z0-9]+", str(leaselist), re.I)
            logger.info(f'duidlist is:{duidreslist}')
            if duidreslist:
                flag = True if len(leaselist) == len(duidreslist) else False
        else:
            logger.error('there is no dhcpv6 leases displayed')
        Assertion.assert_equal(flag, True, "ERR: verify duid in dhcpv6 lease table failed")
        # Assertion.assert_equal(True, True, "ERR: verify duid in dhcpv6 lease table failed")

    def test_03_release_ipv6_address_on_pc2(self):
        res = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(res, True, "ERR: release IPv6 address on PC2 failed")


# Expected: DHCP server act as Stateful DHCP server,M=1,O=1, message between client and server is valid when client
# in LAN zone
class TestTC21_Verify_LAN_zone_with_statefull_mode(Test):
    uuid = "SOSAIOT-TC-56509"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_ipv6_address_from_dhcpv6_server_dynamic_scope(self):
        start_capture_and_clear_packets(packetmonitorapi)
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: get ipv6 address from dhcpv6 server dynamic scope failed")

    def test_03_check_dhcpv6_packets_for_get_ipv6_address(self):
        dhcpv6typeinlist = [
            'Message type: Solicit (1)',
            'Message type: Advertise (2)',
            'Message type: Request (3)',
            'Message type: Reply (7)'
        ]
        packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
        Assertion.assert_equal(packetres, True, "ERR: check dhcpv6 packets failed")

    def test_04_release_ipv6_lease(self):
        res = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(res, True, "ERR: release ipv6 address on PC2 failed")


# Excepted:DHCP client can't get any info from DHCP server, if the DHCP server scope was disabled.
class TestTC30_Verify_disable_DHCPv6_scope(Test):
    uuid = "SOSAIOT-TC-56511"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_ipv6_address_from_dhcpv6_server_and_check_dhcpv6_lease_table_before_disable_scope(self):
        flag = False
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        leaselist = dhcpserverapi.get_dhcp_server_leases(version=6)
        if ipv6addr and leaselist:
            if ipv6addr in str(leaselist):
                flag = True
            else:
                logger.info(f'{ipv6addr} is not in current dhcpv6 lease table')
        else:
            logger.info('there is no current dhcpv6 lease table')
        Assertion.assert_equal(flag, True, "ERR: get ipv6_address before disable scope failed")

    def test_03_disable_dhcpv6_server_dynamic_scope(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "enable": False,
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        logger.info(f'dhcpv6_server_dynamic_scope_dict is:{dhcpv6_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True, "ERR: disable dhcpv6 dynamic scope failed")

    @repeat_method(3)
    def test_04_check_dhcpv6_lease_table_after_disable_scope(self):
        time.sleep(20)
        leaselist = dhcpserverapi.get_dhcp_server_leases(version=6)
        flag = True if not leaselist else False
        if flag is False:
            # sometime leases are not disappeared after disable scope,so when this case occurs,check below
            # information by cli
            scoperes = dhcpservercli.show_dhcpserver_scopev6('scope', 'dynamic')
            logger.info(scoperes)
            leaseres = dhcpservercli.show_dhcpserver_leases_statistic(version='ipv4')
            logger.info(leaseres)
        Assertion.assert_equal(flag, True, "ERR: check dhcpv6 lease table after disable scope failed")

    def test_05_get_ipv6_address_from_dhcpv6_server_after_disable_scope_on_pc2(self):
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        flag = True if not ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC2 get ipv6 address failed after disable scope")

    def test_06_get_ipv6_address_from_dhcpv6_server_after_disable_scope_on_pc3(self):
        ipv6addr = get_dhcpv6_leases(PC3_Login, 'eth1')
        flag = True if not ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC3 get ipv6 address failed after disable scope")

    def test_07_inital_setup_enable_dhcpv6_scope_and_release_ipv6_address_on_pc2(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "enable": True,
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        logger.info(f'dhcpv6_server_dynamic_scope_dict is:{dhcpv6_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(res & releaseres, True, "ERR: enable dhcpv6 dynamic scope and release ipv6 address on pc2 failed")

# Expected:  Multiple Client in same interface (Dynamic entry)
class TestTC33_Verify_multiple_client_in_same_interface(Test):
    uuid = "SOSAIOT-TC-56532"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_ipv6_address_from_dhcpv6_server_on_pc2(self):
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC2 get ipv6 address from X2 failed ")

    def test_03_get_ipv6_address_from_dhcpv6_server_on_pc3(self):
        ipv6addr = get_dhcpv6_leases(PC3_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC3 get ipv6 address from X2 failed ")

    def test_04_release_ipv6_address_on_pc2_and_on_pc3(self):
        releaseres1 = release_dhcpv6_lease(PC2_Login, 'eth1')
        releaseres2 = release_dhcpv6_lease(PC3_Login, 'eth1')
        Assertion.assert_equal(releaseres1 & releaseres2, True, "ERR: release ipv6 address on pc2 and pc3 failed")


# Expected:   Multiple Client in different interface (Dynamic entry)
class TestTC34_Verify_multiple_client_in_different_interface(Test):
    uuid = "SOSAIOT-TC-56533"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcpv6_dynamic_scope_on_x3(self):
        dict_update = {
            "name": "x3_scope",
            "range": {
                "from": "3001:1::100",
                "to": "3001:1::120"
            },
            "prefix": "3001:1::0",
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope on X3 failed")

    def test_03_get_ipv6_address_from_dhcpv6_server_on_pc2(self):
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC2 get ipv6 address from X2 failed ")

    # def test_04_get_ipv6_address_from_dhcpv6_server_on_remote_dut_x3(self):
    #     flag = False
    #     # x3 ipv6 is static mode in init_fw
    #     x3_v6_dict_dhcpv6 = {
    #         'name': 'X3',
    #         'mode': 'dhcpv6',
    #         'listen_router_advertisement': True
    #     }
    #     # change from static mode(by default) to dhcpv6 mode
    #     rc = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_dhcpv6)
    #     logger.info(f'change x3 from static mode to dhcpv6 mode is :{rc}')
    #     clickrelease = reinterfacev4api.click_dhcp_release('x3', version='v6')
    #     logger.info(clickrelease)
    #     clickrenew = reinterfacev4api.click_dhcp_renew('x3', version='v6')
    #     if clickrenew:
    #         time.sleep(10)
    #         ipv6res = get_dhcpv6_leases_on_remote_dut(reinterfacecli, 'X3', 'ipv6')
    #         logger.info(f'ipv6 address on remote dut is {ipv6res}')
    #         flag = True if ipv6res else False
    #     Assertion.assert_equal(flag, True, "ERR: get ipv6 address on remote dut x3 failed")
    #     # Assertion.assert_equal(True, True, "ERR: get ipv6 address on remote dut x3 failed")

    def test_04_get_ipv6_address_from_dhcpv6_server_on_pc5(self):
        ipv6addr = get_dhcpv6_leases(PC5_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: get ipv6 address from remote dut x3 failed ")

    def test_05_release_ipv6_address_on_pc2(self):
        releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(releaseres, True, "ERR: release ipv6 address on pc2 failed")

    def test_06_release_ipv6_address_on_pc5(self):
        releaseres = release_dhcpv6_lease(PC5_Login, 'eth1')
        Assertion.assert_equal(releaseres, True, "ERR: release ipv6 address on pc5 failed")


# Expected:  IP conflicts (client number bigger than ip address number in scope.)
class TestTC39_Verify_client_number_bigger_than_scope_range(Test):
    uuid = "SOSAIOT-TC-56535"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_dhcpv6_scope_range_with_one_number(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::100"
            },
            "prefix": "2001:1::0",
            "enable": True,
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        logger.info(f'dhcpv6_server_dynamic_scope_dict is:{dhcpv6_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True, "ERR: enable dhcpv6 dynamic scope failed")

    def test_03_get_ipv6_address_from_dhcpv6_server_on_pc2(self):
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC2 get ipv6 address from X2 failed ")

    def test_04_get_ipv6_address_from_dhcpv6_server_on_pc3(self):
        ipv6addr = get_dhcpv6_leases(PC3_Login, 'eth1')
        flag = True if not ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: PC3 get ipv6 address from X2 failed ")

    def test_05_enable_dhcpv6_scope_and_release_ipv6_address_on_pc2(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "enable": True,
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        logger.info(f'dhcpv6_server_dynamic_scope_dict is:{dhcpv6_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        logger.info(res)
        releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(res & releaseres, True,"ERR: enable dhcpv6 dynamic scope and release ipv6 address on PC2 failed")


# Expected: Support rapid Commit option
class TestTC35_Verify_rapid_commit_option(Test):
    uuid = "SOSAIOT-TC-56534"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x3',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    # def test_03_configure_x3_to_static_mode(self):
    #     x3_v6_dict_static = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'zone': 'WAN',
    #         'ip': '',
    #         'prefix_length': 64
    #     }
    #     rc = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_static)
    #     Assertion.assert_equal(rc, True, "ERR: Config X3 to static mode failed")

    def test_04_get_ipv6_address_from_dhcpv6_server_on_pc5_and_check_rapid_commit(
            self):  # change to use linnux PC to test rapid_commit since there is bug on remote dut
        flag = False
        start_capture_and_clear_packets(packetmonitorapi)
        initial_pc_eth_for_get_dhcpv6_lease(PC5_Login, 'eth1')
        cmds = [
            #  Create DHCPv6 client configuration file with Rapid Commit option
            "echo 'send dhcp6.rapid-commit;' | sudo tee /etc/dhcp/dhclient6.conf", 
            f'timeout 20 dhclient -6  eth1 -v -cf /etc/dhcp/dhclient6.conf',
            # must input config_file,otherwise will not work
            f'ifconfig eth1'
        ]
        leaseoutput = PC5_Login.send_commands(cmds)
        lease_ipv6 = re.search('(?<=inet6 )\d+\:\d+\::[A-Za-z0-9]+', leaseoutput, re.I).group()
        if lease_ipv6:
            dhcpv6typeinlist = [
                'Message type: Solicit (1)',
                'Message type: Reply (7)',
                'Option: Rapid Commit (14)'
            ]
            dhcpv6typeoutlist = [
                'Message type: Advertise (2)',
                'Message type: Request (3)',
            ]
            (packetintres, packetouttres) = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist,
                                                                 dhcpv6typeoutlist)
            logger.info(f'packetintres is:{packetintres},packetoutres is:{packetouttres}')
            if packetintres and packetouttres:
                flag = True
        else:
            logger.error("eth1 on PC5 doesn't get ipv6 address,please check...")
        Assertion.assert_equal(flag, True, "ERR: check rapid commit failed")

    # def test_04_renew_dhcpv6_on_remote_dut_x3_and_check_rapid_commit(self):
    #     flag = False
    #     start_capture_and_clear_packets(packetmonitorapi)
    #     x3_v6_dict_dhcpv6 = {
    #         'name': 'X3',
    #         'mode': 'dhcpv6',
    #         'dhcpv6': {
    #             'rapid_commit': True,
    #         }
    #     }
    #     rc = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_dhcpv6)
    #     logger.info(f'change x3 from static mode to dhcpv6 mode is :{rc}')
    #     dhcpv6typeinlist = [
    #         'Message type: Solicit (1)',
    #         'Message type: Reply (7)',
    #         'Option: Rapid Commit (14)'
    #     ]
    #     dhcpv6typeoutlist = [
    #         'Message type: Advertise (2)',
    #         'Message type: Request (3)',
    #     ]
    #     (packetintres, packetouttres) = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist, dhcpv6typeoutlist)
    #     logger.info(f'packetintres is:{packetintres},packetoutres is:{packetouttres}')
    #     if packetintres and packetouttres:
    #         flag = True
    #     else:
    #         for each in range(0, 6):
    #             time.sleep(10)
    #             # release ipv6 address if it exists
    #             ipv6addr = get_dhcpv6_leases_on_remote_dut(reinterfacecli, 'x3', 'ipv6')
    #             if ipv6addr:
    #                 logger.info(f'interface has got ipv6 address:{ipv6addr},so click release it firstly')
    #                 reinterfacev4api.click_dhcp_release('x3', version='v6')

    #             time.sleep(10)
    #             start_capture_and_clear_packets(packetmonitorapi)
    #             clickrenew = reinterfacev4api.click_dhcp_renew('x3', version='v6')
    #             time.sleep(20)
    #             if clickrenew:
    #                 (packetintres, packetouttres) = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist, dhcpv6typeoutlist)
    #                 logger.info(f'packetintres is:{packetintres},packetoutres is:{packetouttres}')
    #                 if packetintres and packetouttres:
    #                     flag = True
    #                     break
    #             else:
    #                 logger.info('click renew faild')
    #         else:
    #             logger.info(f'run {each} times totally')
    #     Assertion.assert_equal(flag, True, "ERR: check rapid commit failed")

    def test_05_release_ipv6_address_on_pc5_and_initial_dhcpv6(self):
        release_dhcpv6_lease(PC5_Login, 'eth1')
        initial_pc_eth_for_get_dhcpv6_lease(PC5_Login, 'eth1')
        Assertion.assert_equal(True, True, "ERR: release ipv6 address on pc5 failed")


# Expected: The user will ensure that the DHCP server act correct at T1 time
class TestTC28_Verify_DHCP_server_act_correct_at_t1_time(Test):
    uuid = "SOSAIOT-TC-56531"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']
    t1_time = ContextVar('0')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_dynamic_dhcpv6_scope_lifetime(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "lifetime": {
                "valid": 3,
                "preferred": 1
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: modify dynamic dhcpv6 scope lifetime failed")

    def test_03_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x2',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_04_release_and_get_ipv6_address_on_pc1_eth1(self):
        flag = False
        PC2_Login.send_command('ifconfig eth1')
        releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        logger.info(f'releaseres is {releaseres}')
        time.sleep(10)
        if releaseres:
            start_capture_and_clear_packets(packetmonitorapi)
            ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
            if ipv6addr:
                logger.info(f'get ipv6 address is :{ipv6addr}')
                t1time = get_t1_time_in_dhcpv6_packets(packetmonitorapi, PC1_Login)
                logger.info(f'get t1 time is :{t1time}')
                self.t1_time.set(t1time)
                flag = True
        else:
            logger.error('release failed')
        Assertion.assert_equal(flag, True, "ERR: Release and get dhcpv6 lease failed")

    def test_05_renew_ipv6_address_on_pc2_eth1(self):
        start_capture_and_clear_packets(packetmonitorapi)
        t_time = self.t1_time.get()
        logger.info(f't_time is :{t_time}')
        time.sleep(int(t_time) + 2)
        dhcpv6typeinlist = [
            'Message type: Renew (5)',
            'Message type: Reply (7)'
        ]
        packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
        logger.info(f'packetres is {packetres}')
        ParamCases.tc31result = True if packetres else False
        Assertion.assert_equal(packetres, True, "ERR: renew ipv6 address on pc2 failed")

    def test_06_inital_dhcpv6_scope_and_release_ipv6_address_on_pc2(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "lifetime": {
                "valid": 2160,
                "preferred": 1440
            },
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        releaserespc1 = release_dhcpv6_lease(PC2_Login, 'eth1')
        logger.info(rc, releaserespc1)
        Assertion.assert_equal(rc & releaserespc1, True,"ERR: inital dhcpv6 scope and release ipv6 address on pc2 failed")


# Expected: DHCPv6 server act correct when Server get renew message from Client
class TestTC31_Verify_renew_ipv6_address(Test):
    uuid = "SOSAIOT-TC-56512"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_renew_ipv6_address_on_pc2_eth1(self):
        logger.info(ParamCases.tc31result)
        Assertion.assert_equal(ParamCases.tc31result, True, "renew ipv6 address on pc2 failed")


# Expected: DHCP server act correctly when it get release message from Client
class TestTC32_Verify_release_ipv6_address(Test):
    uuid = "SOSAIOT-TC-56513"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_release_ipv6_address_on_pc2_eth1(self):
        releaseres = False
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        if ipv6addr:
            start_capture_and_clear_packets(packetmonitorapi)
            releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        else:
            logger.error('please make sure there PC2 has got an ipv6 address ')
        Assertion.assert_equal(releaseres, True, "ERR: Release dhcpv6 lease failed")

    def test_03_check_dhcpv6_packets_about_release(self):
        dhcpv6typeinlist = [
            'Message type: Release (8)',
            'Message type: Reply (7)'
        ]
        packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
        logger.info(f'packetres is {packetres}')
        Assertion.assert_equal(packetres, True, "ERR: check dhcpv6 packets about release failed")


# Expected: DHCPv6 Client Send Information-request message,the DHCP server will send Reply message
# (without IP address info, included requested configuration settings ).
class TestTC45_Verify_send_Information_request_message(Test):
    uuid = "SOSAIOT-TC-56515"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_disable_m_and_enable_o_on_x2(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True,
            'managed': False,
            'other_config': True,
            'router_adv': True
        }
        res = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 ipv6 address failed")

    # change dynamic dhcpv6 scope from dns inherit to static mode,test diversity.
    def test_03_edit_dhcpv6_server_lease_scope_with_manual_dns(self):
        dict_update = {
            "name": "scope",
            "range": {
                "from": "2001:1::100",
                "to": "2001:1::120"
            },
            "prefix": "2001:1::0",
            "dns": {
                "server": {
                    "static": {
                        "primary": Parameter.STATIC_PRIMARY_DNS,
                        "secondary": Parameter.STATIC_SECONDARY_DNS,
                        "tertiary": Parameter.STATIC_TERTIARY_DNS
                    }
                }
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.edit_dhcp_server_scope_v6('dynamic', 'scope', **dhcpv6_server_dynamic_scope_dict)
        Assertion.assert_equal(rc, True, "ERR: edit dhcpv6 dynamic scope failed")

    def test_04_send_information_request_on_pc2_eth1(self):
        start_capture_and_clear_packets(packetmonitorapi)
        output = send_information_request(PC2_Login, 'eth1')
        logger.info(f'send_information result:{output}')
        flag = True if 'Info-Request on eth1' in output and 'Reply message on eth1' in output else False
        Assertion.assert_equal(flag, True, "ERR: pc2 send information request and receive reply failed")

    def test_05_check_dns_details_and_ips_from_captured_packets_on_dut(self):
        flag = False
        # check dns info and ips in packets,and check if there is no IPv6 address in relay packets,
        # focus on "Identity Association for Non-temporary Address"
        dhcpv6typeinlist = [
            'Information-request (11)',
            ' Message type: Reply (7)',
            Parameter.STATIC_PRIMARY_DNS,
            Parameter.STATIC_SECONDARY_DNS,
            Parameter.STATIC_TERTIARY_DNS,
        ]
        dhcpv6typeoutlist = [
            'Identity Association for Non-temporary Address'
        ]
        (packetinres, packetoutres) = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist,
                                                           dhcpv6typeoutlist)
        logger.info(f'packetinres is:{packetinres},packetoutres is:{packetoutres}')
        if packetinres and packetoutres:
            flag = True
            logger.info('reply message without IP address info')
        Assertion.assert_equal(flag, True, "ERR: check dns and ips info failed")
        # Assertion.assert_equal(True, True, "ERR: check dns and ips info failed")

    def test_06_release_ipv6_address_on_pc2_eth1(self):
        res = release_dhcpv6_lease(PC2_Login, 'eth1')
        Assertion.assert_equal(res, True, "ERR: release ipv6 address on pc2 failed")


# Expected: Stateless DHCP server-Multiple Client in same interface, multiply client can get info
class TestTC46_Verify_stateless_with_multiple_client_in_same_interface(Test):
    uuid = "SOSAIOT-TC-56536"
    description = show_testcase_info(TESTPLAN, '46', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_send_information_request_on_pc2_eth1(self):
        TestTC45_Verify_send_Information_request_message().test_04_send_information_request_on_pc2_eth1()

    def test_03_check_dns_details_from_captured_packets_on_dut(self):
        TestTC45_Verify_send_Information_request_message().test_05_check_dns_details_and_ips_from_captured_packets_on_dut()

    def test_04_send_information_request_on_pc3_eth1(self):
        flag = False
        start_capture_and_clear_packets(packetmonitorapi)
        output = send_information_request(PC3_Login, 'eth1')
        logger.info(f'send_information result:{output}')
        if 'Info-Request on eth1' in output and 'Reply message on eth1' in output:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: pc2 send information request and receive replay failed")

    def test_05_check_dns_details_from_captured_packets_on_dut(self):
        TestTC45_Verify_send_Information_request_message().test_05_check_dns_details_and_ips_from_captured_packets_on_dut()


# Expected: Verify the exchange between stateless and stateful mode, the DHCPv6 server still work fine.
class TestTC51_Verify_exchange_between_stateless_and_stateful_mode(Test):
    uuid = "SOSAIOT-TC-56518"
    description = show_testcase_info(TESTPLAN, '51', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_to_stetefull_mode_m_is_1_and_o_is_1_for_x2(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True,
            'managed': True,
            'other_config': True,
            'router_adv': True
        }
        # there is no def edit_interface_ipv6,so use config
        rc = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: change M=0 and O=1 for X2 failed")

    def test_03_check_dhcpv6_packet_types_when_is_statefull_mode(self):
        packetres = False
        start_capture_and_clear_packets(packetmonitorapi)
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        if ipv6addr:
            dhcpv6typeinlist = {
                'Message type: Solicit (1)',
                'Message type: Advertise (2)',
                'Message type: Request (3)',
                'Message type: Reply (7)'
            }
            packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
            logger.info(f'check dhcpv6 result:{packetres}')
        else:
            logger.info("pc2 didn't get ipv6addr")

        # release ipv6addr:
        releaseres = release_dhcpv6_lease(PC2_Login, 'eth1')
        logger.info(f'releaseres is {releaseres}')
        Assertion.assert_equal(packetres, True, "ERR:check dhcpv6 packet types when is in statefull mode failed")

    def test_04_change_to_steteless_mode_m_is_0_and_o_is_1_for_x2(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True,
            'managed': True,
            'other_config': True,
            'router_adv': False
        }
        # there is no def edit_interface_ipv6,so use config
        rc = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: change M=0 and O=1 for X2 failed")

    def test_05_check_dhcpv6_packet_type_when_is_stateless_mode(self):
        start_capture_and_clear_packets(packetmonitorapi)
        output = send_information_request(PC2_Login, 'eth1')
        logger.info(f'send_information result:{output}')
        dhcpv6typeinlist = {
            'Information-request (11)',
            ' Message type: Reply (7)',
        }
        packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
        logger.info(f'packetres is {packetres}')
        Assertion.assert_equal(packetres, True, "ERR:check dhcpv6 packet types when stateless mode failed")

    def test_06_change_to_statefull_mode_and_repeat_statefull_test(self):
        self.test_02_change_to_stetefull_mode_m_is_1_and_o_is_1_for_x2()

    def test_07_change_to_statefull_mode_and_repeat_statefull_test(self):
        self.test_03_check_dhcpv6_packet_types_when_is_statefull_mode()


# Expected: Restarted the firewall ,all configuration of DHCPv6 server saved.
class TestTC58_Restart_dut(Test):
    uuid = "SOSAIOT-TC-56538"
    description = show_testcase_info(TESTPLAN, '58', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_static_dhcpv6_scope(self):
        res = dhcpserverapi.add_dhcp_server_scope_static(**dhcpv6_server_static_scope_dict)
        Assertion.assert_equal(res, True, "ERR: add static dhcpv6 scope failed")

    def test_03_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_04_check_dhcpv6_scopes(self):
        tag = []
        dynamicres = dhcpserverapi.get_dhcp_server_scope_dynamic(version=6)
        staticres = dhcpserverapi.get_dhcp_server_scope_static(version=6)
        logger.info(f'dynamic dhcpv6 scopes are {json.dumps(dynamicres)}')
        logger.info(f'static dhcpv6 scopes are {json.dumps(dynamicres)}')
        if '"name": "x3_scope"' in json.dumps(dynamicres) and '"name": "scope"' in json.dumps(dynamicres):
            tag.append(True)
        else:
            tag.append(False)
        if f'"name": "static_dhcpv6_scope"' in json.dumps(staticres):
            tag.append(True)
        else:
            tag.append(False)
        logger.info(f'tag is :{tag}')
        Assertion.assert_equal(all(tag), True, "ERR: check dhcpv6 configuration failed")


# Expected: Mix stateless and stateful,X2 stateless,X3 statefull
class TestTC52_Verify_mix_stateless_and_stateful(Test):
    uuid = "SOSAIOT-TC-56537"
    description = show_testcase_info(TESTPLAN, '52', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_send_information_request_on_pc2_eth1_stateless(self):
        # TestTC45_Verify_send_Information_request_message().test_04_send_information_request_on_pc2_eth1
        TestTC45_Verify_send_Information_request_message().test_04_send_information_request_on_pc2_eth1()

    def test_03_check_dns_details_from_captured_packets_on_dut_stateless(self):
        # TestTC45_Verify_send_Information_request_message().test_05_check_dns_details_and_ips_from_captured_packets_on_dut
        TestTC45_Verify_send_Information_request_message().test_05_check_dns_details_and_ips_from_captured_packets_on_dut()

    def test_04_config_packet_monitor_filter_x3(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x3',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    # def test_05_get_ipv6_address_from_dhcpv6_server_on_remote_dut_x3(self):
    #     flag = False
    #     x3_v6_dict_static = {
    #         'name': 'X3',
    #         'mode': 'static',
    #         'zone': 'WAN',
    #         'ip': '',
    #         'prefix_length': 64
    #     }
    #     x3_v6_dict_dhcpv6 = {
    #         'name': 'X3',
    #         'mode': 'dhcpv6',
    #     }
    #     # change from static mode to dhcpv6 mode
    #     rc1 = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_static)
    #     rc2 = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_dhcpv6)
    #     logger.info(f'rc1 is:{rc1},rc2 is:{rc2}')
    #     clickrelease = reinterfacev4api.click_dhcp_release('x3', version='v6')
    #     logger.info(clickrelease)
    #     clickrenew = reinterfacev4api.click_dhcp_renew('x3', version='v6')
    #     if clickrenew:
    #         time.sleep(10)
    #         ipv6res = get_dhcpv6_leases_on_remote_dut(reinterfacecli, 'X3', 'ipv6')
    #         logger.info(f'ipv6 address on remote dut is {ipv6res}')
    #         flag = True if ipv6res else False
    #     Assertion.assert_equal(flag, True, "ERR: add dhcpv6 dynamic scope failed")

    def test_05_get_ipv6_address_from_dhcpv6_server_on_pc5(self):
        ipv6addr = get_dhcpv6_leases(PC5_Login, 'eth1')
        flag = True if ipv6addr else False
        Assertion.assert_equal(flag, True, "ERR: get ipv6 address from remote dut x3 failed ")

    def test_06_config_packet_monitor_filter_back_to_x2(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x2',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")


# Expected:  Message Validation <Client in DMZ zone, verify basic IP info>.
class TestTC22_Message_validation_in_dmz_zone(Test):
    uuid = "SOSAIOT-TC-56525"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_X2_to_DMZ_zone(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.config_interface(**x2_v4_dict)
        Assertion.assert_equal(res, True, "ERR: change X2 from LAN zone to DMZ zone failed")

    def test_03_check_dhcpv6_packet_types(self):
        flag = False
        start_capture_and_clear_packets(packetmonitorapi)
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        if ipv6addr:
            dhcpv6typeinlist = [
                'Message type: Solicit (1)',
                'Message type: Advertise (2)',
                'Message type: Request (3)',
                'Message type: Reply (7)',
                f'IPv6 address: {ipv6addr}'
            ]
            packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
            logger.info(f'packetres is {packetres}')
            flag = True
        Assertion.assert_equal(flag, True, "ERR:check dhcpv6 packet types when statefull mode failed")


# Expected:  Message Validation < Client in Custom zone, verify basic IP info>
class TestTC23_Message_validation_in_custom_zone(Test):
    uuid = "SOSAIOT-TC-56526"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_creat_custom_zone(self):
        custom_zone_dict = {
            "zones": [
                {
                    "name": "custom_zone",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        res = zoneobjectsapi.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(res, True, "ERR:add custom zone failed")

    def test_03_set_x2_from_dmz_to_custom_zone(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'custom_zone',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.config_interface(**x2_v4_dict)
        Assertion.assert_equal(res, True, "ERR: change X2 from LAN zone to DMZ zone failed")

    def test_04_check_dhcpv6_packet_types(self):
        TestTC22_Message_validation_in_dmz_zone().test_03_check_dhcpv6_packet_types()


# Expected:  Message Validation< Client gets Domain Name Info with Dynamic lease>
class TestTC24_Message_validation_with_domain_name_info(Test):
    uuid = "SOSAIOT-TC-56527"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_dhcpv6_packet_types(self):
        start_capture_and_clear_packets(packetmonitorapi)
        ipv6addr = get_dhcpv6_leases(PC2_Login, 'eth1')
        logger.info(f'get ipv6 address is :{ipv6addr}')
        if ipv6addr:
            dhcpv6typeinlist = [
                'Message type: Solicit (1)',
                'Message type: Advertise (2)',
                'Message type: Request (3)',
                'Message type: Reply (7)',
                f'IPv6 address: {ipv6addr}',
                'Domain: autotest',
                'Preferred lifetime: 86400',  # 1440 * 60
                'Valid lifetime: 129600',  # 2160 * 60
                Parameter.STATIC_PRIMARY_DNS,
                Parameter.STATIC_SECONDARY_DNS,
                Parameter.STATIC_TERTIARY_DNS
            ]
            packetres = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6typeinlist)
            logger.info(f'packetres is {packetres}')
            ParamCases.tc24result = packetres
        Assertion.assert_equal(packetres, True, "ERR:check Domain Name Info in dhcpv6 packets failed")


# Expected:  Message Validation< Client gets DNS Name Info with Dynamic lease >
class TestTC25_Message_validation_with_dns_name(Test):
    uuid = "SOSAIOT-TC-56528"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_dhcpv6_packet_types(self):
        logger.info(f'get result:{ParamCases.tc24result} from case TC24 since it has run this case')
        Assertion.assert_equal(ParamCases.tc24result, True, "ERR:check DNS Name Info in dhcpv6 packets failed")


# Expected:  Message Validation< Client gets Valid Lifetime Info with Dynamic lease>
class TestTC26_Message_validation_with_valid_lifetime_info(Test):
    uuid = "SOSAIOT-TC-56529"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_dhcpv6_packet_types(self):
        logger.info(f'get result:{ParamCases.tc24result} from case TC24 since it has run this case')
        Assertion.assert_equal(ParamCases.tc24result, True, "ERR:check Valid Lifetime Info in dhcpv6 packets failed")



# Expected:  Message Validation< Client gets Preferred Lifetime Info with Dynamic lease >
class TestTC27_Message_validation_with_preferred_lifetime_info(Test):
    uuid = "SOSAIOT-TC-56530"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_dhcpv6_packet_types(self):
        logger.info(f'get result:{ParamCases.tc24result} from case TC24 since it has run this case')
        Assertion.assert_equal(ParamCases.tc24result, True, "ERR:check Preferred Lifetime Info in dhcpv6 failed")


# Expected:Stateless DHCP server-DHCP server deployment with different Relay agent
class TestTC50_Stateless_dhcpv6_server_works_fine_with_relay_agent(Test):
    uuid = "SOSAIOT-TC-56517"
    description = show_testcase_info(TESTPLAN, '50', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_x3_to_static_mode_with_lan_zone(self):
        x3_v6_dict_static = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_REMOTE_V6_IP,
            'prefix_length': 64
        }
        rc = reinterfacev6api.config_interface_ipv6(**x3_v6_dict_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static mode failed")

    def test_03_enable_ip_helper_on_remote_dut(self):
        res = reiphelperapi.enable_iphelper()
        Assertion.assert_equal(res, True, "ERR: enable ip helper on remote dut failed")

    def test_04_enable_dhcp_relay_protocol_on_remote_dut(self):
        dhcpv6_dict = {
            'enable': True
        }
        res = reiphelperapi.edit_protocol(name='DHCPv6', **dhcpv6_dict)
        Assertion.assert_equal(res, True, 'ERR: enable dhcpv6 relay protocol failed')

    def test_05_add_ip_helper_policy_on_remote_dut(self):
        policy_dict = {
            "ip_helper": {
                "policy": [
                    {
                        "egressif": "X3",
                        "protocol": "DHCPv6",
                        "source": {
                            "interface": "X4"
                        },
                        "destination": {
                            "ipv6": Parameter.X3_V6_IP
                        },
                        "enable": True,
                        "comment": ""
                    }
                ]
            }
        }
        rc = reiphelperapi.add_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')


    def test_06_add_dhcpv6_dynamic_scope_for_remote_x4_on_local_dut(self):
        dict_update = {
            "name": "relay_scope",
            "range": {
                "from": "4001:1::101",
                "to": "4001:1::110"
            },
            "prefix": "4001:1::0",
            "dns": {
                "server": {
                    "static": {
                        "primary": Parameter.STATIC_PRIMARY_DNS,
                        "secondary": Parameter.STATIC_SECONDARY_DNS,
                        "tertiary": Parameter.STATIC_TERTIARY_DNS
                    }
                }
            }
        }
        dhcpv6_server_dynamic_base_dict.update(dict_update)
        rc = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcpv6_server_dynamic_scope_dict)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add dhcpv6 dynamic scope for remote x4 failed")

    def test_07_add_network_ao_and_host_ao_on_local_dut(self):
        gateway_ao = {
            "object_type": "host",
            "name": 'gw_remote_x3',
            "zone": 'LAN',
            "ip": Parameter.X3_REMOTE_V6_IP
        }
        client_ao = {
            'name': 'client_ao',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '4001:1::0',
            'mask': '/64',
        }
        rc1 = addressobjectsapi.config_ipv6_addressobject(**gateway_ao)
        rc2 = addressobjectsapi.config_ipv6_addressobject(**client_ao)
        logger.info(f'rc1:{rc1},rc2:{rc2}')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: configure AOs failed")

    def test_08_add_ipv6_route_policy_on_local_dut(self):
        dict_update = {
            "name": "to_client",
            "interface": "X3",
            "destination": {"name": "client_ao"},
            "gateway": {"name": "gw_remote_x3"}
        }
        ipv6_route_base_dict.update(dict_update)
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy failed")

    def test_09_config_packet_monitor_filter_to_x3(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x3',
                'ether_types': 'ipv6',
                'ip_types': 'udp',
                'destination_ports': '546,547',
            }
        }
        output = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(output, True, "ERR: Config packet monitor failed")

    def test_10_send_information_request_on_pc4_eth1(self):
        start_capture_and_clear_packets(packetmonitorapi)
        output = send_information_request(PC4_Login, 'eth1')
        logger.info(f'send_information result:{output}')
        flag = True if 'Info-Request on eth1' in output and 'Reply message on eth1' in output else False
        if not flag:
            leaselist = dhcpserverapi.get_dhcp_server_leases(version=6)
            logger.info(f'current dhcpv6 dynamic scopes: {leaselist}')
        Assertion.assert_equal(flag, True, "ERR: pc4 send information request and receive reply failed")

    def test_11_check_dns_details_and_ips_from_captured_packets_on_dut(self):
        flag = False
        dhcpv6inlist = [
            'Information-request (11)',
            ' Message type: Reply (7)',
            Parameter.STATIC_PRIMARY_DNS,
            Parameter.STATIC_SECONDARY_DNS,
            Parameter.STATIC_TERTIARY_DNS,
        ]
        dhcpv6outlist = [
            'Identity Association for Non-temporary Address'
        ]
        (packetinres, packetoutres) = check_dhcpv6_packets(packetmonitorapi, PC1_Login, dhcpv6inlist, dhcpv6outlist)
        logger.info(f'packetintres is:{packetinres},packetoutres is:{packetoutres}')
        if packetinres and packetoutres:
            flag = True
            logger.info('reply message without IP address info')
        Assertion.assert_equal(flag, True, "ERR: check dns and ips info failed")

    def test_12_release_ipv6_address_on_pc2_eth1(self):
        res = release_dhcpv6_lease(PC4_Login, 'eth1')
        Assertion.assert_equal(res, True, "ERR: release ipv6 address on pc2 failed")
