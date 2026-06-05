from definition.settings import *


class nontc_config(Test):
    uuid = 'NonTC'
    
    def test_01_config_wlan_zone(self):
        edit_zone_object = {
            "zones": [
                {
                    "name": "WLAN",
                    "local_radius_server": {
                        "active_directory_server": {
                            "admin_user_name": "ad_admin",
                            "admin_user_password": "ad_password",
                            "domain": "addomain.com",
                            "enable": False,
                            "full_name": "ADDomain"
                        },
                        "client_password": "clientpassword",
                        "enable": True,
                        "interface_server_numbers": 2,
                        "ldap_server": {
                            "base_dn": "basedn",
                            "cache": False,
                            "cache_lifetime": 86400,
                            "enable": True,
                            "identity_dn": "idn",
                            "identity_dn_password": "idn_password",
                            "server": "10.2.3.4",
                            "tls": False
                        },
                        "port": 1810,
                        "tls_cache": False,
                        "tls_cache_lifetime": 1
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object('WLAN',**edit_zone_object)
        Assertion.assert_equal(rc, True, "ERR: Failed to configure WLAN Zone")


def check_string_with_context(file_path, target_string, prev_string, next_string):
    try:
        with open(file_path, 'r') as file:
            previous_line = None
            current_line = None
            next_line = None
            for line in file:
                previous_line = current_line
                current_line = next_line
                next_line = line.strip()
                if current_line and target_string in current_line:
                    logger.info(f"previous_line = {previous_line}")
                    logger.info(f"current_line = {current_line}")
                    logger.info(f"next_line = {next_line}")
                    if previous_line == prev_string and next_line == next_string:
                        return True
        return False
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return False


class Check_Encrypt_WLAN_RADIUS_Client_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74991"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508961')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Radius Client Password: **************'
        prev_line = 'Radius Server Port: 1810'
        next_line = 'Enable Radius Server Tls Cahce: Off'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_WLAN_RADIUS_Client_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74992"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508962')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Radius Client Password: clientpassword'
        prev_line = 'Radius Server Port: 1810'
        next_line = 'Enable Radius Server Tls Cahce: Off'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_WLAN_LDAP_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-74993"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508963')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Identity DN Password: **************'
        prev_line = 'Identity DN: idn'
        next_line = 'Enable Ldap TLS: Off'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")
