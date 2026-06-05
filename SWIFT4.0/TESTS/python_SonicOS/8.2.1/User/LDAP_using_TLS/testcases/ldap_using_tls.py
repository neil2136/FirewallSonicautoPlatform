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
    
    def test_05_create_sslvpn_address_object(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.10,192.168.168.20"
        }
        address_objects.config_addressobject(**address_object)
        resp = address_objects.get_addressobject_by_name("sslvpn_range", "ipv4")
        Assertion.assert_regular(json.dumps(resp), '"name": "sslvpn_range"', "Err: failed to create address object")

    def test_06_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

    def test_07_enable_sslvpn_access(self):
        enable = {
            'WAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_08_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_09_add_all_ldap_users_to_sslvpn_services(self):
        member = {
            'action': 'add',
            'groupname': 'SSLVPN Services',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        user_local.group_member_of(**member)
        resp1 = user_local.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp1), '"name": "All LDAP Users"', 'ERR: All LDAP Users not added to SSLVPN Services')


class LDAP_Test_Connection(Test):
    uuid = "SOSAIOT-TC-77201"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529406')

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


class LDAP_Test_User_Authentication(Test):
    uuid = "SOSAIOT-TC-77202"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529407')

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


class LDAP_User_Change_Password_Virtual_Office(Test):
    uuid = "SOSAIOT-TC-77203"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529408')

    def test_01_change_password_virtual_office_without_cert(self):
        url = "https://13.0.0.100:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition/ui_user.py ' + '-url ' + url + ' -user changepassword1 -pwd password portallogin'
        out = PC2_login.send_command(cmd)
        logger.info(f"Change password VO without Certificate: {out}")
        Assertion.assert_not_regular(out, 'Exception:', 'ERR: Exception raised')

    def test_02_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_03_change_password_virtual_office_with_cert(self):
        url = "https://13.0.0.100:4433"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition/ui_user.py ' + '-url ' + url + ' -user changepassword2 -pwd password portallogin'
        out = PC2_login.send_command(cmd)
        logger.info(f"Change password VO with Certificate: {out}")
        Assertion.assert_not_regular(out, 'Exception:', 'ERR: Exception raised')

    def test_04_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class LDAP_User_Change_Password_NX(Test):
    uuid = "SOSAIOT-TC-77204"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529409')

    def test_01_install_nx(self):
        cp_nx.buildnx_linux_remote('-PC2')
        inst = cp_nx.install_nx_linux_remote('-PC2')
        logger.info(inst)
    
    def test_02_change_password_nx_without_cert(self):
        logger.info("Changing password with NX")
        rc = nx.connect_nxlinux_remote('changepassword3', 'password', '13.0.0.100:4433', 'LocalDomain', '-PC2', new_password='newpassword')
        logger.info(f"Change password NX: {rc}")
        Assertion.assert_regular(rc, "Your password was changed successfully.", "ERR: Password was not changed")

    def test_03_verify_password_changed_nx_without_cert(self):
        logger.info("Connecting with NX")
        rc = nx.connect_nxlinux_remote('changepassword3', 'newpassword', '13.0.0.100:4433', 'LocalDomain', '-PC2')
        logger.info(f"Connect NX: {rc}")
        Assertion.assert_regular(rc, "NetExtender connected successfully.", "ERR: NX is not connected")
    
    def test_04_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_05_change_password_nx_with_cert(self):
        logger.info("Changing password with NX")
        rc = nx.connect_nxlinux_remote('changepassword4', 'password', '13.0.0.100:4433', 'LocalDomain', '-PC2', new_password='newpassword')
        logger.info(f"Change password NX: {rc}")
        Assertion.assert_regular(rc, "Your password was changed successfully.", "ERR: Password was not changed")

    def test_06_verify_password_changed_nx_with_cert(self):
        logger.info("Connecting with NX")
        rc = nx.connect_nxlinux_remote('changepassword4', 'newpassword', '13.0.0.100:4433', 'LocalDomain', '-PC2')
        logger.info(f"Connect NX: {rc}")
        Assertion.assert_regular(rc, "NetExtender connected successfully.", "ERR: NX is not connected")
    
    def test_07_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class Import_LDAP_Users_and_Groups(Test):
    uuid = "SOSAIOT-TC-77205"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529411')

    def test_01_import_ldap_users_without_cert(self):
        import_user = {
            "user": {
                "local": {
                    "user": [
                        {
                        "name": "user1a",
                        "domain": "os-autosnwl.com"
                        }
                    ]
		        }
	        }
        }
        user_local.import_local_usr_from_ldap(**import_user)
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "user1a"', "ERR: Importing LDAP User without certificate failed")

    def test_02_import_ldap_group_without_cert(self):
        import_group = {           
            "user": {
                "local": {        
                    "group": [
                        {                           
                            "name": "AD_Group1",
                            "domain": "os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        user_local.add_local_group(**import_group)
        resp = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group1"', "ERR: Importing LDAP Group without certificate failed")
    
    def test_03_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_04_import_ldap_users_with_cert(self):
        import_user = {
            "user": {
                "local": {
                    "user": [
                        {
                            "name": "user2b",
                            "domain": "os-autosnwl.com"
                        }
                    ]
		        }
	        }
        }
        user_local.import_local_usr_from_ldap(**import_user)
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "user2b"', "ERR: Importing LDAP User with certificate failed")

    def test_05_import_ldap_group_with_cert(self):
        import_group = {           
            "user": {
                "local": {        
                    "group": [
                        {                           
                            "name": "AD_Group2",
                            "domain": "os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        user_local.add_local_group(**import_group)
        resp = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group2"', "ERR: Importing LDAP Group with certificate failed")

    def test_06_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")

    def test_07_delete_ldap_imported_users_and_groups(self):
        user_local.delete_local_user_with_domain("user1a", "os-autosnwl.com")
        user_local.delete_local_user_with_domain("user2b", "os-autosnwl.com")
        user_resp = user_local.show_local_users()
        Assertion.assert_not_regular(json.dumps(user_resp), '"name": "user1a"', "ERR: Unable to delete user1a")
        Assertion.assert_not_regular(json.dumps(user_resp), '"name": "user2b"', "ERR: Unable to delete user2b")

        user_local.delete_local_group_with_domain("AD_Group1", "os-autosnwl.com")
        user_local.delete_local_group_with_domain("AD_Group2", "os-autosnwl.com")
        group_resp = user_local.show_local_groups()
        Assertion.assert_not_regular(json.dumps(group_resp), '"name": "AD_Group1"', "ERR: Unable to delete AD_Group1")
        Assertion.assert_not_regular(json.dumps(group_resp), '"name": "AD_Group2"', "ERR: Unable to delete AD_Group2")


class Mirror_LDAP_Groups(Test):
    uuid = "SOSAIOT-TC-77206"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529412')

    def test_01_enable_ldap_group_mirroring_without_cert(self):
        mirror_groups = {
            "mirror_user_groups": {
                "refresh": {
                    "period": 5
                },
                "have_members": True
            }
        }
        rc = ldap.ldap_setting_new(**mirror_groups)
        Assertion.assert_equal(rc, True, "ERR: Enabling LDAP Group mirroring without certificate failed")

    def test_02_refresh_from_ldap(self):
        rc = ldap.refresh_from_ldap()
        Assertion.assert_equal(rc, True, "ERR: Refresh from LDAP failed")

    def test_03_verify_ldap_groups_mirrored_without_cert(self):
        time.sleep(10)
        resp = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group1"', "ERR: AD_Group1 LDAP Group is not mirrored without certificate")
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group2"', "ERR: AD_Group2 LDAP Group is not mirrored without certificate")
    
    def test_04_disable_ldap_group_mirroring(self):
        mirror_groups = {
            "mirror_user_groups": {},
            "del_mirrored_user_groups": True
        }
        rc = ldap.ldap_setting_new(**mirror_groups)
        Assertion.assert_equal(rc, True, "ERR: Disabling LDAP Group mirroring failed")
    
    def test_05_enable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': True,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Enabling require valid certificate failed")

    def test_06_enable_ldap_group_mirroring_with_cert(self):
        mirror_groups = {
            "mirror_user_groups": {
                "refresh": {
                    "period": 5
                },
                "have_members": True
            }
        }
        rc = ldap.ldap_setting_new(**mirror_groups)
        Assertion.assert_equal(rc, True, "ERR: Enabling LDAP Group mirroring with certificate failed")

    def test_07_verify_ldap_groups_mirrored_with_cert(self):
        resp = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group1"', "ERR: AD_Group1 LDAP Group is not mirrored with certificate")
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group2"', "ERR: AD_Group2 LDAP Group is not mirrored with certificate")
    
    def test_08_disable_ldap_group_mirroring(self):
        mirror_groups = {
            "mirror_user_groups": {},
            "del_mirrored_user_groups": True
        }
        rc = ldap.ldap_setting_new(**mirror_groups)
        Assertion.assert_equal(rc, True, "ERR: Disabling LDAP Group mirroring failed")

    def test_09_disable_require_valid_certificate(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: Disabling require valid certificate failed")


class LDAP_Test_Connection_User_Authentication_GC_Port_3268(Test):
    uuid = "SOSAIOT-TC-77208"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529416')

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


class LDAP_Test_Connection_User_Authentication_GC_Port_3269(Test):
    uuid = "SOSAIOT-TC-77209"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529417')

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


class Use_LDAP_Retrieve_Group_Info_On_RADIUS_Server_Check_ULA(Test):
    uuid = "SOSAIOT-TC-77207"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529415')

    def test_01_import_ldap_group(self):
        import_group = {           
            "user": {
                "local": {        
                    "group": [
                        {                           
                            "name": "AD_Group1",
                            "domain": "os-autosnwl.com"
                        },
                        {
                            "name": "AD_Group2",
                            "domain": "os-autosnwl.com"
                        }
                    ]
                }
            }
        }
        user_local.add_local_group(**import_group)
        resp = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group1"', "ERR: Importing LDAP Group AD_Group1 without certificate failed")
        Assertion.assert_regular(json.dumps(resp), '"name": "AD_Group2"', "ERR: Importing LDAP Group AD_Group2 without certificate failed")

    def test_02_del_all_lan_to_wan_access_rules(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        if resp:
            rules_list = resp['access_rules']
            for rules in rules_list:
                uuid = rules['ipv4']['uuid']
                output = access_rules.del_ipv4_access_rule_uuid(uuid)
                Assertion.assert_equal(output, True, "ERR: Deletion of LAN to WAN rule failed")
    
    def test_03_allow_all_AD_Group1(self):
        access_rule_option = {
            'name': 'ADGroup1 Allow All',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {
                'any': True
            },
            'source_addr': {
                'any': True
            },
            'dst_addr': {
                'any': True
            },
            'user_included': {
                'group': 'OS-AUTOSNWL\\AD_Group1'
            }
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: Adding AD_Group1 Allow All Access Rule failed")

    def test_04_add_radius_server(self):
        add_radius_server_dict = {
            'host': 'OS-WSV.os-autosnwl.com',
            'enable': True,
            'port_num': 1812,
            'secret': 'password',
            'send_through_vpn_tunnel': False,
        }
        radius_user.add_radius_server(**add_radius_server_dict)
        resp = radius_user.show_radius_server()
        Assertion.assert_regular(json.dumps(resp), '"host": "OS-WSV.os-autosnwl.com"', "ERR: Failed to config RADIUS Server")
    
    def test_05_edit_radius_user_mechanism_to_ldap(self):
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
        radius_user.edit_user_radius_settings(**edit_radius_server_json)
        resp = radius_user.show_user_radius_settings()
        Assertion.assert_regular(json.dumps(resp), '"ldap": True', "ERR: Failed to config RADIUS User mechanism to LDAP")
    
    def test_06_config_auth_method_radius(self):
        user_auth = {
            "auth_method": "radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius"', "ERR: RADIUS method is not selected successfully")

    def test_07_start_httpd_service_PC2_WAN_host(self):
        cmds = ['systemctl start httpd',
                'systemctl status httpd']
        output = PC2_login.send_commands(cmds)
        Assertion.assert_regular(output, r'active \(running\)', "ERR: Failed to start httpd service on PC2 (WAN host)")
        
    def test_08_add_static_route_PC3_LAN_host(self):
        cmds = ['route add -net 13.0.0.0/24 gw 23.0.0.100',
                'ip r']
        output = PC3_login.send_commands(cmds)
        Assertion.assert_regular(output, '13.0.0.0/24 via 23.0.0.100', "ERR: Failed to configure static route on PC3 (LAN host)")

    def test_09_ula_login_blocked_user(self):
        url = "http://13.0.0.5"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition/ui_user.py ' + '-url ' + url + ' -user user2b -pwd password ulaloginblockeduser'
        out = PC3_login.send_command(cmd)
        logger.info(f"ULA Login blocked user: {out}")
        Assertion.assert_not_regular(out, 'Exception:', 'ERR: Exception raised')

    def test_10_ula_login(self):
        url = "http://13.0.0.5"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/LDAP_using_TLS/definition/ui_user.py ' + '-url ' + url + ' -user user1a -pwd password ulalogin'
        out = PC3_login.send_command(cmd)
        logger.info(f"ULA Login blocked user: {out}")
        Assertion.assert_not_regular(out, 'Exception:', 'ERR: Exception raised')
