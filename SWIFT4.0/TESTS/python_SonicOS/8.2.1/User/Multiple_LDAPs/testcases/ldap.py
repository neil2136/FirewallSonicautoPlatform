import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Multiple_LDAPs')

from definition.settings import *


# TC01 Add primary LDAP server when AP is not enabled
class TC001_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75076"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1529214")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_credential_auditor_disable_api(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": False,  
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_setting.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,', "failed to disable toggle button")

    def test_02_add_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC02 Add the second primary LDAP server when AP is not enabled
class TC002_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75077"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529215')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_credential_auditor_disable_api(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": False,  
                        "block_user_login_with_external_auth": False
                    }
                }
            }
        }
        resp = user_setting.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"block_user_login_with_external_auth": false,', "failed to disable toggle button")

    def test_02_add_ldap1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_ldap2(self):
        ldap_server2_primary = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "primary": True
                        },
                        "port": 389,
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2_primary)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"primary": true',
                                 "ERR: Failed to config the ldap server")

    def test_04_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_05_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC03 Add secondary LDAP server when AP is not enabled
class TC003_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75078"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529216')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_ldap2(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_04_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC04 Add two or more Backup/replica LDAP servers for the primary server when AP is not enabled
class TC004_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75079"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529217')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_ldap2(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_04_add_backup_server2(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.110",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.110")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.110"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_backup_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.110")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC05 Add Backup/replica LDAP server  with using same bind credentials as server backup for
class TC005_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75082"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529220')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_04_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_05_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC06 Add multiple LDAP Servers with TLS and Non-TLS mixture
class TC006_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75085"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529223')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_nontls(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"use_tls": false',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_ldap_with_tls(self):
        ldap_server2_primary = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
                        },
                        "port": 389,
                        "timeout": {
                            "server": 10,
                            "operation": 5
                        },
                        "use_tls": True,
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2_primary)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"use_tls": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_04_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC07 Delete the LDAP server
class TC007_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75089"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529227')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_03_verify_deleted_ldap_server(self):
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"code": "E_NO_MATCH"',
                                 "ERR: Failed to config the ldap server")


# TC08 Edit the LDAP server
class TC008_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75088"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529226')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': True,
            'port_num': 6365,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 20,
            'overalloperationtimeout': 10,
        }

        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

    def test_03_verify_updated_ldap_server(self):
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"use_tls": true',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"port": 6365',
                                 "ERR: Failed to config the ldap server")

    def test_04_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC09 LDAP Configuration> Directory. DNs for user trees. Add
class TC009_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75103"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825339')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                            },
                                {
                                    "name": "testqa.com/unit1"
                                }
                            ],
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
        print(f"LDAP resp ----> {resp}")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"name": "testqa.com/unit1"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC10 LDAP Configuration> Directory. DNs for user trees. Edit
class TC010_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75104"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825340')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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

    def test_02_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': True,
            "directory": True,
            "users_tree": {"os-autosnwl2.com/Users"}
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl2.com/Users"',
                                 "ERR: Failed to config the ldap server")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC11 LDAP Configuration> Directory. DNs for user trees. Remove
class TC011_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75105"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825341')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                            "users_tree": [],
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
        Assertion.assert_not_regular(json.dumps(resp), '"users_tree": "os-autosnwl.com/Users"',
                                     "ERR: Failed to config the ldap server")

    def test_02_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC12 LDAP Configuration> Directory. DNs for user trees. Limits
class TC012_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75106"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825342')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                                "name": "os-autosnwl1.com/Users"
                            }, {
                                "name": "os-autosnwl2.com/Users"
                            }, {
                                "name": "os-autosnwl3.com/Users"
                            }, {
                                "name": "os-autosnwl4.com/Users"
                            }, {
                                "name": "os-autosnwl5.com/Users"
                            }, {
                                "name": "os-autosnwl6.com/Users"
                            }, {
                                "name": "os-autosnwl7.com/Users"
                            }, {
                                "name": "os-autosnwl8.com/Users"
                            }, {
                                "name": "os-autosnwl9.com/Users"
                            }, {
                                "name": "os-autosnwl10.com/Users"
                            }, {
                                "name": "os-autosnwl11.com/Users"
                            }, {
                                "name": "os-autosnwl12.com/Users"
                            }, {
                                "name": "os-autosnwl13.com/Users"
                            }, {
                                "name": "os-autosnwl14.com/Users"
                            }, {
                                "name": "os-autosnwl15.com/Users"
                            }, {
                                "name": "os-autosnwl16.com/Users"
                            }
                            ],
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
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl1.com/Users"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl10.com/Users"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl16.com/Users"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC13 LDAP Configuration> Directory. The format for trees
class TC013_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75107"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825343')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "test",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to configure")

    def test_03_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': True,
            "directory": True,
            "users_tree": {"ou=Users,dc=os-autosnwl,dc=com"}
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"name": "ou=Users,dc=os-autosnwl,dc=com"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_04_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "test",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        print(f"LDAP user auth test {resp}")
        Assertion.assert_equal(resp, True, "failed to configure")

    def test_05_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC14 LDAP Configuration> Directory. DNs for user group trees. Add
