from definition.settings import *

class TC01_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75187"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519584')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")
        
class TC02_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75188"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519585')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_auth_partition(self):
        auth_partition1 = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        auth_partition2 = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test2",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-automationsnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res1 = user_auth_partition.add_auth_partition(**auth_partition1)
        res2 = user_auth_partition.add_auth_partition(**auth_partition2)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        Assertion.assert_equal(res2, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")
        Assertion.assert_regular(json.dumps(resp), '"name": "test2"', "ERR: Failed to add partition")


class TC03_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75189"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519586')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_sub_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                "partition": [
                    {
                    "name": "subpart_test1",
                    "parent_partition": "test1",
                    "comment": "",
                    "domain": []
                    }
                ]
                }
            }
            }
        res1 = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "subpart_test1"', "ERR: Failed to add partition")
        

class TC04_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75190"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519587')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_01_edit_auth_partition(self):
        auth_partition = {
        "user": {
            "partitioning": {
            "partition": [
                {
                "name": "test1",
                "parent_partition": "",
                "comment": "",
                "domain": [
                    
                ]
                }
            ]
            }
        }
        }
        res1 = user_auth_partition.edit_auth_partition(name="test1", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
    
    def test_02_edit_auth_sub_partition(self):
        auth_partition = {
        "user": {
        "partitioning": {
            "partition": [
            {
                "name": "subpart_test1",
                "parent_partition": "test1",
                "comment": "",
                "domain": [
                {
                    "name": "os-autosnwlpart1.com"
                }
                ]
            }
            ]
        }
        }
        }
        res1 = user_auth_partition.edit_auth_partition(name="subpart_test1", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwlpart1.com"', "ERR: Failed to add partition")
        
class TC05_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75191"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519588')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_primary_ldap_with_partition(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.85',
                        "enable": True,
                        "role": {
                            "primary": True
                        },
                        "port": 389,
                        "partition": "test1",
                        "timeout": {
                            "server": 10,
                            "operation": 5
                        },
                        "use_tls": False,
                        "schema": "microsoft-active-directory",
                        "user_class": "user",
                        "user_attribute": {
                            "logon_name": "sAMAccountName",
                            "qualified_logon_name": "userPrincipalName",
                            "group_membership": "memberOf",
                            "additional_group_id": "primaryGroupID",
                            "use_additional_group_id": False,
                            "framed_ip_address": "msRADIUSFramedIPAddress"
                        },
                        "user_group_class": "group",
                        "user_group_attribute": {
                            "member": {
                                "type": "distinguished-name",
                                "name": "member"
                            },
                            "additional_group_match": "primaryGroupToken"
                        },
                        "directory": {
                            "primary_domain": "os-autosnwl.com",
                            "users_tree": [{
                                "name": "os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
    
    def test_02_edit_auth_partition(self):
        add_ldap_server = {
            'role': 'primary',
            'host': '192.168.168.85',
            'partition': "test2"
        }

        user_ldap.edit_ldap_server(**add_ldap_server)
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to use ip as host")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test2"',
                                 "ERR: Failed to config the ldap server")

class TC06_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75192"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519589')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")
        
class TC07_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75193"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519590')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

class TC08_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75194"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519591')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_primary_ldap_with_partition(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.85',
                        "enable": True,
                        "role": {
                            "primary": True
                        },
                        "port": 389,
                        "partition": "test1",
                        "timeout": {
                            "server": 10,
                            "operation": 5
                        },
                        "use_tls": False,
                        "schema": "microsoft-active-directory",
                        "user_class": "user",
                        "user_attribute": {
                            "logon_name": "sAMAccountName",
                            "qualified_logon_name": "userPrincipalName",
                            "group_membership": "memberOf",
                            "additional_group_id": "primaryGroupID",
                            "use_additional_group_id": False,
                            "framed_ip_address": "msRADIUSFramedIPAddress"
                        },
                        "user_group_class": "group",
                        "user_group_attribute": {
                            "member": {
                                "type": "distinguished-name",
                                "name": "member"
                            },
                            "additional_group_match": "primaryGroupToken"
                        },
                        "directory": {
                            "primary_domain": "os-autosnwl.com",
                            "users_tree": [{
                                "name": "os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_sub_partition(self):
        resp = user_auth_partition.del_auth_partition("subpart_test1")
        show_resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_not_regular(json.dumps(show_resp), '"name": "subpart_test1"', "ERR: Failed to add partition")

    def test_03_delete_sub_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        show_resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_not_regular(json.dumps(show_resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_04_edit_auth_partition(self):
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to use ip as host")
        Assertion.assert_not_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")
        
class TC09_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75195"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519592')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_default_partition(self):
        resp = user_auth_partition.del_auth_partition("Default")
        show_resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(show_resp), '"name": "Default"', "ERR: Failed to add partition")

class TC10_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75196"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519593')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_auth_partition(self):
        auth_partition1 = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test3",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl3.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res1 = user_auth_partition.add_auth_partition(**auth_partition1)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test3"', "ERR: Failed to add partition")

    
    def test_02_add_sub_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                "partition": [
                    {
                    "name": "subpart_test2",
                    "parent_partition": "test3",
                    "comment": "",
                    "domain": []
                    }
                ]
                }
            }
            }
        res1 = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "subpart_test2"', "ERR: Failed to add partition")
    
class TC11_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75197"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519594')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test3",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }

        res1 = user_auth_partition.edit_auth_partition(name="test3", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test3"', "ERR: Failed to add partition")


class TC12_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75198"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519595')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_auth_partition(self):
        auth_partition1 = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test5",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl3.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res1 = user_auth_partition.add_auth_partition(**auth_partition1)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test5"', "ERR: Failed to add partition")

    def test_02_delete_default_partition(self):
        resp1 = user_auth_partition.del_auth_partition("test5")
        logger.info(resp1)
        resp2 = user_auth_partition.del_auth_partition("Default")
        show_resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(show_resp), '"name": "Default"', "ERR: Failed to add partition")
        Assertion.assert_not_regular(json.dumps(show_resp), '"name": "test5"', "ERR: Failed to add partition")

class TC13_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75199"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2706660')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

class TC14_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75201"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2772776')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        policies = {
        "user": {
            "partitioning": {
            "policy": [
                {
                "interface": "any",
                "zone": "VPN",
                "address_object": "any",
                "partition": "Default",
                "priority": 1,
                "comment": ""
                }
            ]
            }
        }
        }
        ldap_user = user_auth_partition.add_auth_partition_policies(**policies)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

class TC15_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75202"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2772777')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test4",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res1 = user_auth_partition.add_auth_partition(name="test4", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test4"', "ERR: Failed to add partition")
    
    def test_02_edit_auth_partition(self):
        add_ldap_server = {
            'role': 'primary',
            'host': '192.168.168.85',
            'partition': "test4"
        }

        user_ldap.edit_ldap_server(**add_ldap_server)
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to use ip as host")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test4"',
                                 "ERR: Failed to config the ldap server")

    def test_03_edit_auth_partition(self):
        add_ldap_server = {
            'role': 'primary',
            'host': '192.168.168.85',
            'partition': "test2"
        }

        user_ldap.edit_ldap_server(**add_ldap_server)
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to use ip as host")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test2"',
                                 "ERR: Failed to config the ldap server")
        
class TC16_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75200"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2723402')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user(self):
        user_json = {

            'action': 'add',
            'username': 'test_user',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'SSLVPN Services', "SonicWALL Administrators"],
            'vpn_client_access': ['LAN Subnets']
        }
        resp = local_user.local_user(**user_json)
        resp1 = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "test_user"', 'err: sslvpntest not created')

    def test_02_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group3'
        }
        post_resp = local_user.local_group(**group_json)
        get_resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "group3"', 'err: group2 not created')
    
    def test_03_local_user_scan_and_enter_totp(self):
        scanner_page = True
        local_host.send_command('pkill firefox')
        time.sleep(5)
        url = "https://192.168.168.168"
        cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/Auth_Partitions_GUI/definition/ui_user.py -url {url} -user admin -pwd sonicauto'
        out = local_host.send_command(cmd)
        logger.info("login with user\nRESPONSE: \n" + out)
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Unable to show auth partiotions")
       
    def test_04_edit_auth_partition(self):
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test4"', "ERR: Failed to add partition")

    def test_05_local_users(self):
        res1 = localusers.show_local_users()
        get_resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "group3"', 'err: group2 not created')
        Assertion.assert_regular(json.dumps(res1), '"name": "test_user"', "ERR: Failed to add partition")

