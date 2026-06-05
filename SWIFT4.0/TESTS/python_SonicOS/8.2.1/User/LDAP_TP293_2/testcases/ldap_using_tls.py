from definition.settings import *


class ldap_config(Test):
    uuid = 'NonTC'
    
    def test_01_configure_dns(self):
        dns_dict = {
            "dns": {
                "server": {
                    "inherit": False,
                    "static": {
                        "primary": "192.168.168.85"
                    }
                }
            }
        }
        rc = dnssettingapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_02_config_ldap_server(self):
        add_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.add_ldap_server(**add_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"host": "OS-WSV.os-autosnwl.com"', "ERR: Failed to config LDAP Server")

    def test_03_config_auth_method_ldap(self):
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
                                 "ERR: LDAP method is not selected successfully")

    def test_04_add_CA_cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = certobj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'ERR: Add CA Cert failed')
  


class TC01_GUI_Enable_RADIUS_to_LDAP_Relay(Test):
    uuid = "SOSAIOT-TC-77024"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503616')

    def test_01_tls_test_connection_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_connection_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class TC02_Import_user_from_LDAP_on_the_Local_Users_page(Test):
    uuid = "SOSAIOT-TC-77027"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503621')

    def test_01_tls_test_user_authentication_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_user_authentication_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class TC03_Import_user_from_LDAP_on_Users_tab_of_the_LDAP_configuration(Test):
    uuid = "SOSAIOT-TC-77028"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503622')

    def test_01_tls_test_user_authentication_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_user_authentication_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")



class TC04_LDAP_login_of_Sonicwall_Administrator_using_empty_password(Test):
    uuid = "SOSAIOT-TC-77033"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503627')

    def test_01_tls_test_user_authentication_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_user_authentication_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class TC05_GUI_LDAP_Configuration_Settings_Login_Password_field(Test):
    uuid = "SOSAIOT-TC-77034"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503628')

    
    def test_01_tls_test_user_authentication_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_user_authentication_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class TC06_GEN7_37403_Firewall_is_not_accepting_LDAP_server_name_that_begins_with_a_number(Test):
    uuid = "SOSAIOT-TC-77036"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503632')

    
    def test_01_tls_test_user_authentication_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS without Cert failed')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_tls_test_user_authentication_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication TLS with Cert failed')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class TC07_GUI_LDAP_Configuration_Settings_Use_TLS_SSL(Test):
    uuid = "SOSAIOT-TC-77037"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503633')

    def test_01_edit_ldap_server_port_3268(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3268,
            'use_tls': False,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3268', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3268(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3268 failed')
    
    def test_03_test_user_authentication_windows_gc_port_3268(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3268 failed')
    
    def test_04_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")


class TC08_GUI_LDAP_Configuration_Settings_Require_valid_certificate_from_server(Test):
    uuid = "SOSAIOT-TC-77038"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503634')

    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")


class TC10_GUI_LDAP_Configuration_Schema_LDAP_Schema_list(Test):
    uuid = "SOSAIOT-TC-77040"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503636')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")



class TC09_GUI_LDAP_Configuration_Settings_Local_certificate_for_TLS(Test):
    uuid = "SOSAIOT-TC-77039"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503635')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")


class TC10_GUI_LDAP_Configuration_Schema_LDAP_Schema_list(Test):
    uuid = "SOSAIOT-TC-77040"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503636')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")



class TC11_GUI_LDAP_Configuration_Schema_Microsoft_Active_Directory_selected(Test):
    uuid = "SOSAIOT-TC-77041"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503637')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")





class TC12_GUI_Select_LDAP(Test):
    uuid = "SOSAIOT-TC-77042"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503638')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")




class TC13_GUI_LDAP_Configuration_Directory_Primary_domain_field(Test):
    uuid = "SOSAIOT-TC-77043"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503639')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")




class TC14_GUI_LDAP_Configuration_Directory_DNS_for_user_trees_Add(Test):
    uuid = "SOSAIOT-TC-77044"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503640')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")



class TC15_GUI_LDAP_Configuration_Directory_DNs_for_user_trees_Remove(Test):
    uuid = "SOSAIOT-TC-77045"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503641')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")




class TC16_GUI_Select_LDAP_Local_Users(Test):
    uuid = "SOSAIOT-TC-77046"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503642')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")




class TC17_GUI_LDAP_Configuration_LDAP_Users_Default_LDAP_User_Group_Select(Test):
    uuid = "SOSAIOT-TC-77047"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503643')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")





class TC18_GUI_LDAP_Configuration_LDAP_Users_Default_LDAP_User_Group_Create_a_new_user_group(Test):
    uuid = "SOSAIOT-TC-77048"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503644')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")





class TC19_GUI_LDAP_Configuration_Settings_Name_or_IP_Address_field_Use_IP_address(Test):
    uuid = "SOSAIOT-TC-77053"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503649')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")





class TC20_Functional_Connection_to_LDAP_server_TLS_is_used(Test):
    uuid = "SOSAIOT-TC-77058"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503654')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")






class TC21_LDAP_server_is_successful_when_TLS_is_used_and_a_server_CA_certificate_is_not_required(Test):
    uuid = "SOSAIOT-TC-77059"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503655')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")








class TC22_Functional_TLS_is_used_sending_Start_TLS_request_is_required(Test):
    uuid = "SOSAIOT-TC-77060"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503656')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")









class TC23_Functional_Microsoft_Active_Directory_schema_is_used(Test):
    uuid = "SOSAIOT-TC-77063"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1503664')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")









class TC24_GEN8_3585_LDAP_user_with_wrong_domain_should_not_be_authed_successfully(Test):
    uuid = "SOSAIOT-TC-77093"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2797797')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")











class TC25_Correct_user_password_with_the_wrong_domain_should_not_be_authed_successfully(Test):
    uuid = "SOSAIOT-TC-77095"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2913938')

    
    def test_01_edit_ldap_server_port_3269(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 3269,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 3269', "ERR: Failed to edit LDAP Server port")

    def test_02_test_connection_windows_gc_port_3269_without_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 without certificate failed')
    
    def test_03_test_user_authentication_windows_gc_port_3269_without_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 without certificate failed')
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")
    
    def test_05_test_connection_windows_gc_port_3269_with_cert(self):
        test_ldap = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "connectivity_bind": True
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_ldap)
        Assertion.assert_equal(resp, True, 'ERR: Test Connection Windows GC Port 3269 with certificate failed')
    
    def test_06_test_user_authentication_windows_gc_port_3269_with_cert(self):
        test_user_auth = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "OS-WSV.os-autosnwl.com",
                        "type": {
                            "user_authentication": {
                                "userName": "user1a",
                                "userPwd": "password"
                            }
                        }
                    }
                }
            }
        }
        resp = ldap.test_ldap_server(**test_user_auth)
        Assertion.assert_equal(resp, True, 'ERR: Test User Authentication Windows GC Port 3269 with certificate failed')
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")
    
    def test_08_revert_ldap_server_settings(self):
        edit_ldap_server = {
            'role': 'primary',
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 636,
            'use_tls': True,
            'timeout': True,
            'servertimeout': 5,
            'overalloperationtimeout': 4,
            'send_start_tls_request': False,
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
        ldap.edit_ldap_server(**edit_ldap_server)
        resp = ldap.show_ldap_servers()
        Assertion.assert_regular(json.dumps(resp), '"port": 636', "ERR: Failed to edit LDAP Server port")