class TC014_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75108"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825344')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                            },
                                {
                                    "name": "testqa.com/unit1"
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
        Assertion.assert_regular(json.dumps(resp), '"name": "testqa.com/unit1"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC15 LDAP Configuration> Directory. DNs for user group trees. Edit
class TC015_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75109"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825345')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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

    def test_02_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': True,
            "directory": True,
            "user_groups_tree": {"os-autosnwl2.com/Users"}
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl2.com/Users"',
                                 "ERR: Failed to config the ldap server")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC16 LDAP Configuration> Directory. DNs for user group trees. Remove
class TC016_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75110"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825346')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                                "name": "os-autosnwl-group.com/Users"
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

    def test_02_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': True,
            "directory": {
                "primary_domain": "os-autosnwl.com",
                "users_tree": [{
                    "name": ""
                }],
                "user_groups_tree": [{
                    "name": ""
                }]
            }
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_not_regular(json.dumps(resp), '"name": "os-autosnwl-group.com/Users"',
                                     "ERR: Failed to config the ldap server")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC17 LDAP Configuration> Directory. DNs for user group trees. Limits
class TC017_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75111"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825347')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap(self):
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
                                "name": "os-autosnwl.com/Users",
                            }
                            ],
                            "user_groups_tree": [{
                                "name": "os-autosnwl1.com/Users"
                            }, {
                                "name": "os-autosnwl2.com/Users"
                            }, {
                                "name": "os-autosnwl3.com/Users"
                            }, {
                                "name": "os-autosnwl4.com/Users"
                            }, {
                                "name": "os-autosnwl5.com/Users"
                            }, {
                                "name": "os-autosnwl6.com/Users"
                            }, {
                                "name": "os-autosnwl7.com/Users"
                            }, {
                                "name": "os-autosnwl8.com/Users"
                            }, {
                                "name": "os-autosnwl9.com/Users"
                            }, {
                                "name": "os-autosnwl10.com/Users"
                            }, {
                                "name": "os-autosnwl11.com/Users"
                            }, {
                                "name": "os-autosnwl12.com/Users"
                            }, {
                                "name": "os-autosnwl13.com/Users"
                            }, {
                                "name": "os-autosnwl14.com/Users"
                            }, {
                                "name": "os-autosnwl15.com/Users"
                            }, {
                                "name": "os-autosnwl16.com/Users"
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
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl1.com/Users"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl10.com/Users"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwl16.com/Users"',
                                 "ERR: Failed to config the ldap server")

    def test_02_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC18 LDAP Configuration> LDAP Users. Allow only users listed locally
class TC018_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75112"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825348')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_toggle_allow_only_users_listed_locally(self):
        response = ui_obj.verify_toggle_allow_only_users_listed_locally()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC19 LDAP Configuration> LDAP Users. Default LDAP User Group. Select
class TC019_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75114"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825350')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_drop_down_default_ldap_user_group(self):
        response = ui_obj.verify_drop_down_default_ldap_user_group()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC20 Check LDAP window can be closed without saving
class TC020_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75093"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825324')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_ldap_window_can_be_closed_without_saving(self):
        response = ui_obj.verify_ldap_window_can_be_closed_without_saving()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC21 Invalid  Refresh period for LDAP Mirror
class TC021_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75094"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825325')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_ldap_settings(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "mirror_user_groups": {
                        "refresh": {
                            "period": 0
                        }
                    }
                }
            }
        }

        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, False, "ERR: Failed")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_not_regular(json.dumps(resp), '"period": 0', "failed to set refresh period")


# TC22 mirror setting not allowed when uncheck 'Mirror LDAP user groups locally'
class TC022_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75095"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825327')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_disabled_mirror_ldap_user_group_locally(self):
        response = ui_obj.verify_disabled_mirror_ldap_user_group_locally()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC23 Enable checkbox work for LDAP Server
