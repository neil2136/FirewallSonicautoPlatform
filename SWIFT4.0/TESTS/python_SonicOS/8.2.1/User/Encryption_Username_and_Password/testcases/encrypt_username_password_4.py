from definition.settings import *


class nontc_config(Test):
    uuid = 'NonTC'
    
    def test_01_config_radius(self):
        add_radius_server = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 1812,
            'secret': 'radiuspassword',
            'send_through_vpn_tunnel': False
        }
        response = radius_user.add_radius_server(**add_radius_server)
        logger.info(response)
        response_get = radius_user.show_radius_server()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"', 'ERR: Failed to create radius server')
    
    def test_02_add_radius_accounting_server(self):
      add_accounting_server = {
        "host": "10.10.10.10",
        "enable": True,
        "port": 40,
        "secret": "accountingpassword",
        "user_name_format": "name_dot_domain"
      }
      response = radius_user.add_radius_account(**add_accounting_server)
      Assertion.assert_equal(response, True, 'ERR: Failed to add RADIUS Accounting Server')
    
    @repeat_method(5)
    def test_03_edit_aws_connection(self):
        time.sleep(60)
        aws_conn = {
    		'access_id':'AKIA2QAXUGQ4NG5GPCW6',
    		'password':'j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw',
    		'region':'north-virginia'
        }
        aws_connection.edit_aws_connection(**aws_conn)
        response1 = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response1), '"access_key_id": "AKIA2QAXUGQ4NG5GPCW6"', "ERR: Failed to update AWS connection")
    
    def test_04_edit_dynamic_botnet_list_server(self):
        botnet_obj= {
            "botnet":{
                "dynamic_list": {
                    "enable": True,
                    "periodical_download": False,
                    "download_interval": "5minutes",
                    "protocol": "ftp",
                    "ftp": {
                        "server_ip_address": "10.11.12.13",
                        "login": "botnet_admin",
                        "password": "botnet_password",
                        "directory_path": "/tmp/ftp_server",
                        "file_name": "test_server.txt"
                    }
                }
            }
        }   
        rc = botnet.config_botnet_base(**botnet_obj)
        Assertion.assert_equal(rc, True, "ERR: Config Botnet Settings failed")


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


def check_string_not_in_file(file_path, search_string):
    with open(file_path, 'r') as file:
        contents = file.read()
        if search_string not in contents:
            return True
        else:
            return False


class Check_Encrypt_RADIUS_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75018"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508991')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret:                         ************'
        prev_line = 'Enabled:                               Yes'
        next_line = 'User name format:                      Invalid??'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_RADIUS_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75019"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508992')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret:                         radiuspassword'
        prev_line = 'Enabled:                               Yes'
        next_line = 'User name format:                      Invalid??'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Encrypt_RADIUS_Accounting_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75020"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508993')

    def test_01_enable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret:                         ************'
        prev_line = 'Enabled:                               Yes'
        next_line = 'User name format:                      Name.Domain'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Unencrypt_RADIUS_Accounting_Password_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75021"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1508994')

    def test_01_disable_encryption_password_tsr_options(self):
        tsr_options = {
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_password_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Shared Secret:                         accountingpassword'
        prev_line = 'Enabled:                               Yes'
        next_line = 'User name format:                      Name.Domain'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_AWS_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75030"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509003')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'AccessKeyId:			"********"'
        prev_line = 'Domain:                "amazonaws.com"'
        next_line = 'TLSCompatible:         "No"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted_not_present(self):
        file_path = '/tmp/techSupport'
        search_string = 'AccessKey:             '
        # If sensitive keys are excluded, the "AccessKey" field itself will not be there in TSR
        res = check_string_not_in_file(file_path, search_string)
        Assertion.assert_equal(res, True, "ERR: Found the AccessKey even though Sensitive Keys are excluded")


class Check_AWS_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75031"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509004')

    def test_01_disable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'AccessKeyId:			"AKIA2QAXUGQ4NG5GPCW6"'
        prev_line = 'Domain:                "amazonaws.com"'
        next_line = 'TLSCompatible:         "No"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted_not_present(self):
        file_path = '/tmp/techSupport'
        search_string = 'AccessKey:             '
        # If sensitive keys are excluded, the "AccessKey" field itself will not be there in TSR
        res = check_string_not_in_file(file_path, search_string)
        Assertion.assert_equal(res, True, "ERR: Found the AccessKey even though Sensitive Keys are excluded")


class Check_AWS_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75032"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509005')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'AccessKeyId:			"********"'
        prev_line = 'AccessKey:             "j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw"'
        next_line = 'TLSCompatible:         "No"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'AccessKey:             "j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw"'
        prev_line = 'Domain:                "amazonaws.com"'
        next_line = 'AccessKeyId:			"********"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_AWS_Unencrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75033"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509006')

    def test_01_disable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'AccessKeyId:			"AKIA2QAXUGQ4NG5GPCW6"'
        prev_line = 'AccessKey:             "j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw"'
        next_line = 'TLSCompatible:         "No"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'AccessKey:             "j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw"'
        prev_line = 'Domain:                "amazonaws.com"'
        next_line = 'AccessKeyId:			"AKIA2QAXUGQ4NG5GPCW6"'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Botnet_Server_Encrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75034"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509007')

    def test_01_enable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'userName:********'
        prev_line = 'dirPath:/tmp/ftp_server'
        next_line = 'password:********'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:********'
        prev_line = 'userName:********'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Botnet_Server_Unencrypt_Username_Encrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75035"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509008')

    def test_01_disable_encryption_username_enable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": True,
                "sensitive_keys": False
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_unencrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'userName:botnet_admin'
        prev_line = 'dirPath:/tmp/ftp_server'
        next_line = 'password:********'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_encrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:********'
        prev_line = 'userName:botnet_admin'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")


class Check_Botnet_Server_Encrypt_Username_Unencrypt_Sensitive_Keys_Present_TSR(Test):
    uuid = "SOSAIOT-TC-75036"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1509009')

    def test_01_enable_encryption_username_disable_encryption_sensistive_keys_tsr_options(self):
        tsr_options = {
                "user_name": False,
                "sensitive_keys": True
            }
        rc = diagnostic.conf_tsr(**tsr_options)
        Assertion.assert_equal(rc, True, "ERR: Config TSR Options failed")
    
    def test_02_download_tsr_and_check_username_encrypted(self):
        diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'userName:********'
        prev_line = 'dirPath:/tmp/ftp_server'
        next_line = 'password:botnet_password'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")

    def test_03_check_sensitive_keys_unencrypted(self):
        file_path = '/tmp/techSupport'
        search_line = 'password:botnet_password'
        prev_line = 'userName:********'
        next_line = 'httpUserName:'
        res = check_string_with_context(file_path, search_line, prev_line, next_line)
        Assertion.assert_equal(res, True, "ERR: Unable to find required data")