class TC17_Auth_Partition(Test): 
    uuid = "SOSAIOT-TC-75204"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3214485')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_show_tsr(self):
        commands = ["show tech-support-report user-authentication-partitioning"]
        response, output = fw_cli.do_cli_commands(commands=commands, tag=1)
        Assertion.assert_equal(response, True, "ERR: default blocked page is failed in cli")

class TC18_Auth_Partition(Test):
    uuid = "SOSAIOT-TC-75203"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3100649')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_import_ldap_user(self):
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
        resp = local_user.import_local_usr_from_ldap(**add)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
        
    def test_02_local_user_scan_and_enter_totp(self):
        scanner_page = True
        local_host.send_command('pkill firefox')
        time.sleep(5)
        url = "https://192.168.168.168"
        cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/Auth_Partitions_GUI/definition/ui_user.py -url {url} -user test -pwd sonicauto'
        out = local_host.send_command(cmd)
        logger.info("login with user\nRESPONSE: \n" + out)
        time.sleep(10)
        Assertion.assert_equal(out, True, "ERR: Unable to show auth partiotions")

    def test_03_local_users(self):
        res1 = localusers.show_local_users()
        get_resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(get_resp), '"name": "group3"', 'err: group2 not created')
        Assertion.assert_regular(json.dumps(res1), '"name": "test_user"', "ERR: Failed to add partition")