class TC023_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75096"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825328")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"enable": True', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_03_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': False,
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"enable": False', "ERR: Failed to enable ldap server")
        time.sleep(3)

    def test_04_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, False, "failed to test ldap")

    def test_05_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC24 TLS' checkbox work for LDAP Server
class TC024_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75097"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825329")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")

    def test_02_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'port_num': 636,
            'use_tls': True,
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"enable": true', "ERR: Failed to enable ldap server")
        Assertion.assert_regular(json.dumps(resp), '"use_tls": true',
                                 "ERR: Failed to config the ldap server")

    @repeat_method(3)
    def test_03_verify_tls_checkbox(self):
        response = ui_obj.verify_tls_checkbox()
        Assertion.assert_equal(response, True, "ERR: Failed")

    def test_04_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC25 LDAP Configuration> Schema. LDAP Schema list
class TC025_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75098"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825334')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_drop_down_values_for_ldap_schema(self):
        response = ui_obj.verify_drop_down_values_for_ldap_schema()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC26 LDAP Configuration> Directory. Primary domain field
class TC026_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75102"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825338')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_drop_down_values_for_ldap_schema(self):
        response = ui_obj.verify_drop_down_values_for_ldap_schema()
        Assertion.assert_equal(response, True, "ERR: Failed")


# TC27 LDAP Configuration> LDAP Users. Default LDAP User Group. Create a new user group
class TC027_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75115"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825351")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_local_user_group(self):
        local_group = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "test",
                            "domain": "test.com"
                        }
                    ]
                }
            }
        }
        ldap_user = local_user.add_local_group(**local_group)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add local user group")

        resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "test"', "ERR: Failed to configure local group")

    @repeat_method(3)
    def test_02_verify_default_local_user_group(self):
        response = ui_obj.verify_default_local_user_group()
        Assertion.assert_equal(response, True, "ERR: Failed")

    def test_03_delete_local_group(self):
        resp = local_user.delete_local_group_with_domain(groupname="test", domainname="test.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete local group")


# TC28 Add two or more secondary LDAP servers when AP is not enabled
class TC028_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75116"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825352')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_secondary_ldap1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_secondary_ldap2(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.87',
                        "enable": True,
                        "role": {
                            "secondary": True
                        },
                        "port": 389,
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
                            "primary_domain": "wsv3.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv3.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv3.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv3.os-autosnwl.com/Users"
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

        resp = user_ldap.show_ldap_server_by_name("192.168.168.87")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.87"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_04_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_05_delete_secondary_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_secondary_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.87")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC29 Add two or more Backup/replica LDAP servers for one or more secondary server when AP is not enabled
class TC029_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75117"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825353')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_secondary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.87",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.86",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.87")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.87"',
                                 "ERR: Failed to config the ldap server")

    def test_04_add_backup_server2(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.88",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.86",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.88")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.88"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.87")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_backup_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.88")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")




# TC30 Add the same Backup/replica LDAP server for multiple LDAP servers
class TC030_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75118"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825354')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_add_secondary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")

    def test_03_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.87",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.87")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.87"',
                                 "ERR: Failed to config the ldap server")


    def test_04_add_backup_server2(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.87",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.86",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(msg=True, **backup_server)
        Assertion.assert_regular(json.dumps(ldap_user), '"success": false',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(ldap_user), 'already exists.',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.87")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC31 Add primary LDAP server when AP is enabled
class TC031_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75119"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825355')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_04_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_05_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC32 Add secondary LDAP server when AP is enabled
class TC032_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75120"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825356')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_secondary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC33 Add Backup/replica LDAP server  with using different bind credentials from server backup for
class TC033_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75121"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825357')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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

    def test_04_add_backup_server(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": False
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_backup_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC34 Add Backup/replica LDAP server  in the same partition
class TC034_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75122"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825358')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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

    def test_04_add_backup_server(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_backup_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC35 Add two or more Backup/replica LDAP servers for one or more secondary server in the same partition
class TC035_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75123"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825359')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.86",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_06_add_backup_server2(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.110",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.86",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.110")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.110"',
                                 "ERR: Failed to config the ldap server")

    def test_07_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_backup_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.110")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_10_delete_secondary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_11_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC36 Add a primary LDAP server separately in multiple partitions
class TC036_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75124"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825360')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition1(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_auth_partition2(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test2",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [
                            ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test2"', "ERR: Failed to add partition")

    def test_04_add_primary_ldap(self):
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_change_partition_ldap(self):
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

    def test_06_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition1(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

    def test_08_delete_auth_partition2(self):
        resp = user_auth_partition.del_auth_partition("test2")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC37 Add a secondary LDAP server separately in multiple partitions
class TC037_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75125"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825361')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition1(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_auth_partition2(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test2",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [
                            ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test2"', "ERR: Failed to add partition")

    def test_04_add_primary_ldap(self):
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_06_change_partition_ldap(self):
        add_ldap_server = {
            'role': 'secondary',
            'host': '192.168.168.86',
            'partition': "test2"
        }

        user_ldap.edit_ldap_server(**add_ldap_server)
        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"', "failed to use ip as host")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test2"',
                                 "ERR: Failed to config the ldap server")

    def test_07_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_secondary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition1(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

    def test_10_delete_auth_partition2(self):
        resp = user_auth_partition.del_auth_partition("test2")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC38 Add a Backup/replica LDAP server separately in multiple partitions
class TC038_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75126"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825362')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition1(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_auth_partition2(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test2",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [
                            ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test2"', "ERR: Failed to add partition")

    def test_04_add_primary_ldap(self):
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

    def test_05_add_backup_server(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_06_change_partition_ldap(self):
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

    def test_07_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_backup_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition1(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

    def test_10_delete_auth_partition2(self):
        resp = user_auth_partition.del_auth_partition("test2")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC39 Test LDAP server with wrong User/Password_user authentication test
class TC039_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75134"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825375")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "test",
                                "userPwd": "wrongpassword"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication failed', "ERR: Failed")

    def test_03_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "wrongusername",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication failed', "ERR: Failed")

    def test_04_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC40 Test LDAP server_LDAP search test(Basic Search)
class TC040_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75135"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825376")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "test",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=test,CN=Users,DC=os-autosnwl,DC=com', "ERR: Failed")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC41 Test LDAP server_LDAP search test(Basic Search_user/group name with wildcard format)
class TC041_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75136"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825377")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "tes*",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=test,CN=Users,DC=os-autosnwl,DC=com', "ERR: Failed")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC42 Test LDAP server_LDAP search test(Advanced Search)
class TC042_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-77098"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825378")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "filter": {
                                    "filterContent": "(&(objectClass=user)(sAMAccountName=test))",
                                    "base": {
                                        "top_domain_tree": True
                                    },
                                    "scope": "subTree"
                                }
                            }
                        }
                    }
                }
            }
        }

        resp = user_ldap.test_ldap_server_advance_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=test,CN=Users,DC=os-autosnwl,DC=com', "ERR: Failed")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC43 Test LDAP server_LDAP search test(Advanced Search->'More..')
class TC043_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75137"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825379")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "filter": {
                                    "filterContent": "(&(objectClass=user)(sAMAccountName=Administrator))",
                                    "base": {
                                        "root_directory": True
                                    },
                                    "scope": "base-entry-only"
                                }
                            }
                        }
                    }
                }
            }
        }

        resp = user_ldap.test_ldap_server_advance_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=Aggregate,CN=Schema,CN=Configuration,DC=os-autosnwl,DC=com',
                                 "ERR: Failed")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC44 Test LDAP server_LDAP search test(Same user name in two different LDAP Server)
class TC044_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75138"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825380")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_add_ldap_server2(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_03_test_ldap_server1(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "Administrator",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication succeeded', "ERR: Failed")

    def test_04_test_ldap_server2(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.86",
                        "type": {
                            "user_authentication": {
                                "userName": "Administrator",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication succeeded', "ERR: Failed")

    def test_05_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC45 Test LDAP server_LDAP search test(Same Group name in two different LDAP Server)
class TC045_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75139"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825381")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_add_ldap_server2(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_03_test_ldap_server1(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "Protected Users",
                                    "use": {
                                        "group": "name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=Protected Users,CN=Users,DC=os-autosnwl,DC=com', "ERR: Failed")

    def test_04_test_ldap_server2(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.86",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "Protected Users",
                                    "use": {
                                        "group": "name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=Protected Users,CN=Users,DC=wsv2,DC=os-autosnwl,DC=com',
                                 "ERR: Failed")

    def test_05_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC46 Test LDAP server_LDAP search test(Same user name in one partition with two different LDAP Server)
class TC046_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75140"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825382")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(5)

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(5)

    def test_05_test_ldap_server1(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "user_authentication": {
                                "userName": "Administrator",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication succeeded', "ERR: Failed")

    def test_06_test_ldap_server2(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.86",
                        "type": {
                            "user_authentication": {
                                "userName": "Administrator",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'LDAP authentication succeeded', "ERR: Failed")

    def test_07_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC47 Different LDAP Protocol version check with LDAP Server
class TC047_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75141"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825383")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server1(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_ldap_settings(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "protocol_version": 2
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"protocol_version": 2', "failed to set protocol version")

    def test_03_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_04_ldap_settings(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "protocol_version": 3
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"protocol_version": 3', "failed to set protocol version")

    def test_05_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_06_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC48 specified Return attributes will return matched attribute
class TC048_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75142"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825384")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "return_attribute": "DC=os-autosnwl",
                                "basic": {
                                    "searchContent": "test",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'CN=test,CN=Users,DC=os-autosnwl,DC=com', "ERR: Failed")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC49 Test LDAP server_Error testing
class TC049_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75143"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825385")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '1.1.1.1',
                        "enable": True,
                        "role": {
                            "primary": True
                        },
                        "port": 389,
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
                            "primary_domain": "test.com",
                            "users_tree": [{
                                "name": "test.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "test.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "dummy",
                                "location": "test.com/Users"
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

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "1.1.1.1"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server1(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "1.1.1.1",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'Error connecting to LDAP server', "ERR: Failed")

    def test_03_test_ldap_server2(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "1.1.1.1",
                        "type": {
                            "user_authentication": {
                                "userName": "test",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'Error connecting to LDAP server', "ERR: Failed")

    def test_04_test_ldap_server3(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "1.1.1.1",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "test",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server_basic_search(msg=True, **ldap_test)
        Assertion.assert_regular(json.dumps(resp), 'Error connecting to LDAP server', "ERR: Failed")

    def test_05_delete_ldap(self):
        resp = user_ldap.del_ldap_server("1.1.1.1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC50 Import users from a specific LDAP server
class TC050_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75144"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825386")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test2",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "wsv2.os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test2"', "ERR: Failed to add partition")

    def test_04_add_primary_ldap(self):
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
        time.sleep(3)

    def test_05_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
                        },
                        "port": 389,
                        "partition": "test2",
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(3)

    def test_06_import_ldap1_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "test", "ERR: Failed to import LDAP user.")

    def test_07_delete_local_user1(self):
        resp = local_user.delete_local_user_with_domain(username="test", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete user")

    def test_08_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_10_delete_auth_partition1(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

    def test_11_delete_auth_partition2(self):
        resp = user_auth_partition.del_auth_partition("test2")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC51 Import users from all LDAP servers in a specified partition
class TC051_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75145"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825387")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}, {"name": "wsv2.os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(3)

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(3)

    def test_05_import_ldap1_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test",
                        "domain": "os-autosnwl.com"
                    }, {
                        "name": "GUEST",
                        "domain": "wsv2.os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), "test", "ERR: Failed to import LDAP user.")
        Assertion.assert_regular(json.dumps(get_resp), "GUEST", "ERR: Failed to import LDAP user.")

    def test_06_delete_local_user1(self):
        resp = local_user.delete_local_user_with_domain(username="test", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete user")

        resp = local_user.delete_local_user_with_domain(username="GUEST", domainname="wsv2.os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete user")

    def test_07_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC52 Import the users in different domains with the same name('domain\name' or 'name@domain.com' format)
class TC052_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75145"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825387")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}, {"name": "wsv2.os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(3)

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(3)

    def test_05_set_local_user_settings(self):
        user_setting = {
            "user": {
                "local": {
                    "domain_name_display_format": {
                        "name_at_domain": True
                    }
                }
            }
        }
        response = local_user.config_user_local_base(**user_setting)
        Assertion.assert_equal(response, True, "ERR: setting domain name display failed")

    def test_06_import_ldap1_user(self):
        import_ldap = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test",
                        "domain": "os-autosnwl.com"
                    }, {
                        "name": "GUEST",
                        "domain": "wsv2.os-autosnwl.com"
                    }]
                }
            }
        }
        resp = local_user.import_local_usr_from_ldap(**import_ldap)
        logger.info(resp)
        get_resp = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(get_resp), '"display_name": "test@os-autosnwl.com"',
                                 "ERR: Failed to import LDAP user.")
        Assertion.assert_regular(json.dumps(get_resp), '"display_name": "GUEST@wsv2.os-autosnwl.com"',
                                 "ERR: Failed to import LDAP user.")

    def test_07_delete_local_user1(self):
        resp = local_user.delete_local_user_with_domain(username="test", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete user")

        resp = local_user.delete_local_user_with_domain(username="GUEST", domainname="wsv2.os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete user")

    def test_08_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_10_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC53 Import groups from a specific LDAP server
class TC053_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75148"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825390")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}, {"name": "wsv2.os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(3)

    def test_04_create_local_group(self):
        local_group = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "Protected Users",
                            "domain": "os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        local_group = local_user.add_local_group(**local_group)
        resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "Protected Users"', "failed to add groups")

    def test_05_delete_local_group(self):
        resp = local_user.delete_local_group_with_domain(groupname="Protected Users", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete group")

    def test_06_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC54 Import groups from all LDAP servers in a specific partition
class TC054_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75149"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825391")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}, {"name": "wsv2.os-autosnwl.com"}
                            ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(3)

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(3)

    def test_05_create_local_group(self):
        local_group = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "Protected Users",
                            "domain": "os-autosnwl.com"
                        },
                        {
                            "name": "Domain Guests",
                            "domain": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        local_group = local_user.add_local_group(**local_group)
        resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "Protected Users"', "failed to add groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Guests"', "failed to add groups")

    def test_06_delete_local_group(self):
        resp = local_user.delete_local_group_with_domain(groupname="Protected Users", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete group")

        resp = local_user.delete_local_group_with_domain(groupname="Domain Guests", domainname="wsv2.os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete group")


    def test_07_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC55 Import the groups in different domains with the same name( 'name@domain.com' format)
class TC055_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75151"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825393")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}, {"name": "wsv2.os-autosnwl.com"}
                            ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(3)

    def test_04_add_secondary_ldap(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
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
        time.sleep(3)

    def test_05_set_local_user_settings(self):
        user_setting = {
            "user": {
                "local": {
                    "domain_name_display_format": {
                        "name_at_domain": True
                    }
                }
            }
        }
        response = local_user.config_user_local_base(**user_setting)
        Assertion.assert_equal(response, True, "ERR: setting domain name display failed")

    def test_06_create_local_group(self):
        local_group = {
            "user": {
                "local": {
                    "group": [
                        {
                            "name": "Protected Users",
                            "domain": "os-autosnwl.com"
                        },
                        {
                            "name": "Domain Guests",
                            "domain": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        local_group = local_user.add_local_group(**local_group)
        resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"display_name": "Protected Users@os-autosnwl.com"',
                                 "failed to add groups")
        Assertion.assert_regular(json.dumps(resp), '"display_name": "Domain Guests@wsv2.os-autosnwl.com"',
                                 "failed to add groups")

    def test_07_delete_local_group(self):
        resp = local_user.delete_local_group_with_domain(groupname="Protected Users", domainname="os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete group")

        resp = local_user.delete_local_group_with_domain(groupname="Domain Guests", domainname="wsv2.os-autosnwl.com")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete group")

    def test_08_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_10_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC56 Exclude groups in specified sub-trees work (including with wildcards format )
class TC056_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75154"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825397")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_02_add_secondary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_03_exclude_group_subtree(self):
        sub_tree = {
            "user": {
                "ldap": {
                    "exclude_tree": [
                        {
                            "subTree": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        resp = user_ldap.exclude_sub_trees(**sub_tree)
        Assertion.assert_equal(resp, True, "failed to add exclude groups")

    def test_04_set_mirror_settings(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "mirror_user_groups": {
                        "all": True,
                        "refresh": {
                            "period": 5
                        }
                    }
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"all": true', "failed to set protocol version")

    def test_05_refresh_ldap(self):
        resp = user_ldap.refresh_from_ldap()
        time.sleep(10)

    def test_06_get_mirrored_group(self):
        resp = local_user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp), '"wsv2.os-autosnwl.com"', "failed to add groups")

    def test_07_delete_excluded_group(self):
        sub_tree = {
            "user": {
                "ldap": {
                    "exclude_tree": [
                        {
                            "subTree": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        resp = user_ldap.delete_exclude_sub_trees(**sub_tree)
        Assertion.assert_equal(resp, True, "failed to delete exclude groups")

    def test_07_delete_local_group(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "mirror_user_groups": {
                    },
                    "del_mirrored_user_groups": True
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {}', "failed to set protocol version")

    def test_08_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC57 Remove trees configured for 'Exclude groups in specified sub-trees'
class TC057_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75155"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825399")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_02_add_secondary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_03_exclude_group_subtree(self):
        sub_tree = {
            "user": {
                "ldap": {
                    "exclude_tree": [
                        {
                            "subTree": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        resp = user_ldap.exclude_sub_trees(**sub_tree)
        Assertion.assert_equal(resp, True, "failed to add exclude groups")

    def test_04_set_mirror_settings(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "mirror_user_groups": {
                        "all": True,
                        "refresh": {
                            "period": 5
                        }
                    }
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"all": true', "failed to set protocol version")

    def test_05_refresh_ldap(self):
        resp = user_ldap.refresh_from_ldap()
        time.sleep(10)

    def test_06_get_mirrored_group(self):
        resp = local_user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp), '"wsv2.os-autosnwl.com"', "failed to verify groups")

    def test_07_delete_excluded_group(self):
        sub_tree = {
            "user": {
                "ldap": {
                    "exclude_tree": [
                        {
                            "subTree": "wsv2.os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        resp = user_ldap.delete_exclude_sub_trees(**sub_tree)
        Assertion.assert_equal(resp, True, "failed to delete exclude groups")

    def test_08_refresh_ldap(self):
        resp = user_ldap.refresh_from_ldap()
        time.sleep(10)

    def test_09_get_mirrored_group(self):
        resp = local_user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"wsv2.os-autosnwl.com"', "failed to verify groups")

    def test_10_delete_local_group(self):
        add_ldap_setting = {
            "user": {
                "ldap": {
                    "mirror_user_groups": {
                    },
                    "del_mirrored_user_groups": True
                }
            }
        }
        ldap_settings_resp = user_ldap.config_ldap_setting(**add_ldap_setting)
        Assertion.assert_equal(ldap_settings_resp, True, "ERR: Failed to change settings")

        resp = user_ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {}', "failed to set protocol version")

    def test_11_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_12_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC58 Add a LDAP Server for sub-partition
class TC058_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75157"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825401")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_sub_auth_partition(self):
        auth_partition = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test_sub",
                            "parent_partition": "test1",
                            "comment": "",
                            "domain": [{"name": "wsv2.os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_04_add_primary_ldap(self):
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
                        "partition": "test_sub",
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test_sub"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_05_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_sub_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test_sub")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC59 Backup/replica LDAP server can be  used when Primary LDAP Server  is down or unreachable
class TC059_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75158"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825402")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
        auth_partition = {
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        time.sleep(5)

    def test_04_add_backup_server(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.86",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": False
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        time.sleep(3)

    def test_05_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_06_edit_ldap_server(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': "192.168.168.85",
            'enable': False,
        }
        response = user_ldap.edit_ldap_server(**edit_ldap_server)
        logger.info(response)

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"enable": False', "ERR: Failed to edit ldap server")
        time.sleep(3)

    def test_07_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, False, "failed to test ldap")

    def test_08_test_backup_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.86",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_09_delete_backup_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_10_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_11_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC60 Continuation references in Auto-configure
class TC060_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75159"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825403")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_auto_configure_trees(self):
        auto_config_tree_json = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.85",
                            "directory": {
                                "read_trees_from_server": {
                                    "domain": "os-autosnwl.com",
                                    "type": {
                                        "replace": {
                                            "add": True
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.auto_configure_trees(**auto_config_tree_json)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to auto configure tree")

    def test_03_get_ldap_details(self):
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

        count_user_trees = len(resp['user']['ldap']['server'][0]['directory']['users_tree'])
        count_user_group_trees = len(resp['user']['ldap']['server'][0]['directory']['user_groups_tree'])
        if count_user_trees > 1 and count_user_group_trees > 1:
            response = True
        else:
            response = False

        Assertion.assert_equal(response, True, "ERR: Failed to auto configure tree")

    def test_04_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC61 Auto-configure with blank fields for Primary domain and User tree for login
class TC061_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75160"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825404")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_02_auto_configure_trees(self):
        auto_config_tree_json = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.85",
                            "directory": {
                                "read_trees_from_server": {
                                    "domain": "",
                                    "type": {
                                        "replace": {
                                            "add": True
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        resp, resp_msg = user_ldap.auto_configure_trees(**auto_config_tree_json, msg=True)
        Assertion.assert_equal(resp, False, "ERR: Failed to auto configure tree")
        Assertion.assert_regular(json.dumps(resp_msg), '"message": "Incomplete command."',
                                 "ERR: Failed to config the ldap server")

    def test_03_get_ldap_details(self):
        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

        count_user_trees = len(resp['user']['ldap']['server'][0]['directory']['users_tree'])
        count_user_group_trees = len(resp['user']['ldap']['server'][0]['directory']['user_groups_tree'])
        if count_user_trees == 1 and count_user_group_trees == 1:
            response = True
        else:
            response = False

        Assertion.assert_equal(response, True, "ERR: Failed to auto configure tree")

    def test_04_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC62 LDAP functionality with 'Anonymous login' selected in the configuration
class TC062_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75161"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825410")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
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
                            "anonymous": True
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"bind": {"anonymous": true}', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC63 LDAP functionality with 'Give login name/location in tree' selected in the configuration
class TC063_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75162"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825411")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"location": "os-autosnwl.com/Users"', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC64 LDAP functionality with Give bind distinguished name' selected in the configuration
class TC064_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75163"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, "1825412")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ldap_server(self):
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
                            "distinguished_name": "CN=Administrator,CN=Users,DC=os-autosnwl,DC=com"
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"bind": {"distinguished_name": "CN=Administrator,CN=Users,DC=os-autosnwl,DC=com"}', "ERR: Failed to config the ldap server")
        time.sleep(5)

    def test_02_test_ldap_server(self):
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = user_ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True, "failed to test ldap")

    def test_03_delete_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")


# TC65 Add the second primary LDAP server in the same partition
class TC065_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75080"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529218')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_04_add_ldap2(self):
        ldap_server2_primary = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2_primary)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"primary": true',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_delete_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_06_delete_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC66 Add two or more secondary LDAP servers in the partition
class TC066_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75081"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529219')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")


    def test_03_add_primary_ldap(self):
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.85")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"',
                                 "ERR: Failed to config the ldap server")

    def test_04_add_secondary_ldap1(self):
        ldap_server2 = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.86',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv2.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv2.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv2.os-autosnwl.com/Users"
                            }
                        },
                        "bind_password": "password",
                        "referred_bind_with_account": "local"
                    }]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**ldap_server2)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.86")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.86"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_05_add_secondary_ldap2(self):
        ldap_server = {
            "user": {
                "ldap": {
                    "server": [{
                        "host": '192.168.168.87',
                        "enable": True,
                        "role": {
                            "secondary": True
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
                            "primary_domain": "wsv3.os-autosnwl.com",
                            "users_tree": [{
                                "name": "wsv3.os-autosnwl.com/Users"
                            }],
                            "user_groups_tree": [{
                                "name": "wsv3.os-autosnwl.com/Users"
                            }]
                        },
                        "bind": {
                            "acct": {
                                "name": "Administrator",
                                "location": "wsv3.os-autosnwl.com/Users"
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

        resp = user_ldap.show_ldap_server_by_name("192.168.168.87")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.87"',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"secondary": true',
                                 "ERR: Failed to config the ldap server")
        Assertion.assert_regular(json.dumps(resp), '"partition": "test1"',
                                 "ERR: Failed to config the ldap server")

    def test_06_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_secondary_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.86")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_secondary_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.87")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")


# TC67 Add two or more Backup/replica LDAP servers for the primary server in the same partition
class TC067_Multiple_Ldap(Test):
    uuid = "SOSAIOT-TC-75083"
    description = show_testcase_info(Parameter.TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529221')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

    def test_02_add_auth_partition(self):
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
        res = user_auth_partition.add_auth_partition(**auth_partition)
        Assertion.assert_equal(res, True, "ERR: Failed to add partition")

        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")

    def test_03_add_primary_ldap(self):
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

    def test_04_add_backup_server1(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.105",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.105")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.105"',
                                 "ERR: Failed to config the ldap server")

    def test_05_add_backup_server2(self):
        backup_server = {
            "user": {
                "ldap": {
                    "server": [
                        {
                            "host": "192.168.168.110",
                            "enable": True,
                            "role": {
                                "backup": True
                            },
                            "backup_for": "192.168.168.85",
                            "same_bind_credentials": True
                        }
                    ]
                }
            }
        }
        ldap_user = user_ldap.add_ldap_server_new(**backup_server)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add backup LDAP")

        resp = user_ldap.show_ldap_server_by_name("192.168.168.110")
        Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.110"',
                                 "ERR: Failed to config the ldap server")

    def test_06_delete_backup_ldap1(self):
        resp = user_ldap.del_ldap_server("192.168.168.105")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_07_delete_backup_ldap2(self):
        resp = user_ldap.del_ldap_server("192.168.168.110")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_08_delete_primary_ldap(self):
        resp = user_ldap.del_ldap_server("192.168.168.85")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

    def test_09_delete_auth_partition(self):
        resp = user_auth_partition.del_auth_partition("test1")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete partition")

